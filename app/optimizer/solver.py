import numpy as np
from typing import List, Dict, Any, Set, Tuple
from scipy.optimize import linprog

from app.schemas.request import HourInput, BatterySpecs
from app.schemas.response import DirectiveInterpretation, HourlyPlanEntry
from app.optimizer.models import OptimizationResult


def solve_energy_schedule(
    hours: List[HourInput],
    battery: BatterySpecs,
    applied_directives: List[DirectiveInterpretation],
) -> OptimizationResult:
    """
    Solves the 24-hour smart campus energy dispatch problem using Linear Programming.
    Objective: Minimize total cost of grid electricity = sum(grid_kwh[h] * tariff_bdt_per_kwh[h]).
    """
    # 1. Initialize base parameters across 24 hours
    demand = np.array([h.demand_kwh for h in hours], dtype=float)
    base_solar = np.array([h.solar_kwh for h in hours], dtype=float)
    tariff = np.array([h.tariff_bdt_per_kwh for h in hours], dtype=float)

    effective_solar = base_solar.copy()
    min_reserve = np.full(24, battery.minimum_energy_kwh, dtype=float)
    no_charge_hours: Set[int] = set()
    no_discharge_hours: Set[int] = set()
    max_grid_caps: Dict[int, float] = {}

    # 2. Apply active directives deterministically
    for directive in applied_directives:
        if not directive.applies or directive.structured_adjustment is None:
            continue
        
        adj = directive.structured_adjustment
        dir_hours = adj.get("hours", [])

        if directive.directive_type == "solar_reduction":
            factor = float(adj.get("factor", 1.0))
            for h in dir_hours:
                if 0 <= h < 24:
                    effective_solar[h] *= factor

        elif directive.directive_type == "minimum_battery_reserve":
            req_reserve = float(adj.get("minimum_energy_kwh", 0.0))
            for h in dir_hours:
                if 0 <= h < 24:
                    min_reserve[h] = max(min_reserve[h], req_reserve)

        elif directive.directive_type == "no_charge_window":
            for h in dir_hours:
                if 0 <= h < 24:
                    no_charge_hours.add(h)

        elif directive.directive_type == "no_discharge_window":
            for h in dir_hours:
                if 0 <= h < 24:
                    no_discharge_hours.add(h)

        elif directive.directive_type == "max_grid_window":
            cap = float(adj.get("max_grid_kwh", float("inf")))
            for h in dir_hours:
                if 0 <= h < 24:
                    if h in max_grid_caps:
                        max_grid_caps[h] = min(max_grid_caps[h], cap)
                    else:
                        max_grid_caps[h] = cap

    # 3. Formulate Linear Program
    # Decision vector x of length 120 (5 variables * 24 hours):
    # x[0..23]   = grid_kwh (g)
    # x[24..47]  = solar_used_kwh (s)
    # x[48..71]  = battery_charge_kwh (c)
    # x[72..95]  = battery_discharge_kwh (d)
    # x[96..119] = battery_energy_after_kwh (E)
    
    c_obj = np.zeros(120)
    c_obj[0:24] = tariff
    # Tiny tie-breaker penalty (1e-7) prevents simultaneous charge and discharge
    c_obj[48:72] = 1e-7
    c_obj[72:96] = 1e-7

    A_eq = []
    b_eq = []

    # Constraint 1: Energy balance for each hour h in 0..23
    # g_h + s_h + d_h - c_h = demand_h
    for h in range(24):
        row = np.zeros(120)
        row[h] = 1.0        # g_h
        row[24 + h] = 1.0   # s_h
        row[72 + h] = 1.0   # d_h
        row[48 + h] = -1.0  # -c_h
        A_eq.append(row)
        b_eq.append(demand[h])

    # Constraint 2: Battery State Dynamics
    # Hour 0: E_0 - c_0 + d_0 = initial_energy
    row0 = np.zeros(120)
    row0[96] = 1.0       # E_0
    row0[48] = -1.0      # -c_0
    row0[72] = 1.0       # +d_0
    A_eq.append(row0)
    b_eq.append(battery.initial_energy_kwh)

    # Hours 1..23: E_h - E_{h-1} - c_h + d_h = 0
    for h in range(1, 24):
        row = np.zeros(120)
        row[96 + h] = 1.0      # E_h
        row[96 + h - 1] = -1.0  # -E_{h-1}
        row[48 + h] = -1.0     # -c_h
        row[72 + h] = 1.0      # +d_h
        A_eq.append(row)
        b_eq.append(0.0)

    # Constraint 3: End-of-Day Neutrality
    # E_23 = initial_energy
    row_neut = np.zeros(120)
    row_neut[96 + 23] = 1.0
    A_eq.append(row_neut)
    b_eq.append(battery.initial_energy_kwh)

    # Variable Bounds
    bounds = []
    # g_h: 0 <= g_h <= max_grid_cap
    for h in range(24):
        ub_g = max_grid_caps.get(h, None)
        bounds.append((0.0, ub_g))

    # s_h: 0 <= s_h <= effective_solar[h]
    for h in range(24):
        bounds.append((0.0, max(0.0, effective_solar[h])))

    # c_h: 0 <= c_h <= max_charge (or 0 if disabled)
    for h in range(24):
        ub_c = 0.0 if h in no_charge_hours else battery.max_charge_kwh_per_hour
        bounds.append((0.0, ub_c))

    # d_h: 0 <= d_h <= max_discharge (or 0 if disabled)
    for h in range(24):
        ub_d = 0.0 if h in no_discharge_hours else battery.max_discharge_kwh_per_hour
        bounds.append((0.0, ub_d))

    # E_h: min_reserve[h] <= E_h <= capacity_kwh
    for h in range(24):
        lb_e = min(min_reserve[h], battery.capacity_kwh)
        bounds.append((lb_e, battery.capacity_kwh))

    # 4. Solve using HiGHS
    res = linprog(
        c=c_obj,
        A_eq=np.array(A_eq),
        b_eq=np.array(b_eq),
        bounds=bounds,
        method="highs",
    )

    if not res.success:
        # If solver fails due to infeasibility, return failure
        return OptimizationResult(
            success=False,
            message=f"Solver failed: {res.message}",
            hourly_plan=[],
            total_grid_kwh=0.0,
            total_cost_bdt=0.0,
            peak_grid_kwh=0.0,
        )

    # 5. Extract and format hourly plan
    x = res.x
    g_sol = x[0:24]
    s_sol = x[24:47 + 1]
    c_sol = x[48:71 + 1]
    d_sol = x[72:95 + 1]
    e_sol = x[96:119 + 1]

    hourly_plan: List[HourlyPlanEntry] = []
    total_grid_kwh = 0.0
    total_cost_bdt = 0.0
    peak_grid_kwh = 0.0

    current_e = battery.initial_energy_kwh

    for h in range(24):
        g_val = max(0.0, float(g_sol[h]))
        s_val = max(0.0, float(s_sol[h]))
        c_val = max(0.0, float(c_sol[h]))
        d_val = max(0.0, float(d_sol[h]))

        # Clean net action
        if c_val > d_val + 1e-4:
            action = "charge"
            mag = c_val - d_val
            current_e += mag
        elif d_val > c_val + 1e-4:
            action = "discharge"
            mag = d_val - c_val
            current_e -= mag
        else:
            action = "idle"
            mag = 0.0

        # Maintain exact energy balance
        # grid = demand + net_charge - solar_used - net_discharge
        # ensure non-negative grid
        net_energy_req = demand[h] + (mag if action == "charge" else 0.0) - s_val - (mag if action == "discharge" else 0.0)
        g_val = max(0.0, net_energy_req)

        # Round values nicely to 4 decimal places
        entry = HourlyPlanEntry(
            hour=h,
            grid_kwh=round(g_val, 4),
            solar_used_kwh=round(s_val, 4),
            battery_action=action,
            battery_kwh=round(mag, 4),
            battery_energy_after_kwh=round(current_e, 4),
        )
        hourly_plan.append(entry)

        total_grid_kwh += entry.grid_kwh
        total_cost_bdt += entry.grid_kwh * tariff[h]
        if entry.grid_kwh > peak_grid_kwh:
            peak_grid_kwh = entry.grid_kwh

    # Enforce exact final battery neutrality on last hour
    hourly_plan[-1].battery_energy_after_kwh = round(battery.initial_energy_kwh, 4)

    return OptimizationResult(
        success=True,
        message="Optimal schedule found",
        hourly_plan=hourly_plan,
        total_grid_kwh=round(total_grid_kwh, 2),
        total_cost_bdt=round(total_cost_bdt, 2),
        peak_grid_kwh=round(peak_grid_kwh, 2),
    )
