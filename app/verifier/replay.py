from typing import List, Tuple
from app.schemas.request import HourInput, BatterySpecs
from app.schemas.response import DirectiveInterpretation, HourlyPlanEntry


def verify_and_replay_schedule(
    hourly_plan: List[HourlyPlanEntry],
    hours: List[HourInput],
    battery: BatterySpecs,
    applied_directives: List[DirectiveInterpretation],
    tolerance: float = 0.01,
) -> Tuple[bool, List[str]]:
    """
    Independent Replay Engine simulating the competition judge harness.
    Returns (is_valid, list_of_violations).
    """
    violations: List[str] = []

    if len(hourly_plan) != 24:
        violations.append(f"hourly_plan must contain exactly 24 entries, got {len(hourly_plan)}")
        return False, violations

    # Compute effective solar and reserves
    effective_solar = [h.solar_kwh for h in hours]
    min_reserve = [battery.minimum_energy_kwh for _ in range(24)]
    no_charge_hours = set()
    no_discharge_hours = set()
    max_grid_caps = {}

    for d in applied_directives:
        if not d.applies or d.structured_adjustment is None:
            continue
        adj = d.structured_adjustment
        dir_hours = adj.get("hours", [])

        if d.directive_type == "solar_reduction":
            factor = float(adj.get("factor", 1.0))
            for h in dir_hours:
                if 0 <= h < 24:
                    effective_solar[h] *= factor

        elif d.directive_type == "minimum_battery_reserve":
            req = float(adj.get("minimum_energy_kwh", 0.0))
            for h in dir_hours:
                if 0 <= h < 24:
                    min_reserve[h] = max(min_reserve[h], req)

        elif d.directive_type == "no_charge_window":
            for h in dir_hours:
                if 0 <= h < 24:
                    no_charge_hours.add(h)

        elif d.directive_type == "no_discharge_window":
            for h in dir_hours:
                if 0 <= h < 24:
                    no_discharge_hours.add(h)

        elif d.directive_type == "max_grid_window":
            cap = float(adj.get("max_grid_kwh", float("inf")))
            for h in dir_hours:
                if 0 <= h < 24:
                    if h in max_grid_caps:
                        max_grid_caps[h] = min(max_grid_caps[h], cap)
                    else:
                        max_grid_caps[h] = cap

    prev_energy = battery.initial_energy_kwh

    for h in range(24):
        entry = hourly_plan[h]
        inp = hours[h]

        if entry.hour != h:
            violations.append(f"Hour {h}: mismatched entry hour {entry.hour}")

        # Non-negativity
        if entry.grid_kwh < -tolerance:
            violations.append(f"Hour {h}: negative grid_kwh ({entry.grid_kwh})")
        if entry.solar_used_kwh < -tolerance:
            violations.append(f"Hour {h}: negative solar_used_kwh ({entry.solar_used_kwh})")
        if entry.battery_kwh < -tolerance:
            violations.append(f"Hour {h}: negative battery_kwh ({entry.battery_kwh})")

        # Solar utilization limit
        if entry.solar_used_kwh > effective_solar[h] + tolerance:
            violations.append(
                f"Hour {h}: solar_used_kwh ({entry.solar_used_kwh}) exceeds effective_solar ({effective_solar[h]})"
            )

        # Action-specific values
        c = entry.battery_kwh if entry.battery_action == "charge" else 0.0
        d = entry.battery_kwh if entry.battery_action == "discharge" else 0.0

        if entry.battery_action == "idle" and entry.battery_kwh > tolerance:
            violations.append(f"Hour {h}: battery_action is idle but battery_kwh is {entry.battery_kwh}")

        # Directive: no charge window
        if h in no_charge_hours and c > tolerance:
            violations.append(f"Hour {h}: battery charged during no_charge_window ({c} kWh)")

        # Directive: no discharge window
        if h in no_discharge_hours and d > tolerance:
            violations.append(f"Hour {h}: battery discharged during no_discharge_window ({d} kWh)")

        # Directive: max grid window
        if h in max_grid_caps and entry.grid_kwh > max_grid_caps[h] + tolerance:
            violations.append(
                f"Hour {h}: grid_kwh ({entry.grid_kwh}) exceeds directive cap ({max_grid_caps[h]})"
            )

        # Rate limits
        if c > battery.max_charge_kwh_per_hour + tolerance:
            violations.append(f"Hour {h}: charge ({c}) exceeds max_charge ({battery.max_charge_kwh_per_hour})")
        if d > battery.max_discharge_kwh_per_hour + tolerance:
            violations.append(f"Hour {h}: discharge ({d}) exceeds max_discharge ({battery.max_discharge_kwh_per_hour})")

        # Energy balance
        left_side = entry.grid_kwh + entry.solar_used_kwh + d
        right_side = inp.demand_kwh + c
        if abs(left_side - right_side) > tolerance:
            violations.append(
                f"Hour {h}: energy balance broken. {left_side:.3f} != {right_side:.3f} (diff: {abs(left_side - right_side):.3f})"
            )

        # State of charge dynamics
        expected_soc = prev_energy + c - d
        if abs(entry.battery_energy_after_kwh - expected_soc) > tolerance:
            violations.append(
                f"Hour {h}: state transition error. Got {entry.battery_energy_after_kwh:.3f}, expected {expected_soc:.3f}"
            )

        # Reserve and capacity bounds
        if entry.battery_energy_after_kwh < min_reserve[h] - tolerance:
            violations.append(
                f"Hour {h}: battery energy ({entry.battery_energy_after_kwh}) fell below required minimum ({min_reserve[h]})"
            )
        if entry.battery_energy_after_kwh > battery.capacity_kwh + tolerance:
            violations.append(
                f"Hour {h}: battery energy ({entry.battery_energy_after_kwh}) exceeded capacity ({battery.capacity_kwh})"
            )

        prev_energy = entry.battery_energy_after_kwh

    # End-of-day battery neutrality
    if abs(hourly_plan[-1].battery_energy_after_kwh - battery.initial_energy_kwh) > tolerance:
        violations.append(
            f"End-of-day neutrality violated. Final {hourly_plan[-1].battery_energy_after_kwh}, initial {battery.initial_energy_kwh}"
        )

    return len(violations) == 0, violations
