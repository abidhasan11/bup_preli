import pytest
from app.schemas.request import HourInput, BatterySpecs
from app.optimizer.solver import solve_energy_schedule
from app.verifier.replay import verify_and_replay_schedule


def test_replay_verification_on_optimal_plan():
    hours = [
        HourInput(hour=h, demand_kwh=100.0, solar_kwh=20.0, tariff_bdt_per_kwh=10.0)
        for h in range(24)
    ]
    battery = BatterySpecs(
        capacity_kwh=300.0,
        initial_energy_kwh=150.0,
        minimum_energy_kwh=50.0,
        max_charge_kwh_per_hour=50.0,
        max_discharge_kwh_per_hour=50.0,
    )
    res = solve_energy_schedule(hours, battery, applied_directives=[])
    assert res.success is True

    is_valid, violations = verify_and_replay_schedule(
        hourly_plan=res.hourly_plan,
        hours=hours,
        battery=battery,
        applied_directives=[],
    )
    assert is_valid is True
    assert len(violations) == 0


def test_replay_detects_broken_neutrality():
    hours = [
        HourInput(hour=h, demand_kwh=100.0, solar_kwh=20.0, tariff_bdt_per_kwh=10.0)
        for h in range(24)
    ]
    battery = BatterySpecs(
        capacity_kwh=300.0,
        initial_energy_kwh=150.0,
        minimum_energy_kwh=50.0,
        max_charge_kwh_per_hour=50.0,
        max_discharge_kwh_per_hour=50.0,
    )
    res = solve_energy_schedule(hours, battery, applied_directives=[])
    # Manually corrupt the final hour battery state to break neutrality
    corrupted_plan = [entry.model_copy() for entry in res.hourly_plan]
    corrupted_plan[-1].battery_energy_after_kwh = 50.0  # Should be 150.0

    is_valid, violations = verify_and_replay_schedule(
        hourly_plan=corrupted_plan,
        hours=hours,
        battery=battery,
        applied_directives=[],
    )
    assert is_valid is False
    assert any("neutrality violated" in v.lower() for v in violations)
