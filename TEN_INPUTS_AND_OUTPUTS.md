# GridWise LLM — 10 Verified Input & Output Benchmark Scenarios
## Canonical Test Suite for BUP CSE Fest 2026 Hackathon (Preliminaries)

> **Document Purpose**: This document provides **10 complete, diverse, and mathematically verified** end-to-end input-output scenarios for the Smart Campus Energy Optimization Challenge. Every scenario has been processed by the exact Linear Programming solver, checked by the 9-point judge replay engine, and verified to have **zero constraint violations**.

---

## Summary Benchmark Matrix (10 Scenarios)

| # | Scenario ID | Title | Key Directives Tested | Total Grid (kWh) | Total Cost (BDT) | Peak Grid (kWh) |
|---|---|---|---|:---:|:---:|:---:|
| 1 | `GRID-SCENARIO-01` | **Rooftop Solar Cleaning & Charging Lockout** | `solar_reduction`, `no_charge_window` | 4047.0 | 38862.00 | 366.0 |
| 2 | `GRID-SCENARIO-02` | **Evening Peak Safety Reserve Requirement** | `minimum_battery_reserve` | 3188.8 | 30312.05 | 239.0 |
| 3 | `GRID-SCENARIO-03` | **Morning Substation Maintenance & Charge Lockout** | `max_grid_window`, `no_charge_window` | 4121.2 | 39624.45 | 301.0 |
| 4 | `GRID-SCENARIO-04` | **Inverter Diagnostics No-Discharge Window** | `no_discharge_window` | 3560.5 | 32932.25 | 296.0 |
| 5 | `GRID-SCENARIO-05` | **Midday Solar Haze and Evening Grid Cap** | `solar_reduction`, `max_grid_window` | 4047.0 | 38787.00 | 306.0 |
| 6 | `GRID-SCENARIO-06` | **Midday No-Discharge & Night Safety Reserve** | `minimum_battery_reserve` | 4209.5 | 40858.50 | 296.0 |
| 7 | `GRID-SCENARIO-07` | **Triple Directive Compound Constraint Crunch** | `solar_reduction`, `no_charge_window`, `max_grid_window` | 4047.0 | 38902.00 | 366.0 |
| 8 | `GRID-SCENARIO-08` | **Overnight No-Discharge Protection** | `no_discharge_window` | 3655.0 | 35110.00 | 260.0 |
| 9 | `GRID-SCENARIO-09` | **Cloudburst Panel Washing & High Evening Reserve** | `solar_reduction`, `minimum_battery_reserve` | 3769.8 | 38162.64 | 290.0 |
| 10 | `GRID-SCENARIO-10` | **All-Distractors Pure Economic Dispatch** | *None (All No-Op)* | 3655.0 | 34475.00 | 280.0 |

---

## Scenario 01: Rooftop Solar Cleaning & Charging Lockout (`GRID-SCENARIO-01`)

**Description**: Tests solar reduction during peak sunlight alongside afternoon battery charging prohibition and a distractor note.

### Operational Notes:
- *"Solar output will drop to about 20% from 1 PM to 3 PM."*
- *"Do not charge the battery between 2 PM and 4 PM."*
- *"The cafeteria menu changes tomorrow."*

### Active Directives Applied:
- **`solar_reduction`**: `{"hours": [13, 14], "factor": 0.2}` — *Solar availability reduced to 20% between 1 PM and 3 PM.*
- **`no_charge_window`**: `{"hours": [14, 15]}` — *Battery charging prohibited between 2 PM and 4 PM.*

### Key Financial & Grid Results:
- **Total Grid Electricity Imported**: `4047.00 kWh`
- **Total Electricity Cost**: `38862.00 BDT`
- **Peak Hourly Grid Load**: `366.00 kWh`
- **Battery Capacity & State**: Capacity = `500.0 kWh`, Initial/Final SoC = `200.0 kWh` *(End-of-day neutrality verified)*

<details>
<summary><strong>Click to expand Full HTTP Request JSON (POST /optimize-energy)</strong></summary>

```json
{
  "scenario_id": "GRID-SCENARIO-01",
  "operator_notes": [
    "Solar output will drop to about 20% from 1 PM to 3 PM.",
    "Do not charge the battery between 2 PM and 4 PM.",
    "The cafeteria menu changes tomorrow."
  ],
  "hours": [
    {
      "hour": 0,
      "demand_kwh": 120.0,
      "solar_kwh": 0.0,
      "tariff_bdt_per_kwh": 6.5
    },
    {
      "hour": 1,
      "demand_kwh": 110.0,
      "solar_kwh": 0.0,
      "tariff_bdt_per_kwh": 6.5
    },
    {
      "hour": 2,
      "demand_kwh": 105.0,
      "solar_kwh": 0.0,
      "tariff_bdt_per_kwh": 6.0
    },
    {
      "hour": 3,
      "demand_kwh": 100.0,
      "solar_kwh": 0.0,
      "tariff_bdt_per_kwh": 6.0
    },
    {
      "hour": 4,
      "demand_kwh": 110.0,
      "solar_kwh": 0.0,
      "tariff_bdt_per_kwh": 6.0
    },
    {
      "hour": 5,
      "demand_kwh": 130.0,
      "solar_kwh": 0.0,
      "tariff_bdt_per_kwh": 7.0
    },
    {
      "hour": 6,
      "demand_kwh": 170.0,
      "solar_kwh": 10.0,
      "tariff_bdt_per_kwh": 8.0
    },
    {
      "hour": 7,
      "demand_kwh": 220.0,
      "solar_kwh": 40.0,
      "tariff_bdt_per_kwh": 9.5
    },
    {
      "hour": 8,
      "demand_kwh": 280.0,
      "solar_kwh": 100.0,
      "tariff_bdt_per_kwh": 11.0
    },
    {
      "hour": 9,
      "demand_kwh": 310.0,
      "solar_kwh": 180.0,
      "tariff_bdt_per_kwh": 12.0
    },
    {
      "hour": 10,
      "demand_kwh": 330.0,
      "solar_kwh": 240.0,
      "tariff_bdt_per_kwh": 12.0
    },
    {
      "hour": 11,
      "demand_kwh": 350.0,
      "solar_kwh": 280.0,
      "tariff_bdt_per_kwh": 12.0
    },
    {
      "hour": 12,
      "demand_kwh": 340.0,
      "solar_kwh": 300.0,
      "tariff_bdt_per_kwh": 11.5
    },
    {
      "hour": 13,
      "demand_kwh": 320.0,
      "solar_kwh": 270.0,
      "tariff_bdt_per_kwh": 11.0
    },
    {
      "hour": 14,
      "demand_kwh": 300.0,
      "solar_kwh": 220.0,
      "tariff_bdt_per_kwh": 11.0
    },
    {
      "hour": 15,
      "demand_kwh": 280.0,
      "solar_kwh": 150.0,
      "tariff_bdt_per_kwh": 10.5
    },
    {
      "hour": 16,
      "demand_kwh": 260.0,
      "solar_kwh": 80.0,
      "tariff_bdt_per_kwh": 10.0
    },
    {
      "hour": 17,
      "demand_kwh": 290.0,
      "solar_kwh": 20.0,
      "tariff_bdt_per_kwh": 12.5
    },
    {
      "hour": 18,
      "demand_kwh": 330.0,
      "solar_kwh": 0.0,
      "tariff_bdt_per_kwh": 14.0
    },
    {
      "hour": 19,
      "demand_kwh": 310.0,
      "solar_kwh": 0.0,
      "tariff_bdt_per_kwh": 14.0
    },
    {
      "hour": 20,
      "demand_kwh": 260.0,
      "solar_kwh": 0.0,
      "tariff_bdt_per_kwh": 12.0
    },
    {
      "hour": 21,
      "demand_kwh": 210.0,
      "solar_kwh": 0.0,
      "tariff_bdt_per_kwh": 10.0
    },
    {
      "hour": 22,
      "demand_kwh": 170.0,
      "solar_kwh": 0.0,
      "tariff_bdt_per_kwh": 8.5
    },
    {
      "hour": 23,
      "demand_kwh": 140.0,
      "solar_kwh": 0.0,
      "tariff_bdt_per_kwh": 7.0
    }
  ],
  "battery": {
    "capacity_kwh": 500.0,
    "initial_energy_kwh": 200.0,
    "minimum_energy_kwh": 50.0,
    "max_charge_kwh_per_hour": 100.0,
    "max_discharge_kwh_per_hour": 100.0
  }
}
```
</details>

<details open>
<summary><strong>Full HTTP 200 Response JSON</strong></summary>

```json
{
  "scenario_id": "GRID-SCENARIO-01",
  "directive_interpretation": [
    {
      "note_index": 0,
      "applies": true,
      "directive_type": "solar_reduction",
      "structured_adjustment": {
        "hours": [
          13,
          14
        ],
        "factor": 0.2
      },
      "explanation": "Solar availability reduced to 20% between 1 PM and 3 PM."
    },
    {
      "note_index": 1,
      "applies": true,
      "directive_type": "no_charge_window",
      "structured_adjustment": {
        "hours": [
          14,
          15
        ]
      },
      "explanation": "Battery charging prohibited between 2 PM and 4 PM."
    },
    {
      "note_index": 2,
      "applies": false,
      "directive_type": "no_op",
      "structured_adjustment": null,
      "explanation": "This note does not affect today's energy schedule."
    }
  ],
  "hourly_plan": [
    {
      "hour": 0,
      "grid_kwh": 120.0,
      "solar_used_kwh": 0.0,
      "battery_action": "idle",
      "battery_kwh": 0.0,
      "battery_energy_after_kwh": 200.0
    },
    {
      "hour": 1,
      "grid_kwh": 110.0,
      "solar_used_kwh": 0.0,
      "battery_action": "idle",
      "battery_kwh": 0.0,
      "battery_energy_after_kwh": 200.0
    },
    {
      "hour": 2,
      "grid_kwh": 205.0,
      "solar_used_kwh": 0.0,
      "battery_action": "charge",
      "battery_kwh": 100.0,
      "battery_energy_after_kwh": 300.0
    },
    {
      "hour": 3,
      "grid_kwh": 200.0,
      "solar_used_kwh": 0.0,
      "battery_action": "charge",
      "battery_kwh": 100.0,
      "battery_energy_after_kwh": 400.0
    },
    {
      "hour": 4,
      "grid_kwh": 210.0,
      "solar_used_kwh": 0.0,
      "battery_action": "charge",
      "battery_kwh": 100.0,
      "battery_energy_after_kwh": 500.0
    },
    {
      "hour": 5,
      "grid_kwh": 130.0,
      "solar_used_kwh": 0.0,
      "battery_action": "idle",
      "battery_kwh": 0.0,
      "battery_energy_after_kwh": 500.0
    },
    {
      "hour": 6,
      "grid_kwh": 160.0,
      "solar_used_kwh": 10.0,
      "battery_action": "idle",
      "battery_kwh": 0.0,
      "battery_energy_after_kwh": 500.0
    },
    {
      "hour": 7,
      "grid_kwh": 180.0,
      "solar_used_kwh": 40.0,
      "battery_action": "idle",
      "battery_kwh": 0.0,
      "battery_energy_after_kwh": 500.0
    },
    {
      "hour": 8,
      "grid_kwh": 180.0,
      "solar_used_kwh": 100.0,
      "battery_action": "idle",
      "battery_kwh": 0.0,
      "battery_energy_after_kwh": 500.0
    },
    {
      "hour": 9,
      "grid_kwh": 30.0,
      "solar_used_kwh": 180.0,
      "battery_action": "discharge",
      "battery_kwh": 100.0,
      "battery_energy_after_kwh": 400.0
    },
    {
      "hour": 10,
      "grid_kwh": 0.0,
      "solar_used_kwh": 240.0,
      "battery_action": "discharge",
      "battery_kwh": 90.0,
      "battery_energy_after_kwh": 310.0
    },
    {
      "hour": 11,
      "grid_kwh": 0.0,
      "solar_used_kwh": 280.0,
      "battery_action": "discharge",
      "battery_kwh": 70.0,
      "battery_energy_after_kwh": 240.0
    },
    {
      "hour": 12,
      "grid_kwh": 50.0,
      "solar_used_kwh": 300.0,
      "battery_action": "charge",
      "battery_kwh": 10.0,
      "battery_energy_after_kwh": 250.0
    },
    {
      "hour": 13,
      "grid_kwh": 366.0,
      "solar_used_kwh": 54.0,
      "battery_action": "charge",
      "battery_kwh": 100.0,
      "battery_energy_after_kwh": 350.0
    },
    {
      "hour": 14,
      "grid_kwh": 256.0,
      "solar_used_kwh": 44.0,
      "battery_action": "idle",
      "battery_kwh": 0.0,
      "battery_energy_after_kwh": 350.0
    },
    {
      "hour": 15,
      "grid_kwh": 130.0,
      "solar_used_kwh": 150.0,
      "battery_action": "idle",
      "battery_kwh": 0.0,
      "battery_energy_after_kwh": 350.0
    },
    {
      "hour": 16,
      "grid_kwh": 280.0,
      "solar_used_kwh": 80.0,
      "battery_action": "charge",
      "battery_kwh": 100.0,
      "battery_energy_after_kwh": 450.0
    },
    {
      "hour": 17,
      "grid_kwh": 170.0,
      "solar_used_kwh": 20.0,
      "battery_action": "discharge",
      "battery_kwh": 100.0,
      "battery_energy_after_kwh": 350.0
    },
    {
      "hour": 18,
      "grid_kwh": 230.0,
      "solar_used_kwh": 0.0,
      "battery_action": "discharge",
      "battery_kwh": 100.0,
      "battery_energy_after_kwh": 250.0
    },
    {
      "hour": 19,
      "grid_kwh": 210.0,
      "solar_used_kwh": 0.0,
      "battery_action": "discharge",
      "battery_kwh": 100.0,
      "battery_energy_after_kwh": 150.0
    },
    {
      "hour": 20,
      "grid_kwh": 160.0,
      "solar_used_kwh": 0.0,
      "battery_action": "discharge",
      "battery_kwh": 100.0,
      "battery_energy_after_kwh": 50.0
    },
    {
      "hour": 21,
      "grid_kwh": 210.0,
      "solar_used_kwh": 0.0,
      "battery_action": "idle",
      "battery_kwh": 0.0,
      "battery_energy_after_kwh": 50.0
    },
    {
      "hour": 22,
      "grid_kwh": 220.0,
      "solar_used_kwh": 0.0,
      "battery_action": "charge",
      "battery_kwh": 50.0,
      "battery_energy_after_kwh": 100.0
    },
    {
      "hour": 23,
      "grid_kwh": 240.0,
      "solar_used_kwh": 0.0,
      "battery_action": "charge",
      "battery_kwh": 100.0,
      "battery_energy_after_kwh": 200.0
    }
  ],
  "total_grid_kwh": 4047.0,
  "total_cost_bdt": 38862.0,
  "peak_grid_kwh": 366.0,
  "plan_summary": "Optimized schedule for GRID-SCENARIO-01. Applied 2 active directive(s). Grid import: 4047.00 kWh, Total cost: 38862.00 BDT, Peak load: 366.00 kWh."
}
```
</details>

---

## Scenario 02: Evening Peak Safety Reserve Requirement (`GRID-SCENARIO-02`)

**Description**: Tests dynamic battery reserve elevation during high-tariff evening hours to guarantee emergency campus resilience.

### Operational Notes:
- *"Keep at least 150 kWh in reserve from 6 PM until 9 PM."*
- *"The campus shuttle schedule will be updated next Monday."*

### Active Directives Applied:
- **`minimum_battery_reserve`**: `{"hours": [18, 19, 20], "minimum_energy_kwh": 150.0}` — *Keep at least 150 kWh in reserve between 6 PM and 9 PM.*

### Key Financial & Grid Results:
- **Total Grid Electricity Imported**: `3188.80 kWh`
- **Total Electricity Cost**: `30312.05 BDT`
- **Peak Hourly Grid Load**: `239.00 kWh`
- **Battery Capacity & State**: Capacity = `400.0 kWh`, Initial/Final SoC = `150.0 kWh` *(End-of-day neutrality verified)*

<details>
<summary><strong>Click to expand Full HTTP Request JSON (POST /optimize-energy)</strong></summary>

```json
{
  "scenario_id": "GRID-SCENARIO-02",
  "operator_notes": [
    "Keep at least 150 kWh in reserve from 6 PM until 9 PM.",
    "The campus shuttle schedule will be updated next Monday."
  ],
  "hours": [
    {
      "hour": 0,
      "demand_kwh": 114.0,
      "solar_kwh": 0.0,
      "tariff_bdt_per_kwh": 6.5
    },
    {
      "hour": 1,
      "demand_kwh": 104.5,
      "solar_kwh": 0.0,
      "tariff_bdt_per_kwh": 6.5
    },
    {
      "hour": 2,
      "demand_kwh": 99.8,
      "solar_kwh": 0.0,
      "tariff_bdt_per_kwh": 6.0
    },
    {
      "hour": 3,
      "demand_kwh": 95.0,
      "solar_kwh": 0.0,
      "tariff_bdt_per_kwh": 6.0
    },
    {
      "hour": 4,
      "demand_kwh": 104.5,
      "solar_kwh": 0.0,
      "tariff_bdt_per_kwh": 6.0
    },
    {
      "hour": 5,
      "demand_kwh": 123.5,
      "solar_kwh": 0.0,
      "tariff_bdt_per_kwh": 7.0
    },
    {
      "hour": 6,
      "demand_kwh": 161.5,
      "solar_kwh": 11.0,
      "tariff_bdt_per_kwh": 8.0
    },
    {
      "hour": 7,
      "demand_kwh": 209.0,
      "solar_kwh": 44.0,
      "tariff_bdt_per_kwh": 9.5
    },
    {
      "hour": 8,
      "demand_kwh": 266.0,
      "solar_kwh": 110.0,
      "tariff_bdt_per_kwh": 11.0
    },
    {
      "hour": 9,
      "demand_kwh": 294.5,
      "solar_kwh": 198.0,
      "tariff_bdt_per_kwh": 12.0
    },
    {
      "hour": 10,
      "demand_kwh": 313.5,
      "solar_kwh": 264.0,
      "tariff_bdt_per_kwh": 12.0
    },
    {
      "hour": 11,
      "demand_kwh": 332.5,
      "solar_kwh": 308.0,
      "tariff_bdt_per_kwh": 12.0
    },
    {
      "hour": 12,
      "demand_kwh": 323.0,
      "solar_kwh": 330.0,
      "tariff_bdt_per_kwh": 11.5
    },
    {
      "hour": 13,
      "demand_kwh": 304.0,
      "solar_kwh": 297.0,
      "tariff_bdt_per_kwh": 11.0
    },
    {
      "hour": 14,
      "demand_kwh": 285.0,
      "solar_kwh": 242.0,
      "tariff_bdt_per_kwh": 11.0
    },
    {
      "hour": 15,
      "demand_kwh": 266.0,
      "solar_kwh": 165.0,
      "tariff_bdt_per_kwh": 10.5
    },
    {
      "hour": 16,
      "demand_kwh": 247.0,
      "solar_kwh": 88.0,
      "tariff_bdt_per_kwh": 10.0
    },
    {
      "hour": 17,
      "demand_kwh": 275.5,
      "solar_kwh": 22.0,
      "tariff_bdt_per_kwh": 12.5
    },
    {
      "hour": 18,
      "demand_kwh": 313.5,
      "solar_kwh": 0.0,
      "tariff_bdt_per_kwh": 14.0
    },
    {
      "hour": 19,
      "demand_kwh": 294.5,
      "solar_kwh": 0.0,
      "tariff_bdt_per_kwh": 14.0
    },
    {
      "hour": 20,
      "demand_kwh": 247.0,
      "solar_kwh": 0.0,
      "tariff_bdt_per_kwh": 12.0
    },
    {
      "hour": 21,
      "demand_kwh": 199.5,
      "solar_kwh": 0.0,
      "tariff_bdt_per_kwh": 10.0
    },
    {
      "hour": 22,
      "demand_kwh": 161.5,
      "solar_kwh": 0.0,
      "tariff_bdt_per_kwh": 8.5
    },
    {
      "hour": 23,
      "demand_kwh": 133.0,
      "solar_kwh": 0.0,
      "tariff_bdt_per_kwh": 7.0
    }
  ],
  "battery": {
    "capacity_kwh": 400.0,
    "initial_energy_kwh": 150.0,
    "minimum_energy_kwh": 40.0,
    "max_charge_kwh_per_hour": 80.0,
    "max_discharge_kwh_per_hour": 80.0
  }
}
```
</details>

<details open>
<summary><strong>Full HTTP 200 Response JSON</strong></summary>

```json
{
  "scenario_id": "GRID-SCENARIO-02",
  "directive_interpretation": [
    {
      "note_index": 0,
      "applies": true,
      "directive_type": "minimum_battery_reserve",
      "structured_adjustment": {
        "hours": [
          18,
          19,
          20
        ],
        "minimum_energy_kwh": 150.0
      },
      "explanation": "Keep at least 150 kWh in reserve between 6 PM and 9 PM."
    },
    {
      "note_index": 1,
      "applies": false,
      "directive_type": "no_op",
      "structured_adjustment": null,
      "explanation": "This note does not affect today's energy schedule."
    }
  ],
  "hourly_plan": [
    {
      "hour": 0,
      "grid_kwh": 114.0,
      "solar_used_kwh": 0.0,
      "battery_action": "idle",
      "battery_kwh": 0.0,
      "battery_energy_after_kwh": 150.0
    },
    {
      "hour": 1,
      "grid_kwh": 114.5,
      "solar_used_kwh": 0.0,
      "battery_action": "charge",
      "battery_kwh": 10.0,
      "battery_energy_after_kwh": 160.0
    },
    {
      "hour": 2,
      "grid_kwh": 179.8,
      "solar_used_kwh": 0.0,
      "battery_action": "charge",
      "battery_kwh": 80.0,
      "battery_energy_after_kwh": 240.0
    },
    {
      "hour": 3,
      "grid_kwh": 175.0,
      "solar_used_kwh": 0.0,
      "battery_action": "charge",
      "battery_kwh": 80.0,
      "battery_energy_after_kwh": 320.0
    },
    {
      "hour": 4,
      "grid_kwh": 184.5,
      "solar_used_kwh": 0.0,
      "battery_action": "charge",
      "battery_kwh": 80.0,
      "battery_energy_after_kwh": 400.0
    },
    {
      "hour": 5,
      "grid_kwh": 123.5,
      "solar_used_kwh": 0.0,
      "battery_action": "idle",
      "battery_kwh": 0.0,
      "battery_energy_after_kwh": 400.0
    },
    {
      "hour": 6,
      "grid_kwh": 150.5,
      "solar_used_kwh": 11.0,
      "battery_action": "idle",
      "battery_kwh": 0.0,
      "battery_energy_after_kwh": 400.0
    },
    {
      "hour": 7,
      "grid_kwh": 165.0,
      "solar_used_kwh": 44.0,
      "battery_action": "idle",
      "battery_kwh": 0.0,
      "battery_energy_after_kwh": 400.0
    },
    {
      "hour": 8,
      "grid_kwh": 150.0,
      "solar_used_kwh": 110.0,
      "battery_action": "discharge",
      "battery_kwh": 6.0,
      "battery_energy_after_kwh": 394.0
    },
    {
      "hour": 9,
      "grid_kwh": 16.5,
      "solar_used_kwh": 198.0,
      "battery_action": "discharge",
      "battery_kwh": 80.0,
      "battery_energy_after_kwh": 314.0
    },
    {
      "hour": 10,
      "grid_kwh": 0.0,
      "solar_used_kwh": 264.0,
      "battery_action": "discharge",
      "battery_kwh": 49.5,
      "battery_energy_after_kwh": 264.5
    },
    {
      "hour": 11,
      "grid_kwh": 0.0,
      "solar_used_kwh": 308.0,
      "battery_action": "discharge",
      "battery_kwh": 24.5,
      "battery_energy_after_kwh": 240.0
    },
    {
      "hour": 12,
      "grid_kwh": 0.0,
      "solar_used_kwh": 330.0,
      "battery_action": "charge",
      "battery_kwh": 7.0,
      "battery_energy_after_kwh": 247.0
    },
    {
      "hour": 13,
      "grid_kwh": 0.0,
      "solar_used_kwh": 297.0,
      "battery_action": "discharge",
      "battery_kwh": 7.0,
      "battery_energy_after_kwh": 240.0
    },
    {
      "hour": 14,
      "grid_kwh": 43.0,
      "solar_used_kwh": 242.0,
      "battery_action": "idle",
      "battery_kwh": 0.0,
      "battery_energy_after_kwh": 240.0
    },
    {
      "hour": 15,
      "grid_kwh": 181.0,
      "solar_used_kwh": 165.0,
      "battery_action": "charge",
      "battery_kwh": 80.0,
      "battery_energy_after_kwh": 320.0
    },
    {
      "hour": 16,
      "grid_kwh": 239.0,
      "solar_used_kwh": 88.0,
      "battery_action": "charge",
      "battery_kwh": 80.0,
      "battery_energy_after_kwh": 400.0
    },
    {
      "hour": 17,
      "grid_kwh": 173.5,
      "solar_used_kwh": 22.0,
      "battery_action": "discharge",
      "battery_kwh": 80.0,
      "battery_energy_after_kwh": 320.0
    },
    {
      "hour": 18,
      "grid_kwh": 233.5,
      "solar_used_kwh": 0.0,
      "battery_action": "discharge",
      "battery_kwh": 80.0,
      "battery_energy_after_kwh": 240.0
    },
    {
      "hour": 19,
      "grid_kwh": 214.5,
      "solar_used_kwh": 0.0,
      "battery_action": "discharge",
      "battery_kwh": 80.0,
      "battery_energy_after_kwh": 160.0
    },
    {
      "hour": 20,
      "grid_kwh": 237.0,
      "solar_used_kwh": 0.0,
      "battery_action": "discharge",
      "battery_kwh": 10.0,
      "battery_energy_after_kwh": 150.0
    },
    {
      "hour": 21,
      "grid_kwh": 119.5,
      "solar_used_kwh": 0.0,
      "battery_action": "discharge",
      "battery_kwh": 80.0,
      "battery_energy_after_kwh": 70.0
    },
    {
      "hour": 22,
      "grid_kwh": 161.5,
      "solar_used_kwh": 0.0,
      "battery_action": "idle",
      "battery_kwh": 0.0,
      "battery_energy_after_kwh": 70.0
    },
    {
      "hour": 23,
      "grid_kwh": 213.0,
      "solar_used_kwh": 0.0,
      "battery_action": "charge",
      "battery_kwh": 80.0,
      "battery_energy_after_kwh": 150.0
    }
  ],
  "total_grid_kwh": 3188.8,
  "total_cost_bdt": 30312.05,
  "peak_grid_kwh": 239.0,
  "plan_summary": "Optimized schedule for GRID-SCENARIO-02. Applied 1 active directive(s). Grid import: 3188.80 kWh, Total cost: 30312.05 BDT, Peak load: 239.00 kWh."
}
```
</details>

---

## Scenario 03: Morning Substation Maintenance & Charge Lockout (`GRID-SCENARIO-03`)

**Description**: Tests strict grid power import ceiling alongside early-morning charge blocking to prevent grid overload.

### Operational Notes:
- *"Grid import capped at 120 kWh between 8 AM and 11 AM due to substation maintenance."*
- *"Do not charge the battery between 5 AM and 7 AM."*

### Active Directives Applied:
- **`max_grid_window`**: `{"hours": [8, 9, 10], "max_grid_kwh": 120.0}` — *Grid import capped at 120 kWh between 8 AM and 11 AM.*
- **`no_charge_window`**: `{"hours": [5, 6]}` — *Battery charging prohibited between 5 AM and 7 AM.*

### Key Financial & Grid Results:
- **Total Grid Electricity Imported**: `4121.20 kWh`
- **Total Electricity Cost**: `39624.45 BDT`
- **Peak Hourly Grid Load**: `301.00 kWh`
- **Battery Capacity & State**: Capacity = `500.0 kWh`, Initial/Final SoC = `250.0 kWh` *(End-of-day neutrality verified)*

<details>
<summary><strong>Click to expand Full HTTP Request JSON (POST /optimize-energy)</strong></summary>

```json
{
  "scenario_id": "GRID-SCENARIO-03",
  "operator_notes": [
    "Grid import capped at 120 kWh between 8 AM and 11 AM due to substation maintenance.",
    "Do not charge the battery between 5 AM and 7 AM."
  ],
  "hours": [
    {
      "hour": 0,
      "demand_kwh": 126.0,
      "solar_kwh": 0.0,
      "tariff_bdt_per_kwh": 6.5
    },
    {
      "hour": 1,
      "demand_kwh": 115.5,
      "solar_kwh": 0.0,
      "tariff_bdt_per_kwh": 6.5
    },
    {
      "hour": 2,
      "demand_kwh": 110.2,
      "solar_kwh": 0.0,
      "tariff_bdt_per_kwh": 6.0
    },
    {
      "hour": 3,
      "demand_kwh": 105.0,
      "solar_kwh": 0.0,
      "tariff_bdt_per_kwh": 6.0
    },
    {
      "hour": 4,
      "demand_kwh": 115.5,
      "solar_kwh": 0.0,
      "tariff_bdt_per_kwh": 6.0
    },
    {
      "hour": 5,
      "demand_kwh": 136.5,
      "solar_kwh": 0.0,
      "tariff_bdt_per_kwh": 7.0
    },
    {
      "hour": 6,
      "demand_kwh": 178.5,
      "solar_kwh": 9.0,
      "tariff_bdt_per_kwh": 8.0
    },
    {
      "hour": 7,
      "demand_kwh": 231.0,
      "solar_kwh": 36.0,
      "tariff_bdt_per_kwh": 9.5
    },
    {
      "hour": 8,
      "demand_kwh": 294.0,
      "solar_kwh": 90.0,
      "tariff_bdt_per_kwh": 11.0
    },
    {
      "hour": 9,
      "demand_kwh": 325.5,
      "solar_kwh": 162.0,
      "tariff_bdt_per_kwh": 12.0
    },
    {
      "hour": 10,
      "demand_kwh": 346.5,
      "solar_kwh": 216.0,
      "tariff_bdt_per_kwh": 12.0
    },
    {
      "hour": 11,
      "demand_kwh": 367.5,
      "solar_kwh": 252.0,
      "tariff_bdt_per_kwh": 12.0
    },
    {
      "hour": 12,
      "demand_kwh": 357.0,
      "solar_kwh": 270.0,
      "tariff_bdt_per_kwh": 11.5
    },
    {
      "hour": 13,
      "demand_kwh": 336.0,
      "solar_kwh": 243.0,
      "tariff_bdt_per_kwh": 11.0
    },
    {
      "hour": 14,
      "demand_kwh": 315.0,
      "solar_kwh": 198.0,
      "tariff_bdt_per_kwh": 11.0
    },
    {
      "hour": 15,
      "demand_kwh": 294.0,
      "solar_kwh": 135.0,
      "tariff_bdt_per_kwh": 10.5
    },
    {
      "hour": 16,
      "demand_kwh": 273.0,
      "solar_kwh": 72.0,
      "tariff_bdt_per_kwh": 10.0
    },
    {
      "hour": 17,
      "demand_kwh": 304.5,
      "solar_kwh": 18.0,
      "tariff_bdt_per_kwh": 12.5
    },
    {
      "hour": 18,
      "demand_kwh": 346.5,
      "solar_kwh": 0.0,
      "tariff_bdt_per_kwh": 14.0
    },
    {
      "hour": 19,
      "demand_kwh": 325.5,
      "solar_kwh": 0.0,
      "tariff_bdt_per_kwh": 14.0
    },
    {
      "hour": 20,
      "demand_kwh": 273.0,
      "solar_kwh": 0.0,
      "tariff_bdt_per_kwh": 12.0
    },
    {
      "hour": 21,
      "demand_kwh": 220.5,
      "solar_kwh": 0.0,
      "tariff_bdt_per_kwh": 10.0
    },
    {
      "hour": 22,
      "demand_kwh": 178.5,
      "solar_kwh": 0.0,
      "tariff_bdt_per_kwh": 8.5
    },
    {
      "hour": 23,
      "demand_kwh": 147.0,
      "solar_kwh": 0.0,
      "tariff_bdt_per_kwh": 7.0
    }
  ],
  "battery": {
    "capacity_kwh": 500.0,
    "initial_energy_kwh": 250.0,
    "minimum_energy_kwh": 50.0,
    "max_charge_kwh_per_hour": 100.0,
    "max_discharge_kwh_per_hour": 100.0
  }
}
```
</details>

<details open>
<summary><strong>Full HTTP 200 Response JSON</strong></summary>

```json
{
  "scenario_id": "GRID-SCENARIO-03",
  "directive_interpretation": [
    {
      "note_index": 0,
      "applies": true,
      "directive_type": "max_grid_window",
      "structured_adjustment": {
        "hours": [
          8,
          9,
          10
        ],
        "max_grid_kwh": 120.0
      },
      "explanation": "Grid import capped at 120 kWh between 8 AM and 11 AM."
    },
    {
      "note_index": 1,
      "applies": true,
      "directive_type": "no_charge_window",
      "structured_adjustment": {
        "hours": [
          5,
          6
        ]
      },
      "explanation": "Battery charging prohibited between 5 AM and 7 AM."
    }
  ],
  "hourly_plan": [
    {
      "hour": 0,
      "grid_kwh": 126.0,
      "solar_used_kwh": 0.0,
      "battery_action": "idle",
      "battery_kwh": 0.0,
      "battery_energy_after_kwh": 250.0
    },
    {
      "hour": 1,
      "grid_kwh": 65.5,
      "solar_used_kwh": 0.0,
      "battery_action": "discharge",
      "battery_kwh": 50.0,
      "battery_energy_after_kwh": 200.0
    },
    {
      "hour": 2,
      "grid_kwh": 210.2,
      "solar_used_kwh": 0.0,
      "battery_action": "charge",
      "battery_kwh": 100.0,
      "battery_energy_after_kwh": 300.0
    },
    {
      "hour": 3,
      "grid_kwh": 205.0,
      "solar_used_kwh": 0.0,
      "battery_action": "charge",
      "battery_kwh": 100.0,
      "battery_energy_after_kwh": 400.0
    },
    {
      "hour": 4,
      "grid_kwh": 215.5,
      "solar_used_kwh": 0.0,
      "battery_action": "charge",
      "battery_kwh": 100.0,
      "battery_energy_after_kwh": 500.0
    },
    {
      "hour": 5,
      "grid_kwh": 136.5,
      "solar_used_kwh": 0.0,
      "battery_action": "idle",
      "battery_kwh": 0.0,
      "battery_energy_after_kwh": 500.0
    },
    {
      "hour": 6,
      "grid_kwh": 169.5,
      "solar_used_kwh": 9.0,
      "battery_action": "idle",
      "battery_kwh": 0.0,
      "battery_energy_after_kwh": 500.0
    },
    {
      "hour": 7,
      "grid_kwh": 195.0,
      "solar_used_kwh": 36.0,
      "battery_action": "idle",
      "battery_kwh": 0.0,
      "battery_energy_after_kwh": 500.0
    },
    {
      "hour": 8,
      "grid_kwh": 120.0,
      "solar_used_kwh": 90.0,
      "battery_action": "discharge",
      "battery_kwh": 84.0,
      "battery_energy_after_kwh": 416.0
    },
    {
      "hour": 9,
      "grid_kwh": 63.5,
      "solar_used_kwh": 162.0,
      "battery_action": "discharge",
      "battery_kwh": 100.0,
      "battery_energy_after_kwh": 316.0
    },
    {
      "hour": 10,
      "grid_kwh": 30.5,
      "solar_used_kwh": 216.0,
      "battery_action": "discharge",
      "battery_kwh": 100.0,
      "battery_energy_after_kwh": 216.0
    },
    {
      "hour": 11,
      "grid_kwh": 15.5,
      "solar_used_kwh": 252.0,
      "battery_action": "discharge",
      "battery_kwh": 100.0,
      "battery_energy_after_kwh": 116.0
    },
    {
      "hour": 12,
      "grid_kwh": 21.0,
      "solar_used_kwh": 270.0,
      "battery_action": "discharge",
      "battery_kwh": 66.0,
      "battery_energy_after_kwh": 50.0
    },
    {
      "hour": 13,
      "grid_kwh": 193.0,
      "solar_used_kwh": 243.0,
      "battery_action": "charge",
      "battery_kwh": 100.0,
      "battery_energy_after_kwh": 150.0
    },
    {
      "hour": 14,
      "grid_kwh": 217.0,
      "solar_used_kwh": 198.0,
      "battery_action": "charge",
      "battery_kwh": 100.0,
      "battery_energy_after_kwh": 250.0
    },
    {
      "hour": 15,
      "grid_kwh": 259.0,
      "solar_used_kwh": 135.0,
      "battery_action": "charge",
      "battery_kwh": 100.0,
      "battery_energy_after_kwh": 350.0
    },
    {
      "hour": 16,
      "grid_kwh": 301.0,
      "solar_used_kwh": 72.0,
      "battery_action": "charge",
      "battery_kwh": 100.0,
      "battery_energy_after_kwh": 450.0
    },
    {
      "hour": 17,
      "grid_kwh": 186.5,
      "solar_used_kwh": 18.0,
      "battery_action": "discharge",
      "battery_kwh": 100.0,
      "battery_energy_after_kwh": 350.0
    },
    {
      "hour": 18,
      "grid_kwh": 246.5,
      "solar_used_kwh": 0.0,
      "battery_action": "discharge",
      "battery_kwh": 100.0,
      "battery_energy_after_kwh": 250.0
    },
    {
      "hour": 19,
      "grid_kwh": 225.5,
      "solar_used_kwh": 0.0,
      "battery_action": "discharge",
      "battery_kwh": 100.0,
      "battery_energy_after_kwh": 150.0
    },
    {
      "hour": 20,
      "grid_kwh": 173.0,
      "solar_used_kwh": 0.0,
      "battery_action": "discharge",
      "battery_kwh": 100.0,
      "battery_energy_after_kwh": 50.0
    },
    {
      "hour": 21,
      "grid_kwh": 220.5,
      "solar_used_kwh": 0.0,
      "battery_action": "idle",
      "battery_kwh": 0.0,
      "battery_energy_after_kwh": 50.0
    },
    {
      "hour": 22,
      "grid_kwh": 278.5,
      "solar_used_kwh": 0.0,
      "battery_action": "charge",
      "battery_kwh": 100.0,
      "battery_energy_after_kwh": 150.0
    },
    {
      "hour": 23,
      "grid_kwh": 247.0,
      "solar_used_kwh": 0.0,
      "battery_action": "charge",
      "battery_kwh": 100.0,
      "battery_energy_after_kwh": 250.0
    }
  ],
  "total_grid_kwh": 4121.2,
  "total_cost_bdt": 39624.45,
  "peak_grid_kwh": 301.0,
  "plan_summary": "Optimized schedule for GRID-SCENARIO-03. Applied 2 active directive(s). Grid import: 4121.20 kWh, Total cost: 39624.45 BDT, Peak load: 301.00 kWh."
}
```
</details>

---

## Scenario 04: Inverter Diagnostics No-Discharge Window (`GRID-SCENARIO-04`)

**Description**: Tests battery discharge lockout during morning maintenance while demand must be met purely from solar and grid.

### Operational Notes:
- *"Do not pull battery power from 5 AM to 7 AM during inverter diagnostics."*
- *"Library opening hours extended for finals week."*

### Active Directives Applied:
- **`no_discharge_window`**: `{"hours": [5, 6]}` — *Battery discharging prohibited between 5 AM and 7 AM.*

### Key Financial & Grid Results:
- **Total Grid Electricity Imported**: `3560.50 kWh`
- **Total Electricity Cost**: `32932.25 BDT`
- **Peak Hourly Grid Load**: `296.00 kWh`
- **Battery Capacity & State**: Capacity = `600.0 kWh`, Initial/Final SoC = `300.0 kWh` *(End-of-day neutrality verified)*

<details>
<summary><strong>Click to expand Full HTTP Request JSON (POST /optimize-energy)</strong></summary>

```json
{
  "scenario_id": "GRID-SCENARIO-04",
  "operator_notes": [
    "Do not pull battery power from 5 AM to 7 AM during inverter diagnostics.",
    "Library opening hours extended for finals week."
  ],
  "hours": [
    {
      "hour": 0,
      "demand_kwh": 120.0,
      "solar_kwh": 0.0,
      "tariff_bdt_per_kwh": 6.5
    },
    {
      "hour": 1,
      "demand_kwh": 110.0,
      "solar_kwh": 0.0,
      "tariff_bdt_per_kwh": 6.5
    },
    {
      "hour": 2,
      "demand_kwh": 105.0,
      "solar_kwh": 0.0,
      "tariff_bdt_per_kwh": 6.0
    },
    {
      "hour": 3,
      "demand_kwh": 100.0,
      "solar_kwh": 0.0,
      "tariff_bdt_per_kwh": 6.0
    },
    {
      "hour": 4,
      "demand_kwh": 110.0,
      "solar_kwh": 0.0,
      "tariff_bdt_per_kwh": 6.0
    },
    {
      "hour": 5,
      "demand_kwh": 130.0,
      "solar_kwh": 0.0,
      "tariff_bdt_per_kwh": 7.0
    },
    {
      "hour": 6,
      "demand_kwh": 170.0,
      "solar_kwh": 10.5,
      "tariff_bdt_per_kwh": 8.0
    },
    {
      "hour": 7,
      "demand_kwh": 220.0,
      "solar_kwh": 42.0,
      "tariff_bdt_per_kwh": 9.5
    },
    {
      "hour": 8,
      "demand_kwh": 280.0,
      "solar_kwh": 105.0,
      "tariff_bdt_per_kwh": 11.0
    },
    {
      "hour": 9,
      "demand_kwh": 310.0,
      "solar_kwh": 189.0,
      "tariff_bdt_per_kwh": 12.0
    },
    {
      "hour": 10,
      "demand_kwh": 330.0,
      "solar_kwh": 252.0,
      "tariff_bdt_per_kwh": 12.0
    },
    {
      "hour": 11,
      "demand_kwh": 350.0,
      "solar_kwh": 294.0,
      "tariff_bdt_per_kwh": 12.0
    },
    {
      "hour": 12,
      "demand_kwh": 340.0,
      "solar_kwh": 315.0,
      "tariff_bdt_per_kwh": 11.5
    },
    {
      "hour": 13,
      "demand_kwh": 320.0,
      "solar_kwh": 283.5,
      "tariff_bdt_per_kwh": 11.0
    },
    {
      "hour": 14,
      "demand_kwh": 300.0,
      "solar_kwh": 231.0,
      "tariff_bdt_per_kwh": 11.0
    },
    {
      "hour": 15,
      "demand_kwh": 280.0,
      "solar_kwh": 157.5,
      "tariff_bdt_per_kwh": 10.5
    },
    {
      "hour": 16,
      "demand_kwh": 260.0,
      "solar_kwh": 84.0,
      "tariff_bdt_per_kwh": 10.0
    },
    {
      "hour": 17,
      "demand_kwh": 290.0,
      "solar_kwh": 21.0,
      "tariff_bdt_per_kwh": 12.5
    },
    {
      "hour": 18,
      "demand_kwh": 330.0,
      "solar_kwh": 0.0,
      "tariff_bdt_per_kwh": 14.0
    },
    {
      "hour": 19,
      "demand_kwh": 310.0,
      "solar_kwh": 0.0,
      "tariff_bdt_per_kwh": 14.0
    },
    {
      "hour": 20,
      "demand_kwh": 260.0,
      "solar_kwh": 0.0,
      "tariff_bdt_per_kwh": 12.0
    },
    {
      "hour": 21,
      "demand_kwh": 210.0,
      "solar_kwh": 0.0,
      "tariff_bdt_per_kwh": 10.0
    },
    {
      "hour": 22,
      "demand_kwh": 170.0,
      "solar_kwh": 0.0,
      "tariff_bdt_per_kwh": 8.5
    },
    {
      "hour": 23,
      "demand_kwh": 140.0,
      "solar_kwh": 0.0,
      "tariff_bdt_per_kwh": 7.0
    }
  ],
  "battery": {
    "capacity_kwh": 600.0,
    "initial_energy_kwh": 300.0,
    "minimum_energy_kwh": 60.0,
    "max_charge_kwh_per_hour": 120.0,
    "max_discharge_kwh_per_hour": 120.0
  }
}
```
</details>

<details open>
<summary><strong>Full HTTP 200 Response JSON</strong></summary>

```json
{
  "scenario_id": "GRID-SCENARIO-04",
  "directive_interpretation": [
    {
      "note_index": 0,
      "applies": true,
      "directive_type": "no_discharge_window",
      "structured_adjustment": {
        "hours": [
          5,
          6
        ]
      },
      "explanation": "Battery discharging prohibited between 5 AM and 7 AM."
    },
    {
      "note_index": 1,
      "applies": false,
      "directive_type": "no_op",
      "structured_adjustment": null,
      "explanation": "This note does not affect today's energy schedule."
    }
  ],
  "hourly_plan": [
    {
      "hour": 0,
      "grid_kwh": 60.0,
      "solar_used_kwh": 0.0,
      "battery_action": "discharge",
      "battery_kwh": 60.0,
      "battery_energy_after_kwh": 240.0
    },
    {
      "hour": 1,
      "grid_kwh": 110.0,
      "solar_used_kwh": 0.0,
      "battery_action": "idle",
      "battery_kwh": 0.0,
      "battery_energy_after_kwh": 240.0
    },
    {
      "hour": 2,
      "grid_kwh": 225.0,
      "solar_used_kwh": 0.0,
      "battery_action": "charge",
      "battery_kwh": 120.0,
      "battery_energy_after_kwh": 360.0
    },
    {
      "hour": 3,
      "grid_kwh": 220.0,
      "solar_used_kwh": 0.0,
      "battery_action": "charge",
      "battery_kwh": 120.0,
      "battery_energy_after_kwh": 480.0
    },
    {
      "hour": 4,
      "grid_kwh": 230.0,
      "solar_used_kwh": 0.0,
      "battery_action": "charge",
      "battery_kwh": 120.0,
      "battery_energy_after_kwh": 600.0
    },
    {
      "hour": 5,
      "grid_kwh": 130.0,
      "solar_used_kwh": 0.0,
      "battery_action": "idle",
      "battery_kwh": 0.0,
      "battery_energy_after_kwh": 600.0
    },
    {
      "hour": 6,
      "grid_kwh": 159.5,
      "solar_used_kwh": 10.5,
      "battery_action": "idle",
      "battery_kwh": 0.0,
      "battery_energy_after_kwh": 600.0
    },
    {
      "hour": 7,
      "grid_kwh": 178.0,
      "solar_used_kwh": 42.0,
      "battery_action": "idle",
      "battery_kwh": 0.0,
      "battery_energy_after_kwh": 600.0
    },
    {
      "hour": 8,
      "grid_kwh": 154.0,
      "solar_used_kwh": 105.0,
      "battery_action": "discharge",
      "battery_kwh": 21.0,
      "battery_energy_after_kwh": 579.0
    },
    {
      "hour": 9,
      "grid_kwh": 1.0,
      "solar_used_kwh": 189.0,
      "battery_action": "discharge",
      "battery_kwh": 120.0,
      "battery_energy_after_kwh": 459.0
    },
    {
      "hour": 10,
      "grid_kwh": 0.0,
      "solar_used_kwh": 252.0,
      "battery_action": "discharge",
      "battery_kwh": 78.0,
      "battery_energy_after_kwh": 381.0
    },
    {
      "hour": 11,
      "grid_kwh": 0.0,
      "solar_used_kwh": 294.0,
      "battery_action": "discharge",
      "battery_kwh": 56.0,
      "battery_energy_after_kwh": 325.0
    },
    {
      "hour": 12,
      "grid_kwh": 0.0,
      "solar_used_kwh": 315.0,
      "battery_action": "discharge",
      "battery_kwh": 25.0,
      "battery_energy_after_kwh": 300.0
    },
    {
      "hour": 13,
      "grid_kwh": 36.5,
      "solar_used_kwh": 283.5,
      "battery_action": "idle",
      "battery_kwh": 0.0,
      "battery_energy_after_kwh": 300.0
    },
    {
      "hour": 14,
      "grid_kwh": 69.0,
      "solar_used_kwh": 231.0,
      "battery_action": "idle",
      "battery_kwh": 0.0,
      "battery_energy_after_kwh": 300.0
    },
    {
      "hour": 15,
      "grid_kwh": 242.5,
      "solar_used_kwh": 157.5,
      "battery_action": "charge",
      "battery_kwh": 120.0,
      "battery_energy_after_kwh": 420.0
    },
    {
      "hour": 16,
      "grid_kwh": 296.0,
      "solar_used_kwh": 84.0,
      "battery_action": "charge",
      "battery_kwh": 120.0,
      "battery_energy_after_kwh": 540.0
    },
    {
      "hour": 17,
      "grid_kwh": 149.0,
      "solar_used_kwh": 21.0,
      "battery_action": "discharge",
      "battery_kwh": 120.0,
      "battery_energy_after_kwh": 420.0
    },
    {
      "hour": 18,
      "grid_kwh": 210.0,
      "solar_used_kwh": 0.0,
      "battery_action": "discharge",
      "battery_kwh": 120.0,
      "battery_energy_after_kwh": 300.0
    },
    {
      "hour": 19,
      "grid_kwh": 190.0,
      "solar_used_kwh": 0.0,
      "battery_action": "discharge",
      "battery_kwh": 120.0,
      "battery_energy_after_kwh": 180.0
    },
    {
      "hour": 20,
      "grid_kwh": 140.0,
      "solar_used_kwh": 0.0,
      "battery_action": "discharge",
      "battery_kwh": 120.0,
      "battery_energy_after_kwh": 60.0
    },
    {
      "hour": 21,
      "grid_kwh": 210.0,
      "solar_used_kwh": 0.0,
      "battery_action": "idle",
      "battery_kwh": 0.0,
      "battery_energy_after_kwh": 60.0
    },
    {
      "hour": 22,
      "grid_kwh": 290.0,
      "solar_used_kwh": 0.0,
      "battery_action": "charge",
      "battery_kwh": 120.0,
      "battery_energy_after_kwh": 180.0
    },
    {
      "hour": 23,
      "grid_kwh": 260.0,
      "solar_used_kwh": 0.0,
      "battery_action": "charge",
      "battery_kwh": 120.0,
      "battery_energy_after_kwh": 300.0
    }
  ],
  "total_grid_kwh": 3560.5,
  "total_cost_bdt": 32932.25,
  "peak_grid_kwh": 296.0,
  "plan_summary": "Optimized schedule for GRID-SCENARIO-04. Applied 1 active directive(s). Grid import: 3560.50 kWh, Total cost: 32932.25 BDT, Peak load: 296.00 kWh."
}
```
</details>

---

## Scenario 05: Midday Solar Haze and Evening Grid Cap (`GRID-SCENARIO-05`)

**Description**: Tests compound interaction of midday solar derating combined with an evening utility import ceiling.

### Operational Notes:
- *"Expect an 80% reduction in rooftop solar during the 1-3 PM maintenance window."*
- *"Grid import capped at 240 kWh between 6 PM and 9 PM."*

### Active Directives Applied:
- **`solar_reduction`**: `{"hours": [13, 14], "factor": 0.2}` — *Solar availability reduced to 20% between 1 PM and 3 PM.*
- **`max_grid_window`**: `{"hours": [18, 19, 20], "max_grid_kwh": 240.0}` — *Grid import capped at 240 kWh between 6 PM and 9 PM.*

### Key Financial & Grid Results:
- **Total Grid Electricity Imported**: `4047.00 kWh`
- **Total Electricity Cost**: `38787.00 BDT`
- **Peak Hourly Grid Load**: `306.00 kWh`
- **Battery Capacity & State**: Capacity = `500.0 kWh`, Initial/Final SoC = `200.0 kWh` *(End-of-day neutrality verified)*

<details>
<summary><strong>Click to expand Full HTTP Request JSON (POST /optimize-energy)</strong></summary>

```json
{
  "scenario_id": "GRID-SCENARIO-05",
  "operator_notes": [
    "Expect an 80% reduction in rooftop solar during the 1-3 PM maintenance window.",
    "Grid import capped at 240 kWh between 6 PM and 9 PM."
  ],
  "hours": [
    {
      "hour": 0,
      "demand_kwh": 120.0,
      "solar_kwh": 0.0,
      "tariff_bdt_per_kwh": 6.5
    },
    {
      "hour": 1,
      "demand_kwh": 110.0,
      "solar_kwh": 0.0,
      "tariff_bdt_per_kwh": 6.5
    },
    {
      "hour": 2,
      "demand_kwh": 105.0,
      "solar_kwh": 0.0,
      "tariff_bdt_per_kwh": 6.0
    },
    {
      "hour": 3,
      "demand_kwh": 100.0,
      "solar_kwh": 0.0,
      "tariff_bdt_per_kwh": 6.0
    },
    {
      "hour": 4,
      "demand_kwh": 110.0,
      "solar_kwh": 0.0,
      "tariff_bdt_per_kwh": 6.0
    },
    {
      "hour": 5,
      "demand_kwh": 130.0,
      "solar_kwh": 0.0,
      "tariff_bdt_per_kwh": 7.0
    },
    {
      "hour": 6,
      "demand_kwh": 170.0,
      "solar_kwh": 10.0,
      "tariff_bdt_per_kwh": 8.0
    },
    {
      "hour": 7,
      "demand_kwh": 220.0,
      "solar_kwh": 40.0,
      "tariff_bdt_per_kwh": 9.5
    },
    {
      "hour": 8,
      "demand_kwh": 280.0,
      "solar_kwh": 100.0,
      "tariff_bdt_per_kwh": 11.0
    },
    {
      "hour": 9,
      "demand_kwh": 310.0,
      "solar_kwh": 180.0,
      "tariff_bdt_per_kwh": 12.0
    },
    {
      "hour": 10,
      "demand_kwh": 330.0,
      "solar_kwh": 240.0,
      "tariff_bdt_per_kwh": 12.0
    },
    {
      "hour": 11,
      "demand_kwh": 350.0,
      "solar_kwh": 280.0,
      "tariff_bdt_per_kwh": 12.0
    },
    {
      "hour": 12,
      "demand_kwh": 340.0,
      "solar_kwh": 300.0,
      "tariff_bdt_per_kwh": 11.5
    },
    {
      "hour": 13,
      "demand_kwh": 320.0,
      "solar_kwh": 270.0,
      "tariff_bdt_per_kwh": 11.0
    },
    {
      "hour": 14,
      "demand_kwh": 300.0,
      "solar_kwh": 220.0,
      "tariff_bdt_per_kwh": 11.0
    },
    {
      "hour": 15,
      "demand_kwh": 280.0,
      "solar_kwh": 150.0,
      "tariff_bdt_per_kwh": 10.5
    },
    {
      "hour": 16,
      "demand_kwh": 260.0,
      "solar_kwh": 80.0,
      "tariff_bdt_per_kwh": 10.0
    },
    {
      "hour": 17,
      "demand_kwh": 290.0,
      "solar_kwh": 20.0,
      "tariff_bdt_per_kwh": 12.5
    },
    {
      "hour": 18,
      "demand_kwh": 330.0,
      "solar_kwh": 0.0,
      "tariff_bdt_per_kwh": 14.0
    },
    {
      "hour": 19,
      "demand_kwh": 310.0,
      "solar_kwh": 0.0,
      "tariff_bdt_per_kwh": 14.0
    },
    {
      "hour": 20,
      "demand_kwh": 260.0,
      "solar_kwh": 0.0,
      "tariff_bdt_per_kwh": 12.0
    },
    {
      "hour": 21,
      "demand_kwh": 210.0,
      "solar_kwh": 0.0,
      "tariff_bdt_per_kwh": 10.0
    },
    {
      "hour": 22,
      "demand_kwh": 170.0,
      "solar_kwh": 0.0,
      "tariff_bdt_per_kwh": 8.5
    },
    {
      "hour": 23,
      "demand_kwh": 140.0,
      "solar_kwh": 0.0,
      "tariff_bdt_per_kwh": 7.0
    }
  ],
  "battery": {
    "capacity_kwh": 500.0,
    "initial_energy_kwh": 200.0,
    "minimum_energy_kwh": 50.0,
    "max_charge_kwh_per_hour": 100.0,
    "max_discharge_kwh_per_hour": 100.0
  }
}
```
</details>

<details open>
<summary><strong>Full HTTP 200 Response JSON</strong></summary>

```json
{
  "scenario_id": "GRID-SCENARIO-05",
  "directive_interpretation": [
    {
      "note_index": 0,
      "applies": true,
      "directive_type": "solar_reduction",
      "structured_adjustment": {
        "hours": [
          13,
          14
        ],
        "factor": 0.2
      },
      "explanation": "Solar availability reduced to 20% between 1 PM and 3 PM."
    },
    {
      "note_index": 1,
      "applies": true,
      "directive_type": "max_grid_window",
      "structured_adjustment": {
        "hours": [
          18,
          19,
          20
        ],
        "max_grid_kwh": 240.0
      },
      "explanation": "Grid import capped at 240 kWh between 6 PM and 9 PM."
    }
  ],
  "hourly_plan": [
    {
      "hour": 0,
      "grid_kwh": 120.0,
      "solar_used_kwh": 0.0,
      "battery_action": "idle",
      "battery_kwh": 0.0,
      "battery_energy_after_kwh": 200.0
    },
    {
      "hour": 1,
      "grid_kwh": 110.0,
      "solar_used_kwh": 0.0,
      "battery_action": "idle",
      "battery_kwh": 0.0,
      "battery_energy_after_kwh": 200.0
    },
    {
      "hour": 2,
      "grid_kwh": 205.0,
      "solar_used_kwh": 0.0,
      "battery_action": "charge",
      "battery_kwh": 100.0,
      "battery_energy_after_kwh": 300.0
    },
    {
      "hour": 3,
      "grid_kwh": 200.0,
      "solar_used_kwh": 0.0,
      "battery_action": "charge",
      "battery_kwh": 100.0,
      "battery_energy_after_kwh": 400.0
    },
    {
      "hour": 4,
      "grid_kwh": 210.0,
      "solar_used_kwh": 0.0,
      "battery_action": "charge",
      "battery_kwh": 100.0,
      "battery_energy_after_kwh": 500.0
    },
    {
      "hour": 5,
      "grid_kwh": 130.0,
      "solar_used_kwh": 0.0,
      "battery_action": "idle",
      "battery_kwh": 0.0,
      "battery_energy_after_kwh": 500.0
    },
    {
      "hour": 6,
      "grid_kwh": 160.0,
      "solar_used_kwh": 10.0,
      "battery_action": "idle",
      "battery_kwh": 0.0,
      "battery_energy_after_kwh": 500.0
    },
    {
      "hour": 7,
      "grid_kwh": 180.0,
      "solar_used_kwh": 40.0,
      "battery_action": "idle",
      "battery_kwh": 0.0,
      "battery_energy_after_kwh": 500.0
    },
    {
      "hour": 8,
      "grid_kwh": 180.0,
      "solar_used_kwh": 100.0,
      "battery_action": "idle",
      "battery_kwh": 0.0,
      "battery_energy_after_kwh": 500.0
    },
    {
      "hour": 9,
      "grid_kwh": 30.0,
      "solar_used_kwh": 180.0,
      "battery_action": "discharge",
      "battery_kwh": 100.0,
      "battery_energy_after_kwh": 400.0
    },
    {
      "hour": 10,
      "grid_kwh": 0.0,
      "solar_used_kwh": 240.0,
      "battery_action": "discharge",
      "battery_kwh": 90.0,
      "battery_energy_after_kwh": 310.0
    },
    {
      "hour": 11,
      "grid_kwh": 0.0,
      "solar_used_kwh": 280.0,
      "battery_action": "discharge",
      "battery_kwh": 70.0,
      "battery_energy_after_kwh": 240.0
    },
    {
      "hour": 12,
      "grid_kwh": 0.0,
      "solar_used_kwh": 300.0,
      "battery_action": "discharge",
      "battery_kwh": 40.0,
      "battery_energy_after_kwh": 200.0
    },
    {
      "hour": 13,
      "grid_kwh": 266.0,
      "solar_used_kwh": 54.0,
      "battery_action": "idle",
      "battery_kwh": 0.0,
      "battery_energy_after_kwh": 200.0
    },
    {
      "hour": 14,
      "grid_kwh": 306.0,
      "solar_used_kwh": 44.0,
      "battery_action": "charge",
      "battery_kwh": 50.0,
      "battery_energy_after_kwh": 250.0
    },
    {
      "hour": 15,
      "grid_kwh": 230.0,
      "solar_used_kwh": 150.0,
      "battery_action": "charge",
      "battery_kwh": 100.0,
      "battery_energy_after_kwh": 350.0
    },
    {
      "hour": 16,
      "grid_kwh": 280.0,
      "solar_used_kwh": 80.0,
      "battery_action": "charge",
      "battery_kwh": 100.0,
      "battery_energy_after_kwh": 450.0
    },
    {
      "hour": 17,
      "grid_kwh": 170.0,
      "solar_used_kwh": 20.0,
      "battery_action": "discharge",
      "battery_kwh": 100.0,
      "battery_energy_after_kwh": 350.0
    },
    {
      "hour": 18,
      "grid_kwh": 230.0,
      "solar_used_kwh": 0.0,
      "battery_action": "discharge",
      "battery_kwh": 100.0,
      "battery_energy_after_kwh": 250.0
    },
    {
      "hour": 19,
      "grid_kwh": 210.0,
      "solar_used_kwh": 0.0,
      "battery_action": "discharge",
      "battery_kwh": 100.0,
      "battery_energy_after_kwh": 150.0
    },
    {
      "hour": 20,
      "grid_kwh": 160.0,
      "solar_used_kwh": 0.0,
      "battery_action": "discharge",
      "battery_kwh": 100.0,
      "battery_energy_after_kwh": 50.0
    },
    {
      "hour": 21,
      "grid_kwh": 210.0,
      "solar_used_kwh": 0.0,
      "battery_action": "idle",
      "battery_kwh": 0.0,
      "battery_energy_after_kwh": 50.0
    },
    {
      "hour": 22,
      "grid_kwh": 220.0,
      "solar_used_kwh": 0.0,
      "battery_action": "charge",
      "battery_kwh": 50.0,
      "battery_energy_after_kwh": 100.0
    },
    {
      "hour": 23,
      "grid_kwh": 240.0,
      "solar_used_kwh": 0.0,
      "battery_action": "charge",
      "battery_kwh": 100.0,
      "battery_energy_after_kwh": 200.0
    }
  ],
  "total_grid_kwh": 4047.0,
  "total_cost_bdt": 38787.0,
  "peak_grid_kwh": 306.0,
  "plan_summary": "Optimized schedule for GRID-SCENARIO-05. Applied 2 active directive(s). Grid import: 4047.00 kWh, Total cost: 38787.00 BDT, Peak load: 306.00 kWh."
}
```
</details>

---

## Scenario 06: Midday No-Discharge & Night Safety Reserve (`GRID-SCENARIO-06`)

**Description**: Prevents battery discharge during solar peak and mandates a 100 kWh safety floor across late evening.

### Operational Notes:
- *"No battery discharging permitted between 11:00 and 14:00."*
- *"Maintain at least 100 kWh reserve between 18:00 and 22:00."*

### Active Directives Applied:
- **`minimum_battery_reserve`**: `{"hours": [18, 19, 20, 21], "minimum_energy_kwh": 100.0}` — *Keep at least 100 kWh in reserve between 6 PM and 10 PM.*

### Key Financial & Grid Results:
- **Total Grid Electricity Imported**: `4209.50 kWh`
- **Total Electricity Cost**: `40858.50 BDT`
- **Peak Hourly Grid Load**: `296.00 kWh`
- **Battery Capacity & State**: Capacity = `450.0 kWh`, Initial/Final SoC = `200.0 kWh` *(End-of-day neutrality verified)*

<details>
<summary><strong>Click to expand Full HTTP Request JSON (POST /optimize-energy)</strong></summary>

```json
{
  "scenario_id": "GRID-SCENARIO-06",
  "operator_notes": [
    "No battery discharging permitted between 11:00 and 14:00.",
    "Maintain at least 100 kWh reserve between 18:00 and 22:00."
  ],
  "hours": [
    {
      "hour": 0,
      "demand_kwh": 132.0,
      "solar_kwh": 0.0,
      "tariff_bdt_per_kwh": 6.5
    },
    {
      "hour": 1,
      "demand_kwh": 121.0,
      "solar_kwh": 0.0,
      "tariff_bdt_per_kwh": 6.5
    },
    {
      "hour": 2,
      "demand_kwh": 115.5,
      "solar_kwh": 0.0,
      "tariff_bdt_per_kwh": 6.0
    },
    {
      "hour": 3,
      "demand_kwh": 110.0,
      "solar_kwh": 0.0,
      "tariff_bdt_per_kwh": 6.0
    },
    {
      "hour": 4,
      "demand_kwh": 121.0,
      "solar_kwh": 0.0,
      "tariff_bdt_per_kwh": 6.0
    },
    {
      "hour": 5,
      "demand_kwh": 143.0,
      "solar_kwh": 0.0,
      "tariff_bdt_per_kwh": 7.0
    },
    {
      "hour": 6,
      "demand_kwh": 187.0,
      "solar_kwh": 10.0,
      "tariff_bdt_per_kwh": 8.0
    },
    {
      "hour": 7,
      "demand_kwh": 242.0,
      "solar_kwh": 40.0,
      "tariff_bdt_per_kwh": 9.5
    },
    {
      "hour": 8,
      "demand_kwh": 308.0,
      "solar_kwh": 100.0,
      "tariff_bdt_per_kwh": 11.0
    },
    {
      "hour": 9,
      "demand_kwh": 341.0,
      "solar_kwh": 180.0,
      "tariff_bdt_per_kwh": 12.0
    },
    {
      "hour": 10,
      "demand_kwh": 363.0,
      "solar_kwh": 240.0,
      "tariff_bdt_per_kwh": 12.0
    },
    {
      "hour": 11,
      "demand_kwh": 385.0,
      "solar_kwh": 280.0,
      "tariff_bdt_per_kwh": 12.0
    },
    {
      "hour": 12,
      "demand_kwh": 374.0,
      "solar_kwh": 300.0,
      "tariff_bdt_per_kwh": 11.5
    },
    {
      "hour": 13,
      "demand_kwh": 352.0,
      "solar_kwh": 270.0,
      "tariff_bdt_per_kwh": 11.0
    },
    {
      "hour": 14,
      "demand_kwh": 330.0,
      "solar_kwh": 220.0,
      "tariff_bdt_per_kwh": 11.0
    },
    {
      "hour": 15,
      "demand_kwh": 308.0,
      "solar_kwh": 150.0,
      "tariff_bdt_per_kwh": 10.5
    },
    {
      "hour": 16,
      "demand_kwh": 286.0,
      "solar_kwh": 80.0,
      "tariff_bdt_per_kwh": 10.0
    },
    {
      "hour": 17,
      "demand_kwh": 319.0,
      "solar_kwh": 20.0,
      "tariff_bdt_per_kwh": 12.5
    },
    {
      "hour": 18,
      "demand_kwh": 363.0,
      "solar_kwh": 0.0,
      "tariff_bdt_per_kwh": 14.0
    },
    {
      "hour": 19,
      "demand_kwh": 341.0,
      "solar_kwh": 0.0,
      "tariff_bdt_per_kwh": 14.0
    },
    {
      "hour": 20,
      "demand_kwh": 286.0,
      "solar_kwh": 0.0,
      "tariff_bdt_per_kwh": 12.0
    },
    {
      "hour": 21,
      "demand_kwh": 231.0,
      "solar_kwh": 0.0,
      "tariff_bdt_per_kwh": 10.0
    },
    {
      "hour": 22,
      "demand_kwh": 187.0,
      "solar_kwh": 0.0,
      "tariff_bdt_per_kwh": 8.5
    },
    {
      "hour": 23,
      "demand_kwh": 154.0,
      "solar_kwh": 0.0,
      "tariff_bdt_per_kwh": 7.0
    }
  ],
  "battery": {
    "capacity_kwh": 450.0,
    "initial_energy_kwh": 200.0,
    "minimum_energy_kwh": 40.0,
    "max_charge_kwh_per_hour": 90.0,
    "max_discharge_kwh_per_hour": 90.0
  }
}
```
</details>

<details open>
<summary><strong>Full HTTP 200 Response JSON</strong></summary>

```json
{
  "scenario_id": "GRID-SCENARIO-06",
  "directive_interpretation": [
    {
      "note_index": 0,
      "applies": false,
      "directive_type": "no_op",
      "structured_adjustment": null,
      "explanation": "This note does not affect today's energy schedule."
    },
    {
      "note_index": 1,
      "applies": true,
      "directive_type": "minimum_battery_reserve",
      "structured_adjustment": {
        "hours": [
          18,
          19,
          20,
          21
        ],
        "minimum_energy_kwh": 100.0
      },
      "explanation": "Keep at least 100 kWh in reserve between 6 PM and 10 PM."
    }
  ],
  "hourly_plan": [
    {
      "hour": 0,
      "grid_kwh": 132.0,
      "solar_used_kwh": 0.0,
      "battery_action": "idle",
      "battery_kwh": 0.0,
      "battery_energy_after_kwh": 200.0
    },
    {
      "hour": 1,
      "grid_kwh": 101.0,
      "solar_used_kwh": 0.0,
      "battery_action": "discharge",
      "battery_kwh": 20.0,
      "battery_energy_after_kwh": 180.0
    },
    {
      "hour": 2,
      "grid_kwh": 205.5,
      "solar_used_kwh": 0.0,
      "battery_action": "charge",
      "battery_kwh": 90.0,
      "battery_energy_after_kwh": 270.0
    },
    {
      "hour": 3,
      "grid_kwh": 200.0,
      "solar_used_kwh": 0.0,
      "battery_action": "charge",
      "battery_kwh": 90.0,
      "battery_energy_after_kwh": 360.0
    },
    {
      "hour": 4,
      "grid_kwh": 211.0,
      "solar_used_kwh": 0.0,
      "battery_action": "charge",
      "battery_kwh": 90.0,
      "battery_energy_after_kwh": 450.0
    },
    {
      "hour": 5,
      "grid_kwh": 143.0,
      "solar_used_kwh": 0.0,
      "battery_action": "idle",
      "battery_kwh": 0.0,
      "battery_energy_after_kwh": 450.0
    },
    {
      "hour": 6,
      "grid_kwh": 177.0,
      "solar_used_kwh": 10.0,
      "battery_action": "idle",
      "battery_kwh": 0.0,
      "battery_energy_after_kwh": 450.0
    },
    {
      "hour": 7,
      "grid_kwh": 202.0,
      "solar_used_kwh": 40.0,
      "battery_action": "idle",
      "battery_kwh": 0.0,
      "battery_energy_after_kwh": 450.0
    },
    {
      "hour": 8,
      "grid_kwh": 208.0,
      "solar_used_kwh": 100.0,
      "battery_action": "idle",
      "battery_kwh": 0.0,
      "battery_energy_after_kwh": 450.0
    },
    {
      "hour": 9,
      "grid_kwh": 71.0,
      "solar_used_kwh": 180.0,
      "battery_action": "discharge",
      "battery_kwh": 90.0,
      "battery_energy_after_kwh": 360.0
    },
    {
      "hour": 10,
      "grid_kwh": 33.0,
      "solar_used_kwh": 240.0,
      "battery_action": "discharge",
      "battery_kwh": 90.0,
      "battery_energy_after_kwh": 270.0
    },
    {
      "hour": 11,
      "grid_kwh": 15.0,
      "solar_used_kwh": 280.0,
      "battery_action": "discharge",
      "battery_kwh": 90.0,
      "battery_energy_after_kwh": 180.0
    },
    {
      "hour": 12,
      "grid_kwh": 0.0,
      "solar_used_kwh": 300.0,
      "battery_action": "discharge",
      "battery_kwh": 74.0,
      "battery_energy_after_kwh": 106.0
    },
    {
      "hour": 13,
      "grid_kwh": 156.0,
      "solar_used_kwh": 270.0,
      "battery_action": "charge",
      "battery_kwh": 74.0,
      "battery_energy_after_kwh": 180.0
    },
    {
      "hour": 14,
      "grid_kwh": 200.0,
      "solar_used_kwh": 220.0,
      "battery_action": "charge",
      "battery_kwh": 90.0,
      "battery_energy_after_kwh": 270.0
    },
    {
      "hour": 15,
      "grid_kwh": 248.0,
      "solar_used_kwh": 150.0,
      "battery_action": "charge",
      "battery_kwh": 90.0,
      "battery_energy_after_kwh": 360.0
    },
    {
      "hour": 16,
      "grid_kwh": 296.0,
      "solar_used_kwh": 80.0,
      "battery_action": "charge",
      "battery_kwh": 90.0,
      "battery_energy_after_kwh": 450.0
    },
    {
      "hour": 17,
      "grid_kwh": 209.0,
      "solar_used_kwh": 20.0,
      "battery_action": "discharge",
      "battery_kwh": 90.0,
      "battery_energy_after_kwh": 360.0
    },
    {
      "hour": 18,
      "grid_kwh": 273.0,
      "solar_used_kwh": 0.0,
      "battery_action": "discharge",
      "battery_kwh": 90.0,
      "battery_energy_after_kwh": 270.0
    },
    {
      "hour": 19,
      "grid_kwh": 251.0,
      "solar_used_kwh": 0.0,
      "battery_action": "discharge",
      "battery_kwh": 90.0,
      "battery_energy_after_kwh": 180.0
    },
    {
      "hour": 20,
      "grid_kwh": 206.0,
      "solar_used_kwh": 0.0,
      "battery_action": "discharge",
      "battery_kwh": 80.0,
      "battery_energy_after_kwh": 100.0
    },
    {
      "hour": 21,
      "grid_kwh": 231.0,
      "solar_used_kwh": 0.0,
      "battery_action": "idle",
      "battery_kwh": 0.0,
      "battery_energy_after_kwh": 100.0
    },
    {
      "hour": 22,
      "grid_kwh": 197.0,
      "solar_used_kwh": 0.0,
      "battery_action": "charge",
      "battery_kwh": 10.0,
      "battery_energy_after_kwh": 110.0
    },
    {
      "hour": 23,
      "grid_kwh": 244.0,
      "solar_used_kwh": 0.0,
      "battery_action": "charge",
      "battery_kwh": 90.0,
      "battery_energy_after_kwh": 200.0
    }
  ],
  "total_grid_kwh": 4209.5,
  "total_cost_bdt": 40858.5,
  "peak_grid_kwh": 296.0,
  "plan_summary": "Optimized schedule for GRID-SCENARIO-06. Applied 1 active directive(s). Grid import: 4209.50 kWh, Total cost: 40858.50 BDT, Peak load: 296.00 kWh."
}
```
</details>

---

## Scenario 07: Triple Directive Compound Constraint Crunch (`GRID-SCENARIO-07`)

**Description**: Stresses the optimizer with 3 active concurrent directives: solar derating, charge lockout, and grid import capping.

### Operational Notes:
- *"PV production will drop to about 20% between 13:00 and 15:00."*
- *"Inverter testing: no battery charging allowed from 14:00 to 16:00."*
- *"Grid import capped at 100 kWh from 8 AM to 11 AM."*

### Active Directives Applied:
- **`solar_reduction`**: `{"hours": [13, 14], "factor": 0.2}` — *Solar availability reduced to 20% between 1 PM and 3 PM.*
- **`no_charge_window`**: `{"hours": [14, 15]}` — *Battery charging prohibited between 2 PM and 4 PM.*
- **`max_grid_window`**: `{"hours": [8, 9, 10], "max_grid_kwh": 100.0}` — *Grid import capped at 100 kWh between 8 AM and 11 AM.*

### Key Financial & Grid Results:
- **Total Grid Electricity Imported**: `4047.00 kWh`
- **Total Electricity Cost**: `38902.00 BDT`
- **Peak Hourly Grid Load**: `366.00 kWh`
- **Battery Capacity & State**: Capacity = `500.0 kWh`, Initial/Final SoC = `200.0 kWh` *(End-of-day neutrality verified)*

<details>
<summary><strong>Click to expand Full HTTP Request JSON (POST /optimize-energy)</strong></summary>

```json
{
  "scenario_id": "GRID-SCENARIO-07",
  "operator_notes": [
    "PV production will drop to about 20% between 13:00 and 15:00.",
    "Inverter testing: no battery charging allowed from 14:00 to 16:00.",
    "Grid import capped at 100 kWh from 8 AM to 11 AM."
  ],
  "hours": [
    {
      "hour": 0,
      "demand_kwh": 120.0,
      "solar_kwh": 0.0,
      "tariff_bdt_per_kwh": 6.5
    },
    {
      "hour": 1,
      "demand_kwh": 110.0,
      "solar_kwh": 0.0,
      "tariff_bdt_per_kwh": 6.5
    },
    {
      "hour": 2,
      "demand_kwh": 105.0,
      "solar_kwh": 0.0,
      "tariff_bdt_per_kwh": 6.0
    },
    {
      "hour": 3,
      "demand_kwh": 100.0,
      "solar_kwh": 0.0,
      "tariff_bdt_per_kwh": 6.0
    },
    {
      "hour": 4,
      "demand_kwh": 110.0,
      "solar_kwh": 0.0,
      "tariff_bdt_per_kwh": 6.0
    },
    {
      "hour": 5,
      "demand_kwh": 130.0,
      "solar_kwh": 0.0,
      "tariff_bdt_per_kwh": 7.0
    },
    {
      "hour": 6,
      "demand_kwh": 170.0,
      "solar_kwh": 10.0,
      "tariff_bdt_per_kwh": 8.0
    },
    {
      "hour": 7,
      "demand_kwh": 220.0,
      "solar_kwh": 40.0,
      "tariff_bdt_per_kwh": 9.5
    },
    {
      "hour": 8,
      "demand_kwh": 280.0,
      "solar_kwh": 100.0,
      "tariff_bdt_per_kwh": 11.0
    },
    {
      "hour": 9,
      "demand_kwh": 310.0,
      "solar_kwh": 180.0,
      "tariff_bdt_per_kwh": 12.0
    },
    {
      "hour": 10,
      "demand_kwh": 330.0,
      "solar_kwh": 240.0,
      "tariff_bdt_per_kwh": 12.0
    },
    {
      "hour": 11,
      "demand_kwh": 350.0,
      "solar_kwh": 280.0,
      "tariff_bdt_per_kwh": 12.0
    },
    {
      "hour": 12,
      "demand_kwh": 340.0,
      "solar_kwh": 300.0,
      "tariff_bdt_per_kwh": 11.5
    },
    {
      "hour": 13,
      "demand_kwh": 320.0,
      "solar_kwh": 270.0,
      "tariff_bdt_per_kwh": 11.0
    },
    {
      "hour": 14,
      "demand_kwh": 300.0,
      "solar_kwh": 220.0,
      "tariff_bdt_per_kwh": 11.0
    },
    {
      "hour": 15,
      "demand_kwh": 280.0,
      "solar_kwh": 150.0,
      "tariff_bdt_per_kwh": 10.5
    },
    {
      "hour": 16,
      "demand_kwh": 260.0,
      "solar_kwh": 80.0,
      "tariff_bdt_per_kwh": 10.0
    },
    {
      "hour": 17,
      "demand_kwh": 290.0,
      "solar_kwh": 20.0,
      "tariff_bdt_per_kwh": 12.5
    },
    {
      "hour": 18,
      "demand_kwh": 330.0,
      "solar_kwh": 0.0,
      "tariff_bdt_per_kwh": 14.0
    },
    {
      "hour": 19,
      "demand_kwh": 310.0,
      "solar_kwh": 0.0,
      "tariff_bdt_per_kwh": 14.0
    },
    {
      "hour": 20,
      "demand_kwh": 260.0,
      "solar_kwh": 0.0,
      "tariff_bdt_per_kwh": 12.0
    },
    {
      "hour": 21,
      "demand_kwh": 210.0,
      "solar_kwh": 0.0,
      "tariff_bdt_per_kwh": 10.0
    },
    {
      "hour": 22,
      "demand_kwh": 170.0,
      "solar_kwh": 0.0,
      "tariff_bdt_per_kwh": 8.5
    },
    {
      "hour": 23,
      "demand_kwh": 140.0,
      "solar_kwh": 0.0,
      "tariff_bdt_per_kwh": 7.0
    }
  ],
  "battery": {
    "capacity_kwh": 500.0,
    "initial_energy_kwh": 200.0,
    "minimum_energy_kwh": 50.0,
    "max_charge_kwh_per_hour": 100.0,
    "max_discharge_kwh_per_hour": 100.0
  }
}
```
</details>

<details open>
<summary><strong>Full HTTP 200 Response JSON</strong></summary>

```json
{
  "scenario_id": "GRID-SCENARIO-07",
  "directive_interpretation": [
    {
      "note_index": 0,
      "applies": true,
      "directive_type": "solar_reduction",
      "structured_adjustment": {
        "hours": [
          13,
          14
        ],
        "factor": 0.2
      },
      "explanation": "Solar availability reduced to 20% between 1 PM and 3 PM."
    },
    {
      "note_index": 1,
      "applies": true,
      "directive_type": "no_charge_window",
      "structured_adjustment": {
        "hours": [
          14,
          15
        ]
      },
      "explanation": "Battery charging prohibited between 2 PM and 4 PM."
    },
    {
      "note_index": 2,
      "applies": true,
      "directive_type": "max_grid_window",
      "structured_adjustment": {
        "hours": [
          8,
          9,
          10
        ],
        "max_grid_kwh": 100.0
      },
      "explanation": "Grid import capped at 100 kWh between 8 AM and 11 AM."
    }
  ],
  "hourly_plan": [
    {
      "hour": 0,
      "grid_kwh": 120.0,
      "solar_used_kwh": 0.0,
      "battery_action": "idle",
      "battery_kwh": 0.0,
      "battery_energy_after_kwh": 200.0
    },
    {
      "hour": 1,
      "grid_kwh": 110.0,
      "solar_used_kwh": 0.0,
      "battery_action": "idle",
      "battery_kwh": 0.0,
      "battery_energy_after_kwh": 200.0
    },
    {
      "hour": 2,
      "grid_kwh": 205.0,
      "solar_used_kwh": 0.0,
      "battery_action": "charge",
      "battery_kwh": 100.0,
      "battery_energy_after_kwh": 300.0
    },
    {
      "hour": 3,
      "grid_kwh": 200.0,
      "solar_used_kwh": 0.0,
      "battery_action": "charge",
      "battery_kwh": 100.0,
      "battery_energy_after_kwh": 400.0
    },
    {
      "hour": 4,
      "grid_kwh": 210.0,
      "solar_used_kwh": 0.0,
      "battery_action": "charge",
      "battery_kwh": 100.0,
      "battery_energy_after_kwh": 500.0
    },
    {
      "hour": 5,
      "grid_kwh": 130.0,
      "solar_used_kwh": 0.0,
      "battery_action": "idle",
      "battery_kwh": 0.0,
      "battery_energy_after_kwh": 500.0
    },
    {
      "hour": 6,
      "grid_kwh": 160.0,
      "solar_used_kwh": 10.0,
      "battery_action": "idle",
      "battery_kwh": 0.0,
      "battery_energy_after_kwh": 500.0
    },
    {
      "hour": 7,
      "grid_kwh": 180.0,
      "solar_used_kwh": 40.0,
      "battery_action": "idle",
      "battery_kwh": 0.0,
      "battery_energy_after_kwh": 500.0
    },
    {
      "hour": 8,
      "grid_kwh": 100.0,
      "solar_used_kwh": 100.0,
      "battery_action": "discharge",
      "battery_kwh": 80.0,
      "battery_energy_after_kwh": 420.0
    },
    {
      "hour": 9,
      "grid_kwh": 30.0,
      "solar_used_kwh": 180.0,
      "battery_action": "discharge",
      "battery_kwh": 100.0,
      "battery_energy_after_kwh": 320.0
    },
    {
      "hour": 10,
      "grid_kwh": 0.0,
      "solar_used_kwh": 240.0,
      "battery_action": "discharge",
      "battery_kwh": 90.0,
      "battery_energy_after_kwh": 230.0
    },
    {
      "hour": 11,
      "grid_kwh": 0.0,
      "solar_used_kwh": 280.0,
      "battery_action": "discharge",
      "battery_kwh": 70.0,
      "battery_energy_after_kwh": 160.0
    },
    {
      "hour": 12,
      "grid_kwh": 130.0,
      "solar_used_kwh": 300.0,
      "battery_action": "charge",
      "battery_kwh": 90.0,
      "battery_energy_after_kwh": 250.0
    },
    {
      "hour": 13,
      "grid_kwh": 366.0,
      "solar_used_kwh": 54.0,
      "battery_action": "charge",
      "battery_kwh": 100.0,
      "battery_energy_after_kwh": 350.0
    },
    {
      "hour": 14,
      "grid_kwh": 256.0,
      "solar_used_kwh": 44.0,
      "battery_action": "idle",
      "battery_kwh": 0.0,
      "battery_energy_after_kwh": 350.0
    },
    {
      "hour": 15,
      "grid_kwh": 130.0,
      "solar_used_kwh": 150.0,
      "battery_action": "idle",
      "battery_kwh": 0.0,
      "battery_energy_after_kwh": 350.0
    },
    {
      "hour": 16,
      "grid_kwh": 280.0,
      "solar_used_kwh": 80.0,
      "battery_action": "charge",
      "battery_kwh": 100.0,
      "battery_energy_after_kwh": 450.0
    },
    {
      "hour": 17,
      "grid_kwh": 170.0,
      "solar_used_kwh": 20.0,
      "battery_action": "discharge",
      "battery_kwh": 100.0,
      "battery_energy_after_kwh": 350.0
    },
    {
      "hour": 18,
      "grid_kwh": 230.0,
      "solar_used_kwh": 0.0,
      "battery_action": "discharge",
      "battery_kwh": 100.0,
      "battery_energy_after_kwh": 250.0
    },
    {
      "hour": 19,
      "grid_kwh": 210.0,
      "solar_used_kwh": 0.0,
      "battery_action": "discharge",
      "battery_kwh": 100.0,
      "battery_energy_after_kwh": 150.0
    },
    {
      "hour": 20,
      "grid_kwh": 160.0,
      "solar_used_kwh": 0.0,
      "battery_action": "discharge",
      "battery_kwh": 100.0,
      "battery_energy_after_kwh": 50.0
    },
    {
      "hour": 21,
      "grid_kwh": 210.0,
      "solar_used_kwh": 0.0,
      "battery_action": "idle",
      "battery_kwh": 0.0,
      "battery_energy_after_kwh": 50.0
    },
    {
      "hour": 22,
      "grid_kwh": 220.0,
      "solar_used_kwh": 0.0,
      "battery_action": "charge",
      "battery_kwh": 50.0,
      "battery_energy_after_kwh": 100.0
    },
    {
      "hour": 23,
      "grid_kwh": 240.0,
      "solar_used_kwh": 0.0,
      "battery_action": "charge",
      "battery_kwh": 100.0,
      "battery_energy_after_kwh": 200.0
    }
  ],
  "total_grid_kwh": 4047.0,
  "total_cost_bdt": 38902.0,
  "peak_grid_kwh": 366.0,
  "plan_summary": "Optimized schedule for GRID-SCENARIO-07. Applied 3 active directive(s). Grid import: 4047.00 kWh, Total cost: 38902.00 BDT, Peak load: 366.00 kWh."
}
```
</details>

---

## Scenario 08: Overnight No-Discharge Protection (`GRID-SCENARIO-08`)

**Description**: Restricts early morning battery usage to preserve energy for high-tariff daytime dispatch.

### Operational Notes:
- *"Do not discharge the battery between 1 AM and 4 AM."*
- *"Auditorium booking confirmed for CSE Fest inauguration."*

### Active Directives Applied:
- **`no_discharge_window`**: `{"hours": [1, 2, 3]}` — *Battery discharging prohibited between 1 AM and 4 AM.*

### Key Financial & Grid Results:
- **Total Grid Electricity Imported**: `3655.00 kWh`
- **Total Electricity Cost**: `35110.00 BDT`
- **Peak Hourly Grid Load**: `260.00 kWh`
- **Battery Capacity & State**: Capacity = `400.0 kWh`, Initial/Final SoC = `160.0 kWh` *(End-of-day neutrality verified)*

<details>
<summary><strong>Click to expand Full HTTP Request JSON (POST /optimize-energy)</strong></summary>

```json
{
  "scenario_id": "GRID-SCENARIO-08",
  "operator_notes": [
    "Do not discharge the battery between 1 AM and 4 AM.",
    "Auditorium booking confirmed for CSE Fest inauguration."
  ],
  "hours": [
    {
      "hour": 0,
      "demand_kwh": 120.0,
      "solar_kwh": 0.0,
      "tariff_bdt_per_kwh": 6.5
    },
    {
      "hour": 1,
      "demand_kwh": 110.0,
      "solar_kwh": 0.0,
      "tariff_bdt_per_kwh": 6.5
    },
    {
      "hour": 2,
      "demand_kwh": 105.0,
      "solar_kwh": 0.0,
      "tariff_bdt_per_kwh": 6.0
    },
    {
      "hour": 3,
      "demand_kwh": 100.0,
      "solar_kwh": 0.0,
      "tariff_bdt_per_kwh": 6.0
    },
    {
      "hour": 4,
      "demand_kwh": 110.0,
      "solar_kwh": 0.0,
      "tariff_bdt_per_kwh": 6.0
    },
    {
      "hour": 5,
      "demand_kwh": 130.0,
      "solar_kwh": 0.0,
      "tariff_bdt_per_kwh": 7.0
    },
    {
      "hour": 6,
      "demand_kwh": 170.0,
      "solar_kwh": 10.0,
      "tariff_bdt_per_kwh": 8.0
    },
    {
      "hour": 7,
      "demand_kwh": 220.0,
      "solar_kwh": 40.0,
      "tariff_bdt_per_kwh": 9.5
    },
    {
      "hour": 8,
      "demand_kwh": 280.0,
      "solar_kwh": 100.0,
      "tariff_bdt_per_kwh": 11.0
    },
    {
      "hour": 9,
      "demand_kwh": 310.0,
      "solar_kwh": 180.0,
      "tariff_bdt_per_kwh": 12.0
    },
    {
      "hour": 10,
      "demand_kwh": 330.0,
      "solar_kwh": 240.0,
      "tariff_bdt_per_kwh": 12.0
    },
    {
      "hour": 11,
      "demand_kwh": 350.0,
      "solar_kwh": 280.0,
      "tariff_bdt_per_kwh": 12.0
    },
    {
      "hour": 12,
      "demand_kwh": 340.0,
      "solar_kwh": 300.0,
      "tariff_bdt_per_kwh": 11.5
    },
    {
      "hour": 13,
      "demand_kwh": 320.0,
      "solar_kwh": 270.0,
      "tariff_bdt_per_kwh": 11.0
    },
    {
      "hour": 14,
      "demand_kwh": 300.0,
      "solar_kwh": 220.0,
      "tariff_bdt_per_kwh": 11.0
    },
    {
      "hour": 15,
      "demand_kwh": 280.0,
      "solar_kwh": 150.0,
      "tariff_bdt_per_kwh": 10.5
    },
    {
      "hour": 16,
      "demand_kwh": 260.0,
      "solar_kwh": 80.0,
      "tariff_bdt_per_kwh": 10.0
    },
    {
      "hour": 17,
      "demand_kwh": 290.0,
      "solar_kwh": 20.0,
      "tariff_bdt_per_kwh": 12.5
    },
    {
      "hour": 18,
      "demand_kwh": 330.0,
      "solar_kwh": 0.0,
      "tariff_bdt_per_kwh": 14.0
    },
    {
      "hour": 19,
      "demand_kwh": 310.0,
      "solar_kwh": 0.0,
      "tariff_bdt_per_kwh": 14.0
    },
    {
      "hour": 20,
      "demand_kwh": 260.0,
      "solar_kwh": 0.0,
      "tariff_bdt_per_kwh": 12.0
    },
    {
      "hour": 21,
      "demand_kwh": 210.0,
      "solar_kwh": 0.0,
      "tariff_bdt_per_kwh": 10.0
    },
    {
      "hour": 22,
      "demand_kwh": 170.0,
      "solar_kwh": 0.0,
      "tariff_bdt_per_kwh": 8.5
    },
    {
      "hour": 23,
      "demand_kwh": 140.0,
      "solar_kwh": 0.0,
      "tariff_bdt_per_kwh": 7.0
    }
  ],
  "battery": {
    "capacity_kwh": 400.0,
    "initial_energy_kwh": 160.0,
    "minimum_energy_kwh": 40.0,
    "max_charge_kwh_per_hour": 80.0,
    "max_discharge_kwh_per_hour": 80.0
  }
}
```
</details>

<details open>
<summary><strong>Full HTTP 200 Response JSON</strong></summary>

```json
{
  "scenario_id": "GRID-SCENARIO-08",
  "directive_interpretation": [
    {
      "note_index": 0,
      "applies": true,
      "directive_type": "no_discharge_window",
      "structured_adjustment": {
        "hours": [
          1,
          2,
          3
        ]
      },
      "explanation": "Battery discharging prohibited between 1 AM and 4 AM."
    },
    {
      "note_index": 1,
      "applies": false,
      "directive_type": "no_op",
      "structured_adjustment": null,
      "explanation": "This note does not affect today's energy schedule."
    }
  ],
  "hourly_plan": [
    {
      "hour": 0,
      "grid_kwh": 120.0,
      "solar_used_kwh": 0.0,
      "battery_action": "idle",
      "battery_kwh": 0.0,
      "battery_energy_after_kwh": 160.0
    },
    {
      "hour": 1,
      "grid_kwh": 110.0,
      "solar_used_kwh": 0.0,
      "battery_action": "idle",
      "battery_kwh": 0.0,
      "battery_energy_after_kwh": 160.0
    },
    {
      "hour": 2,
      "grid_kwh": 185.0,
      "solar_used_kwh": 0.0,
      "battery_action": "charge",
      "battery_kwh": 80.0,
      "battery_energy_after_kwh": 240.0
    },
    {
      "hour": 3,
      "grid_kwh": 180.0,
      "solar_used_kwh": 0.0,
      "battery_action": "charge",
      "battery_kwh": 80.0,
      "battery_energy_after_kwh": 320.0
    },
    {
      "hour": 4,
      "grid_kwh": 190.0,
      "solar_used_kwh": 0.0,
      "battery_action": "charge",
      "battery_kwh": 80.0,
      "battery_energy_after_kwh": 400.0
    },
    {
      "hour": 5,
      "grid_kwh": 130.0,
      "solar_used_kwh": 0.0,
      "battery_action": "idle",
      "battery_kwh": 0.0,
      "battery_energy_after_kwh": 400.0
    },
    {
      "hour": 6,
      "grid_kwh": 160.0,
      "solar_used_kwh": 10.0,
      "battery_action": "idle",
      "battery_kwh": 0.0,
      "battery_energy_after_kwh": 400.0
    },
    {
      "hour": 7,
      "grid_kwh": 180.0,
      "solar_used_kwh": 40.0,
      "battery_action": "idle",
      "battery_kwh": 0.0,
      "battery_energy_after_kwh": 400.0
    },
    {
      "hour": 8,
      "grid_kwh": 180.0,
      "solar_used_kwh": 100.0,
      "battery_action": "idle",
      "battery_kwh": 0.0,
      "battery_energy_after_kwh": 400.0
    },
    {
      "hour": 9,
      "grid_kwh": 50.0,
      "solar_used_kwh": 180.0,
      "battery_action": "discharge",
      "battery_kwh": 80.0,
      "battery_energy_after_kwh": 320.0
    },
    {
      "hour": 10,
      "grid_kwh": 10.0,
      "solar_used_kwh": 240.0,
      "battery_action": "discharge",
      "battery_kwh": 80.0,
      "battery_energy_after_kwh": 240.0
    },
    {
      "hour": 11,
      "grid_kwh": 0.0,
      "solar_used_kwh": 280.0,
      "battery_action": "discharge",
      "battery_kwh": 70.0,
      "battery_energy_after_kwh": 170.0
    },
    {
      "hour": 12,
      "grid_kwh": 0.0,
      "solar_used_kwh": 300.0,
      "battery_action": "discharge",
      "battery_kwh": 40.0,
      "battery_energy_after_kwh": 130.0
    },
    {
      "hour": 13,
      "grid_kwh": 50.0,
      "solar_used_kwh": 270.0,
      "battery_action": "idle",
      "battery_kwh": 0.0,
      "battery_energy_after_kwh": 130.0
    },
    {
      "hour": 14,
      "grid_kwh": 150.0,
      "solar_used_kwh": 220.0,
      "battery_action": "charge",
      "battery_kwh": 70.0,
      "battery_energy_after_kwh": 200.0
    },
    {
      "hour": 15,
      "grid_kwh": 210.0,
      "solar_used_kwh": 150.0,
      "battery_action": "charge",
      "battery_kwh": 80.0,
      "battery_energy_after_kwh": 280.0
    },
    {
      "hour": 16,
      "grid_kwh": 260.0,
      "solar_used_kwh": 80.0,
      "battery_action": "charge",
      "battery_kwh": 80.0,
      "battery_energy_after_kwh": 360.0
    },
    {
      "hour": 17,
      "grid_kwh": 190.0,
      "solar_used_kwh": 20.0,
      "battery_action": "discharge",
      "battery_kwh": 80.0,
      "battery_energy_after_kwh": 280.0
    },
    {
      "hour": 18,
      "grid_kwh": 250.0,
      "solar_used_kwh": 0.0,
      "battery_action": "discharge",
      "battery_kwh": 80.0,
      "battery_energy_after_kwh": 200.0
    },
    {
      "hour": 19,
      "grid_kwh": 230.0,
      "solar_used_kwh": 0.0,
      "battery_action": "discharge",
      "battery_kwh": 80.0,
      "battery_energy_after_kwh": 120.0
    },
    {
      "hour": 20,
      "grid_kwh": 180.0,
      "solar_used_kwh": 0.0,
      "battery_action": "discharge",
      "battery_kwh": 80.0,
      "battery_energy_after_kwh": 40.0
    },
    {
      "hour": 21,
      "grid_kwh": 210.0,
      "solar_used_kwh": 0.0,
      "battery_action": "idle",
      "battery_kwh": 0.0,
      "battery_energy_after_kwh": 40.0
    },
    {
      "hour": 22,
      "grid_kwh": 210.0,
      "solar_used_kwh": 0.0,
      "battery_action": "charge",
      "battery_kwh": 40.0,
      "battery_energy_after_kwh": 80.0
    },
    {
      "hour": 23,
      "grid_kwh": 220.0,
      "solar_used_kwh": 0.0,
      "battery_action": "charge",
      "battery_kwh": 80.0,
      "battery_energy_after_kwh": 160.0
    }
  ],
  "total_grid_kwh": 3655.0,
  "total_cost_bdt": 35110.0,
  "peak_grid_kwh": 260.0,
  "plan_summary": "Optimized schedule for GRID-SCENARIO-08. Applied 1 active directive(s). Grid import: 3655.00 kWh, Total cost: 35110.00 BDT, Peak load: 260.00 kWh."
}
```
</details>

---

## Scenario 09: Cloudburst Panel Washing & High Evening Reserve (`GRID-SCENARIO-09`)

**Description**: Tests paraphrased solar reduction note with elevated evening emergency reserve floor.

### Operational Notes:
- *"Panel washing from one until three will leave roughly one-fifth of normal solar output."*
- *"Keep at least 200 kWh in reserve from 7 PM until 10 PM."*

### Active Directives Applied:
- **`solar_reduction`**: `{"hours": [13, 14], "factor": 0.2}` — *Solar availability reduced to 20% between 1 PM and 3 PM.*
- **`minimum_battery_reserve`**: `{"hours": [19, 20, 21], "minimum_energy_kwh": 200.0}` — *Keep at least 200 kWh in reserve between 7 PM and 10 PM.*

### Key Financial & Grid Results:
- **Total Grid Electricity Imported**: `3769.80 kWh`
- **Total Electricity Cost**: `38162.64 BDT`
- **Peak Hourly Grid Load**: `290.00 kWh`
- **Battery Capacity & State**: Capacity = `500.0 kWh`, Initial/Final SoC = `200.0 kWh` *(End-of-day neutrality verified)*

<details>
<summary><strong>Click to expand Full HTTP Request JSON (POST /optimize-energy)</strong></summary>

```json
{
  "scenario_id": "GRID-SCENARIO-09",
  "operator_notes": [
    "Panel washing from one until three will leave roughly one-fifth of normal solar output.",
    "Keep at least 200 kWh in reserve from 7 PM until 10 PM."
  ],
  "hours": [
    {
      "hour": 0,
      "demand_kwh": 114.0,
      "solar_kwh": 0.0,
      "tariff_bdt_per_kwh": 6.83
    },
    {
      "hour": 1,
      "demand_kwh": 104.5,
      "solar_kwh": 0.0,
      "tariff_bdt_per_kwh": 6.83
    },
    {
      "hour": 2,
      "demand_kwh": 99.8,
      "solar_kwh": 0.0,
      "tariff_bdt_per_kwh": 6.3
    },
    {
      "hour": 3,
      "demand_kwh": 95.0,
      "solar_kwh": 0.0,
      "tariff_bdt_per_kwh": 6.3
    },
    {
      "hour": 4,
      "demand_kwh": 104.5,
      "solar_kwh": 0.0,
      "tariff_bdt_per_kwh": 6.3
    },
    {
      "hour": 5,
      "demand_kwh": 123.5,
      "solar_kwh": 0.0,
      "tariff_bdt_per_kwh": 7.35
    },
    {
      "hour": 6,
      "demand_kwh": 161.5,
      "solar_kwh": 10.0,
      "tariff_bdt_per_kwh": 8.4
    },
    {
      "hour": 7,
      "demand_kwh": 209.0,
      "solar_kwh": 40.0,
      "tariff_bdt_per_kwh": 9.97
    },
    {
      "hour": 8,
      "demand_kwh": 266.0,
      "solar_kwh": 100.0,
      "tariff_bdt_per_kwh": 11.55
    },
    {
      "hour": 9,
      "demand_kwh": 294.5,
      "solar_kwh": 180.0,
      "tariff_bdt_per_kwh": 12.6
    },
    {
      "hour": 10,
      "demand_kwh": 313.5,
      "solar_kwh": 240.0,
      "tariff_bdt_per_kwh": 12.6
    },
    {
      "hour": 11,
      "demand_kwh": 332.5,
      "solar_kwh": 280.0,
      "tariff_bdt_per_kwh": 12.6
    },
    {
      "hour": 12,
      "demand_kwh": 323.0,
      "solar_kwh": 300.0,
      "tariff_bdt_per_kwh": 12.08
    },
    {
      "hour": 13,
      "demand_kwh": 304.0,
      "solar_kwh": 270.0,
      "tariff_bdt_per_kwh": 11.55
    },
    {
      "hour": 14,
      "demand_kwh": 285.0,
      "solar_kwh": 220.0,
      "tariff_bdt_per_kwh": 11.55
    },
    {
      "hour": 15,
      "demand_kwh": 266.0,
      "solar_kwh": 150.0,
      "tariff_bdt_per_kwh": 11.03
    },
    {
      "hour": 16,
      "demand_kwh": 247.0,
      "solar_kwh": 80.0,
      "tariff_bdt_per_kwh": 10.5
    },
    {
      "hour": 17,
      "demand_kwh": 275.5,
      "solar_kwh": 20.0,
      "tariff_bdt_per_kwh": 13.12
    },
    {
      "hour": 18,
      "demand_kwh": 313.5,
      "solar_kwh": 0.0,
      "tariff_bdt_per_kwh": 14.7
    },
    {
      "hour": 19,
      "demand_kwh": 294.5,
      "solar_kwh": 0.0,
      "tariff_bdt_per_kwh": 14.7
    },
    {
      "hour": 20,
      "demand_kwh": 247.0,
      "solar_kwh": 0.0,
      "tariff_bdt_per_kwh": 12.6
    },
    {
      "hour": 21,
      "demand_kwh": 199.5,
      "solar_kwh": 0.0,
      "tariff_bdt_per_kwh": 10.5
    },
    {
      "hour": 22,
      "demand_kwh": 161.5,
      "solar_kwh": 0.0,
      "tariff_bdt_per_kwh": 8.93
    },
    {
      "hour": 23,
      "demand_kwh": 133.0,
      "solar_kwh": 0.0,
      "tariff_bdt_per_kwh": 7.35
    }
  ],
  "battery": {
    "capacity_kwh": 500.0,
    "initial_energy_kwh": 200.0,
    "minimum_energy_kwh": 50.0,
    "max_charge_kwh_per_hour": 100.0,
    "max_discharge_kwh_per_hour": 100.0
  }
}
```
</details>

<details open>
<summary><strong>Full HTTP 200 Response JSON</strong></summary>

```json
{
  "scenario_id": "GRID-SCENARIO-09",
  "directive_interpretation": [
    {
      "note_index": 0,
      "applies": true,
      "directive_type": "solar_reduction",
      "structured_adjustment": {
        "hours": [
          13,
          14
        ],
        "factor": 0.2
      },
      "explanation": "Solar availability reduced to 20% between 1 PM and 3 PM."
    },
    {
      "note_index": 1,
      "applies": true,
      "directive_type": "minimum_battery_reserve",
      "structured_adjustment": {
        "hours": [
          19,
          20,
          21
        ],
        "minimum_energy_kwh": 200.0
      },
      "explanation": "Keep at least 200 kWh in reserve between 7 PM and 10 PM."
    }
  ],
  "hourly_plan": [
    {
      "hour": 0,
      "grid_kwh": 114.0,
      "solar_used_kwh": 0.0,
      "battery_action": "idle",
      "battery_kwh": 0.0,
      "battery_energy_after_kwh": 200.0
    },
    {
      "hour": 1,
      "grid_kwh": 104.5,
      "solar_used_kwh": 0.0,
      "battery_action": "idle",
      "battery_kwh": 0.0,
      "battery_energy_after_kwh": 200.0
    },
    {
      "hour": 2,
      "grid_kwh": 199.8,
      "solar_used_kwh": 0.0,
      "battery_action": "charge",
      "battery_kwh": 100.0,
      "battery_energy_after_kwh": 300.0
    },
    {
      "hour": 3,
      "grid_kwh": 195.0,
      "solar_used_kwh": 0.0,
      "battery_action": "charge",
      "battery_kwh": 100.0,
      "battery_energy_after_kwh": 400.0
    },
    {
      "hour": 4,
      "grid_kwh": 204.5,
      "solar_used_kwh": 0.0,
      "battery_action": "charge",
      "battery_kwh": 100.0,
      "battery_energy_after_kwh": 500.0
    },
    {
      "hour": 5,
      "grid_kwh": 123.5,
      "solar_used_kwh": 0.0,
      "battery_action": "idle",
      "battery_kwh": 0.0,
      "battery_energy_after_kwh": 500.0
    },
    {
      "hour": 6,
      "grid_kwh": 151.5,
      "solar_used_kwh": 10.0,
      "battery_action": "idle",
      "battery_kwh": 0.0,
      "battery_energy_after_kwh": 500.0
    },
    {
      "hour": 7,
      "grid_kwh": 169.0,
      "solar_used_kwh": 40.0,
      "battery_action": "idle",
      "battery_kwh": 0.0,
      "battery_energy_after_kwh": 500.0
    },
    {
      "hour": 8,
      "grid_kwh": 166.0,
      "solar_used_kwh": 100.0,
      "battery_action": "idle",
      "battery_kwh": 0.0,
      "battery_energy_after_kwh": 500.0
    },
    {
      "hour": 9,
      "grid_kwh": 14.5,
      "solar_used_kwh": 180.0,
      "battery_action": "discharge",
      "battery_kwh": 100.0,
      "battery_energy_after_kwh": 400.0
    },
    {
      "hour": 10,
      "grid_kwh": 0.0,
      "solar_used_kwh": 240.0,
      "battery_action": "discharge",
      "battery_kwh": 73.5,
      "battery_energy_after_kwh": 326.5
    },
    {
      "hour": 11,
      "grid_kwh": 0.0,
      "solar_used_kwh": 280.0,
      "battery_action": "discharge",
      "battery_kwh": 52.5,
      "battery_energy_after_kwh": 274.0
    },
    {
      "hour": 12,
      "grid_kwh": 0.0,
      "solar_used_kwh": 300.0,
      "battery_action": "discharge",
      "battery_kwh": 23.0,
      "battery_energy_after_kwh": 251.0
    },
    {
      "hour": 13,
      "grid_kwh": 250.0,
      "solar_used_kwh": 54.0,
      "battery_action": "idle",
      "battery_kwh": 0.0,
      "battery_energy_after_kwh": 251.0
    },
    {
      "hour": 14,
      "grid_kwh": 290.0,
      "solar_used_kwh": 44.0,
      "battery_action": "charge",
      "battery_kwh": 49.0,
      "battery_energy_after_kwh": 300.0
    },
    {
      "hour": 15,
      "grid_kwh": 216.0,
      "solar_used_kwh": 150.0,
      "battery_action": "charge",
      "battery_kwh": 100.0,
      "battery_energy_after_kwh": 400.0
    },
    {
      "hour": 16,
      "grid_kwh": 267.0,
      "solar_used_kwh": 80.0,
      "battery_action": "charge",
      "battery_kwh": 100.0,
      "battery_energy_after_kwh": 500.0
    },
    {
      "hour": 17,
      "grid_kwh": 155.5,
      "solar_used_kwh": 20.0,
      "battery_action": "discharge",
      "battery_kwh": 100.0,
      "battery_energy_after_kwh": 400.0
    },
    {
      "hour": 18,
      "grid_kwh": 213.5,
      "solar_used_kwh": 0.0,
      "battery_action": "discharge",
      "battery_kwh": 100.0,
      "battery_energy_after_kwh": 300.0
    },
    {
      "hour": 19,
      "grid_kwh": 194.5,
      "solar_used_kwh": 0.0,
      "battery_action": "discharge",
      "battery_kwh": 100.0,
      "battery_energy_after_kwh": 200.0
    },
    {
      "hour": 20,
      "grid_kwh": 247.0,
      "solar_used_kwh": 0.0,
      "battery_action": "idle",
      "battery_kwh": 0.0,
      "battery_energy_after_kwh": 200.0
    },
    {
      "hour": 21,
      "grid_kwh": 199.5,
      "solar_used_kwh": 0.0,
      "battery_action": "idle",
      "battery_kwh": 0.0,
      "battery_energy_after_kwh": 200.0
    },
    {
      "hour": 22,
      "grid_kwh": 61.5,
      "solar_used_kwh": 0.0,
      "battery_action": "discharge",
      "battery_kwh": 100.0,
      "battery_energy_after_kwh": 100.0
    },
    {
      "hour": 23,
      "grid_kwh": 233.0,
      "solar_used_kwh": 0.0,
      "battery_action": "charge",
      "battery_kwh": 100.0,
      "battery_energy_after_kwh": 200.0
    }
  ],
  "total_grid_kwh": 3769.8,
  "total_cost_bdt": 38162.64,
  "peak_grid_kwh": 290.0,
  "plan_summary": "Optimized schedule for GRID-SCENARIO-09. Applied 2 active directive(s). Grid import: 3769.80 kWh, Total cost: 38162.64 BDT, Peak load: 290.00 kWh."
}
```
</details>

---

## Scenario 10: All-Distractors Pure Economic Dispatch (`GRID-SCENARIO-10`)

**Description**: Verifies safe fallback handling when multiple notes are sent, but none contain actionable energy constraints.

### Operational Notes:
- *"The cafeteria menu changes tomorrow."*
- *"Campus sports complex closed for annual floor polishing."*

### Active Directives Applied: *None (Pure Economic Dispatch)*

### Key Financial & Grid Results:
- **Total Grid Electricity Imported**: `3655.00 kWh`
- **Total Electricity Cost**: `34475.00 BDT`
- **Peak Hourly Grid Load**: `280.00 kWh`
- **Battery Capacity & State**: Capacity = `500.0 kWh`, Initial/Final SoC = `200.0 kWh` *(End-of-day neutrality verified)*

<details>
<summary><strong>Click to expand Full HTTP Request JSON (POST /optimize-energy)</strong></summary>

```json
{
  "scenario_id": "GRID-SCENARIO-10",
  "operator_notes": [
    "The cafeteria menu changes tomorrow.",
    "Campus sports complex closed for annual floor polishing."
  ],
  "hours": [
    {
      "hour": 0,
      "demand_kwh": 120.0,
      "solar_kwh": 0.0,
      "tariff_bdt_per_kwh": 6.5
    },
    {
      "hour": 1,
      "demand_kwh": 110.0,
      "solar_kwh": 0.0,
      "tariff_bdt_per_kwh": 6.5
    },
    {
      "hour": 2,
      "demand_kwh": 105.0,
      "solar_kwh": 0.0,
      "tariff_bdt_per_kwh": 6.0
    },
    {
      "hour": 3,
      "demand_kwh": 100.0,
      "solar_kwh": 0.0,
      "tariff_bdt_per_kwh": 6.0
    },
    {
      "hour": 4,
      "demand_kwh": 110.0,
      "solar_kwh": 0.0,
      "tariff_bdt_per_kwh": 6.0
    },
    {
      "hour": 5,
      "demand_kwh": 130.0,
      "solar_kwh": 0.0,
      "tariff_bdt_per_kwh": 7.0
    },
    {
      "hour": 6,
      "demand_kwh": 170.0,
      "solar_kwh": 10.0,
      "tariff_bdt_per_kwh": 8.0
    },
    {
      "hour": 7,
      "demand_kwh": 220.0,
      "solar_kwh": 40.0,
      "tariff_bdt_per_kwh": 9.5
    },
    {
      "hour": 8,
      "demand_kwh": 280.0,
      "solar_kwh": 100.0,
      "tariff_bdt_per_kwh": 11.0
    },
    {
      "hour": 9,
      "demand_kwh": 310.0,
      "solar_kwh": 180.0,
      "tariff_bdt_per_kwh": 12.0
    },
    {
      "hour": 10,
      "demand_kwh": 330.0,
      "solar_kwh": 240.0,
      "tariff_bdt_per_kwh": 12.0
    },
    {
      "hour": 11,
      "demand_kwh": 350.0,
      "solar_kwh": 280.0,
      "tariff_bdt_per_kwh": 12.0
    },
    {
      "hour": 12,
      "demand_kwh": 340.0,
      "solar_kwh": 300.0,
      "tariff_bdt_per_kwh": 11.5
    },
    {
      "hour": 13,
      "demand_kwh": 320.0,
      "solar_kwh": 270.0,
      "tariff_bdt_per_kwh": 11.0
    },
    {
      "hour": 14,
      "demand_kwh": 300.0,
      "solar_kwh": 220.0,
      "tariff_bdt_per_kwh": 11.0
    },
    {
      "hour": 15,
      "demand_kwh": 280.0,
      "solar_kwh": 150.0,
      "tariff_bdt_per_kwh": 10.5
    },
    {
      "hour": 16,
      "demand_kwh": 260.0,
      "solar_kwh": 80.0,
      "tariff_bdt_per_kwh": 10.0
    },
    {
      "hour": 17,
      "demand_kwh": 290.0,
      "solar_kwh": 20.0,
      "tariff_bdt_per_kwh": 12.5
    },
    {
      "hour": 18,
      "demand_kwh": 330.0,
      "solar_kwh": 0.0,
      "tariff_bdt_per_kwh": 14.0
    },
    {
      "hour": 19,
      "demand_kwh": 310.0,
      "solar_kwh": 0.0,
      "tariff_bdt_per_kwh": 14.0
    },
    {
      "hour": 20,
      "demand_kwh": 260.0,
      "solar_kwh": 0.0,
      "tariff_bdt_per_kwh": 12.0
    },
    {
      "hour": 21,
      "demand_kwh": 210.0,
      "solar_kwh": 0.0,
      "tariff_bdt_per_kwh": 10.0
    },
    {
      "hour": 22,
      "demand_kwh": 170.0,
      "solar_kwh": 0.0,
      "tariff_bdt_per_kwh": 8.5
    },
    {
      "hour": 23,
      "demand_kwh": 140.0,
      "solar_kwh": 0.0,
      "tariff_bdt_per_kwh": 7.0
    }
  ],
  "battery": {
    "capacity_kwh": 500.0,
    "initial_energy_kwh": 200.0,
    "minimum_energy_kwh": 50.0,
    "max_charge_kwh_per_hour": 100.0,
    "max_discharge_kwh_per_hour": 100.0
  }
}
```
</details>

<details open>
<summary><strong>Full HTTP 200 Response JSON</strong></summary>

```json
{
  "scenario_id": "GRID-SCENARIO-10",
  "directive_interpretation": [
    {
      "note_index": 0,
      "applies": false,
      "directive_type": "no_op",
      "structured_adjustment": null,
      "explanation": "This note does not affect today's energy schedule."
    },
    {
      "note_index": 1,
      "applies": false,
      "directive_type": "no_op",
      "structured_adjustment": null,
      "explanation": "This note does not affect today's energy schedule."
    }
  ],
  "hourly_plan": [
    {
      "hour": 0,
      "grid_kwh": 120.0,
      "solar_used_kwh": 0.0,
      "battery_action": "idle",
      "battery_kwh": 0.0,
      "battery_energy_after_kwh": 200.0
    },
    {
      "hour": 1,
      "grid_kwh": 110.0,
      "solar_used_kwh": 0.0,
      "battery_action": "idle",
      "battery_kwh": 0.0,
      "battery_energy_after_kwh": 200.0
    },
    {
      "hour": 2,
      "grid_kwh": 205.0,
      "solar_used_kwh": 0.0,
      "battery_action": "charge",
      "battery_kwh": 100.0,
      "battery_energy_after_kwh": 300.0
    },
    {
      "hour": 3,
      "grid_kwh": 200.0,
      "solar_used_kwh": 0.0,
      "battery_action": "charge",
      "battery_kwh": 100.0,
      "battery_energy_after_kwh": 400.0
    },
    {
      "hour": 4,
      "grid_kwh": 210.0,
      "solar_used_kwh": 0.0,
      "battery_action": "charge",
      "battery_kwh": 100.0,
      "battery_energy_after_kwh": 500.0
    },
    {
      "hour": 5,
      "grid_kwh": 130.0,
      "solar_used_kwh": 0.0,
      "battery_action": "idle",
      "battery_kwh": 0.0,
      "battery_energy_after_kwh": 500.0
    },
    {
      "hour": 6,
      "grid_kwh": 160.0,
      "solar_used_kwh": 10.0,
      "battery_action": "idle",
      "battery_kwh": 0.0,
      "battery_energy_after_kwh": 500.0
    },
    {
      "hour": 7,
      "grid_kwh": 180.0,
      "solar_used_kwh": 40.0,
      "battery_action": "idle",
      "battery_kwh": 0.0,
      "battery_energy_after_kwh": 500.0
    },
    {
      "hour": 8,
      "grid_kwh": 180.0,
      "solar_used_kwh": 100.0,
      "battery_action": "idle",
      "battery_kwh": 0.0,
      "battery_energy_after_kwh": 500.0
    },
    {
      "hour": 9,
      "grid_kwh": 30.0,
      "solar_used_kwh": 180.0,
      "battery_action": "discharge",
      "battery_kwh": 100.0,
      "battery_energy_after_kwh": 400.0
    },
    {
      "hour": 10,
      "grid_kwh": 0.0,
      "solar_used_kwh": 240.0,
      "battery_action": "discharge",
      "battery_kwh": 90.0,
      "battery_energy_after_kwh": 310.0
    },
    {
      "hour": 11,
      "grid_kwh": 0.0,
      "solar_used_kwh": 280.0,
      "battery_action": "discharge",
      "battery_kwh": 70.0,
      "battery_energy_after_kwh": 240.0
    },
    {
      "hour": 12,
      "grid_kwh": 0.0,
      "solar_used_kwh": 300.0,
      "battery_action": "discharge",
      "battery_kwh": 40.0,
      "battery_energy_after_kwh": 200.0
    },
    {
      "hour": 13,
      "grid_kwh": 100.0,
      "solar_used_kwh": 270.0,
      "battery_action": "charge",
      "battery_kwh": 50.0,
      "battery_energy_after_kwh": 250.0
    },
    {
      "hour": 14,
      "grid_kwh": 80.0,
      "solar_used_kwh": 220.0,
      "battery_action": "idle",
      "battery_kwh": 0.0,
      "battery_energy_after_kwh": 250.0
    },
    {
      "hour": 15,
      "grid_kwh": 230.0,
      "solar_used_kwh": 150.0,
      "battery_action": "charge",
      "battery_kwh": 100.0,
      "battery_energy_after_kwh": 350.0
    },
    {
      "hour": 16,
      "grid_kwh": 280.0,
      "solar_used_kwh": 80.0,
      "battery_action": "charge",
      "battery_kwh": 100.0,
      "battery_energy_after_kwh": 450.0
    },
    {
      "hour": 17,
      "grid_kwh": 170.0,
      "solar_used_kwh": 20.0,
      "battery_action": "discharge",
      "battery_kwh": 100.0,
      "battery_energy_after_kwh": 350.0
    },
    {
      "hour": 18,
      "grid_kwh": 230.0,
      "solar_used_kwh": 0.0,
      "battery_action": "discharge",
      "battery_kwh": 100.0,
      "battery_energy_after_kwh": 250.0
    },
    {
      "hour": 19,
      "grid_kwh": 210.0,
      "solar_used_kwh": 0.0,
      "battery_action": "discharge",
      "battery_kwh": 100.0,
      "battery_energy_after_kwh": 150.0
    },
    {
      "hour": 20,
      "grid_kwh": 160.0,
      "solar_used_kwh": 0.0,
      "battery_action": "discharge",
      "battery_kwh": 100.0,
      "battery_energy_after_kwh": 50.0
    },
    {
      "hour": 21,
      "grid_kwh": 210.0,
      "solar_used_kwh": 0.0,
      "battery_action": "idle",
      "battery_kwh": 0.0,
      "battery_energy_after_kwh": 50.0
    },
    {
      "hour": 22,
      "grid_kwh": 220.0,
      "solar_used_kwh": 0.0,
      "battery_action": "charge",
      "battery_kwh": 50.0,
      "battery_energy_after_kwh": 100.0
    },
    {
      "hour": 23,
      "grid_kwh": 240.0,
      "solar_used_kwh": 0.0,
      "battery_action": "charge",
      "battery_kwh": 100.0,
      "battery_energy_after_kwh": 200.0
    }
  ],
  "total_grid_kwh": 3655.0,
  "total_cost_bdt": 34475.0,
  "peak_grid_kwh": 280.0,
  "plan_summary": "Optimized schedule for GRID-SCENARIO-10. Applied 0 active directive(s). Grid import: 3655.00 kWh, Total cost: 34475.00 BDT, Peak load: 280.00 kWh."
}
```
</details>

---
