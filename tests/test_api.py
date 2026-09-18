import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_root_dashboard():
    response = client.get("/")
    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]
    assert "GridWise LLM" in response.text


def test_full_scenario_api():
    payload = {
        "scenario_id": "BUP-TEST-SCENARIO-01",
        "operator_notes": [
            "Solar output will drop to about 20% from 1 PM to 3 PM.",
            "Do not charge the battery between 2 PM and 4 PM.",
            "The cafeteria menu changes tomorrow."
        ],
        "hours": [
            {"hour": 0, "demand_kwh": 120.0, "solar_kwh": 0.0, "tariff_bdt_per_kwh": 6.5},
            {"hour": 1, "demand_kwh": 110.0, "solar_kwh": 0.0, "tariff_bdt_per_kwh": 6.5},
            {"hour": 2, "demand_kwh": 105.0, "solar_kwh": 0.0, "tariff_bdt_per_kwh": 6.0},
            {"hour": 3, "demand_kwh": 100.0, "solar_kwh": 0.0, "tariff_bdt_per_kwh": 6.0},
            {"hour": 4, "demand_kwh": 110.0, "solar_kwh": 0.0, "tariff_bdt_per_kwh": 6.0},
            {"hour": 5, "demand_kwh": 130.0, "solar_kwh": 0.0, "tariff_bdt_per_kwh": 7.0},
            {"hour": 6, "demand_kwh": 170.0, "solar_kwh": 10.0, "tariff_bdt_per_kwh": 8.0},
            {"hour": 7, "demand_kwh": 220.0, "solar_kwh": 40.0, "tariff_bdt_per_kwh": 9.5},
            {"hour": 8, "demand_kwh": 280.0, "solar_kwh": 100.0, "tariff_bdt_per_kwh": 11.0},
            {"hour": 9, "demand_kwh": 310.0, "solar_kwh": 180.0, "tariff_bdt_per_kwh": 12.0},
            {"hour": 10, "demand_kwh": 330.0, "solar_kwh": 240.0, "tariff_bdt_per_kwh": 12.0},
            {"hour": 11, "demand_kwh": 350.0, "solar_kwh": 280.0, "tariff_bdt_per_kwh": 12.0},
            {"hour": 12, "demand_kwh": 340.0, "solar_kwh": 300.0, "tariff_bdt_per_kwh": 11.5},
            {"hour": 13, "demand_kwh": 320.0, "solar_kwh": 270.0, "tariff_bdt_per_kwh": 11.0},
            {"hour": 14, "demand_kwh": 300.0, "solar_kwh": 220.0, "tariff_bdt_per_kwh": 11.0},
            {"hour": 15, "demand_kwh": 280.0, "solar_kwh": 150.0, "tariff_bdt_per_kwh": 10.5},
            {"hour": 16, "demand_kwh": 260.0, "solar_kwh": 80.0, "tariff_bdt_per_kwh": 10.0},
            {"hour": 17, "demand_kwh": 290.0, "solar_kwh": 20.0, "tariff_bdt_per_kwh": 12.5},
            {"hour": 18, "demand_kwh": 330.0, "solar_kwh": 0.0, "tariff_bdt_per_kwh": 14.0},
            {"hour": 19, "demand_kwh": 310.0, "solar_kwh": 0.0, "tariff_bdt_per_kwh": 14.0},
            {"hour": 20, "demand_kwh": 260.0, "solar_kwh": 0.0, "tariff_bdt_per_kwh": 12.0},
            {"hour": 21, "demand_kwh": 210.0, "solar_kwh": 0.0, "tariff_bdt_per_kwh": 10.0},
            {"hour": 22, "demand_kwh": 170.0, "solar_kwh": 0.0, "tariff_bdt_per_kwh": 8.5},
            {"hour": 23, "demand_kwh": 140.0, "solar_kwh": 0.0, "tariff_bdt_per_kwh": 7.0}
        ],
        "battery": {
            "capacity_kwh": 500.0,
            "initial_energy_kwh": 200.0,
            "minimum_energy_kwh": 50.0,
            "max_charge_kwh_per_hour": 100.0,
            "max_discharge_kwh_per_hour": 100.0
        }
    }

    response = client.post("/optimize-energy", json=payload)
    assert response.status_code == 200
    data = response.json()

    assert data["scenario_id"] == "BUP-TEST-SCENARIO-01"
    assert len(data["directive_interpretation"]) == 3
    assert len(data["hourly_plan"]) == 24
    assert data["total_grid_kwh"] > 0
    assert data["total_cost_bdt"] > 0
    assert data["peak_grid_kwh"] > 0
    assert isinstance(data["plan_summary"], str)

    # Verify directive interpretations
    d0 = data["directive_interpretation"][0]
    assert d0["note_index"] == 0
    assert d0["directive_type"] == "solar_reduction"
    assert d0["applies"] is True
    assert d0["structured_adjustment"]["hours"] == [13, 14]

    d1 = data["directive_interpretation"][1]
    assert d1["note_index"] == 1
    assert d1["directive_type"] == "no_charge_window"
    assert d1["applies"] is True
    assert d1["structured_adjustment"]["hours"] == [14, 15]

    d2 = data["directive_interpretation"][2]
    assert d2["note_index"] == 2
    assert d2["directive_type"] == "no_op"
    assert d2["applies"] is False
    assert d2["structured_adjustment"] is None


def test_invalid_hours_count():
    # Only 23 hours instead of 24
    payload = {
        "scenario_id": "ERR-1",
        "operator_notes": ["Regular day"],
        "hours": [
            {"hour": h, "demand_kwh": 100.0, "solar_kwh": 0.0, "tariff_bdt_per_kwh": 7.0}
            for h in range(23)
        ],
        "battery": {
            "capacity_kwh": 500.0,
            "initial_energy_kwh": 200.0,
            "minimum_energy_kwh": 50.0,
            "max_charge_kwh_per_hour": 100.0,
            "max_discharge_kwh_per_hour": 100.0
        }
    }
    response = client.post("/optimize-energy", json=payload)
    assert response.status_code == 422
