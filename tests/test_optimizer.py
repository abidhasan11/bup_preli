import pytest
from app.schemas.request import HourInput, BatterySpecs
from app.schemas.response import DirectiveInterpretation
from app.optimizer.solver import solve_energy_schedule


@pytest.fixture
def base_scenario():
    hours = []
    # Realistic 24-hour demand and solar profile
    demand_profile = [
        120, 110, 105, 100, 110, 130, 170, 220, 280, 310, 330, 350,
        340, 320, 300, 280, 260, 290, 330, 310, 260, 210, 170, 140
    ]
    solar_profile = [
        0, 0, 0, 0, 0, 0, 10, 40, 100, 180, 240, 280,
        300, 270, 220, 150, 80, 20, 0, 0, 0, 0, 0, 0
    ]
    tariff_profile = [
        6.5, 6.5, 6.0, 6.0, 6.0, 7.0, 8.0, 9.5, 11.0, 12.0, 12.0, 12.0,
        11.5, 11.0, 11.0, 10.5, 10.0, 12.5, 14.0, 14.0, 12.0, 10.0, 8.5, 7.0
    ]
    for h in range(24):
        hours.append(
            HourInput(
                hour=h,
                demand_kwh=float(demand_profile[h]),
                solar_kwh=float(solar_profile[h]),
                tariff_bdt_per_kwh=float(tariff_profile[h]),
            )
        )
    battery = BatterySpecs(
        capacity_kwh=500.0,
        initial_energy_kwh=200.0,
        minimum_energy_kwh=50.0,
        max_charge_kwh_per_hour=100.0,
        max_discharge_kwh_per_hour=100.0,
    )
    return hours, battery


def test_base_optimization(base_scenario):
    hours, battery = base_scenario
    res = solve_energy_schedule(hours, battery, applied_directives=[])
    assert res.success is True
    assert len(res.hourly_plan) == 24
    assert res.total_grid_kwh > 0
    assert res.total_cost_bdt > 0
    # Check end-of-day battery neutrality
    assert abs(res.hourly_plan[-1].battery_energy_after_kwh - battery.initial_energy_kwh) < 0.01


def test_solar_reduction(base_scenario):
    hours, battery = base_scenario
    directive = DirectiveInterpretation(
        note_index=0,
        applies=True,
        directive_type="solar_reduction",
        structured_adjustment={"hours": [13, 14], "factor": 0.2},
        explanation="Solar cut to 20%",
    )
    res = solve_energy_schedule(hours, battery, applied_directives=[directive])
    assert res.success is True
    # At hours 13 and 14, solar used must not exceed effective solar (270*0.2 = 54, 220*0.2 = 44)
    assert res.hourly_plan[13].solar_used_kwh <= 54.0 + 0.01
    assert res.hourly_plan[14].solar_used_kwh <= 44.0 + 0.01


def test_no_charge_window(base_scenario):
    hours, battery = base_scenario
    directive = DirectiveInterpretation(
        note_index=0,
        applies=True,
        directive_type="no_charge_window",
        structured_adjustment={"hours": [2, 3, 4]},
        explanation="No charging at night",
    )
    res = solve_energy_schedule(hours, battery, applied_directives=[directive])
    assert res.success is True
    for h in [2, 3, 4]:
        assert res.hourly_plan[h].battery_action != "charge"


def test_no_discharge_window(base_scenario):
    hours, battery = base_scenario
    directive = DirectiveInterpretation(
        note_index=0,
        applies=True,
        directive_type="no_discharge_window",
        structured_adjustment={"hours": [18, 19]},
        explanation="No discharge in evening",
    )
    res = solve_energy_schedule(hours, battery, applied_directives=[directive])
    assert res.success is True
    for h in [18, 19]:
        assert res.hourly_plan[h].battery_action != "discharge"


def test_minimum_battery_reserve(base_scenario):
    hours, battery = base_scenario
    directive = DirectiveInterpretation(
        note_index=0,
        applies=True,
        directive_type="minimum_battery_reserve",
        structured_adjustment={"hours": [18, 19, 20], "minimum_energy_kwh": 150.0},
        explanation="Keep 150 kWh in reserve",
    )
    res = solve_energy_schedule(hours, battery, applied_directives=[directive])
    assert res.success is True
    for h in [18, 19, 20]:
        assert res.hourly_plan[h].battery_energy_after_kwh >= 150.0 - 0.01
