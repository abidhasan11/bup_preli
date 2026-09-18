import pytest
from app.schemas.request import BatterySpecs
from app.guardrails.validator import validate_and_sanitize_directives, sanitize_hours


@pytest.fixture
def sample_battery():
    return BatterySpecs(
        capacity_kwh=500.0,
        initial_energy_kwh=200.0,
        minimum_energy_kwh=50.0,
        max_charge_kwh_per_hour=100.0,
        max_discharge_kwh_per_hour=100.0,
    )


def test_sanitize_hours():
    assert sanitize_hours([15, 14, 13]) == [13, 14, 15]
    assert sanitize_hours([23, 0, 10, 25, -1]) == [0, 10, 23]
    assert sanitize_hours("invalid") == []


def test_validate_valid_directives(sample_battery):
    raw = [
        {
            "note_index": 0,
            "applies": True,
            "directive_type": "solar_reduction",
            "structured_adjustment": {"hours": [14, 13], "factor": 0.2},
            "explanation": "Solar cleaning",
        },
        {
            "note_index": 1,
            "applies": False,
            "directive_type": "no_op",
            "structured_adjustment": None,
            "explanation": "Cafeteria update",
        },
    ]
    cleaned = validate_and_sanitize_directives(raw, expected_note_count=2, battery=sample_battery)
    assert len(cleaned) == 2
    assert cleaned[0].note_index == 0
    assert cleaned[0].applies is True
    assert cleaned[0].directive_type == "solar_reduction"
    assert cleaned[0].structured_adjustment["hours"] == [13, 14]
    assert cleaned[0].structured_adjustment["factor"] == 0.2

    assert cleaned[1].note_index == 1
    assert cleaned[1].applies is False
    assert cleaned[1].directive_type == "no_op"
    assert cleaned[1].structured_adjustment is None


def test_safe_failure_on_malformed_directives(sample_battery):
    raw = [
        # Note 0 has invalid directive type
        {
            "note_index": 0,
            "directive_type": "alien_invasion_mode",
            "structured_adjustment": {"hours": [10]},
        },
        # Note 1 has negative factor for solar_reduction
        {
            "note_index": 1,
            "directive_type": "solar_reduction",
            "structured_adjustment": {"hours": [12], "factor": -0.5},
        },
        # Note 2 is completely missing
    ]
    cleaned = validate_and_sanitize_directives(raw, expected_note_count=3, battery=sample_battery)
    assert len(cleaned) == 3
    for i in range(3):
        assert cleaned[i].note_index == i
        assert cleaned[i].directive_type == "no_op"
        assert cleaned[i].applies is False
        assert cleaned[i].structured_adjustment is None
