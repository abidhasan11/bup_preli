# Smart Campus Energy Optimization Challenge (GridWise LLM)
## Complete Input & Output Specification Reference Guide

> **Document Purpose**: Canonical reference for all HTTP requests, responses, data schemas, validation constraints, data types, and concrete examples for the BUP CSE Fest 2026 Hackathon Preliminary Round.

---

## Table of Contents
1. [Endpoint Overview](#1-endpoint-overview)
2. [Health Check Endpoint (`GET /health`)](#2-health-check-endpoint-get-health)
3. [Main Optimization Endpoint (`POST /optimize-energy`)](#3-main-optimization-endpoint-post-optimize-energy)
4. [Detailed Request Schema & Fields](#4-detailed-request-schema--fields)
5. [Detailed Response Schema & Fields](#5-detailed-response-schema--fields)
6. [Operator Directives Input-Output Mapping Reference](#6-operator-directives-input-output-mapping-reference)
7. [Full 24-Hour End-to-End Example](#7-full-24-hour-end-to-end-example)
8. [Error Responses & Status Codes](#8-error-responses--status-codes)
9. [Validation Constraints & Precision Rules](#9-validation-constraints--precision-rules)

---

## 1. Endpoint Overview

| Method | Route | Purpose | Expected Status Codes |
|---|---|---|---|
| `GET` | `/health` | Service liveness and readiness probe | `200` |
| `POST` | `/optimize-energy` | Ingests 24h scenario + operator notes; returns parsed directives and optimal schedule | `200`, `400`, `422`, `500` |

---

## 2. Health Check Endpoint (`GET /health`)

Used by the automated judge harness to ensure your service is alive before sending benchmark scenarios.

### 2.1 Request
- **Method**: `GET`
- **Path**: `/health`
- **Headers**: None required
- **Body**: None

### 2.2 Response
- **Status Code**: `200 OK`
- **Content-Type**: `application/json`
- **Body Schema**:
```json
{
  "status": "ok"
}
```

---

## 3. Main Optimization Endpoint (`POST /optimize-energy`)

### 3.1 HTTP Headers
```http
POST /optimize-energy HTTP/1.1
Host: <your-service-host>
Content-Type: application/json
Accept: application/json
```

---

## 4. Detailed Request Schema & Fields

### 4.1 Top-Level Request Structure

```typescript
interface ScenarioRequest {
  scenario_id: string;             // Unique identifier for the scenario
  operator_notes: string[];        // 1 to 3 natural language operator directives
  hours: HourInput[];              // Exactly 24 hourly entries (hours 0 through 23)
  battery: BatterySpecs;           // Battery hardware specifications & initial state
}
```

### 4.2 Field-by-Field Reference (Request)

| JSON Key | Type | Constraints | Description |
|---|---|---|---|
| `scenario_id` | `string` | Non-empty | Unique identifier provided by the test harness (e.g., `"GRID-101"`). Must be reflected identically in response. |
| `operator_notes` | `array[string]` | Length $1 \le N \le 3$, non-empty strings | Raw human operator notes describing temporary constraints or distractor notices. |
| `hours` | `array[object]` | Exactly 24 entries | Array of hourly forecast data for hours $0 \dots 23$. Must be ordered sequentially. |
| `battery` | `object` | All values $\ge 0$ | Object specifying battery capacity, starting energy, reserve levels, and hourly limits. |

### 4.3 `hours` Array Element (`HourInput`)

```typescript
interface HourInput {
  hour: number;                    // Integer: 0 to 23
  demand_kwh: number;              // Float >= 0: Campus electricity demand in this hour
  solar_kwh: number;               // Float >= 0: Rooftop solar generation available
  tariff_bdt_per_kwh: number;      // Float >= 0: Grid electricity price for this hour
}
```

| Field | Type | Bounds | Description |
|---|---|---|---|
| `hour` | `integer` | $0 \le \text{hour} \le 23$ | Sequential hour index. |
| `demand_kwh` | `number` | $\ge 0.0$ | Campus electricity demand (kWh) that must be satisfied. |
| `solar_kwh` | `number` | $\ge 0.0$ | Expected baseline solar PV power output (kWh) before operator directives. |
| `tariff_bdt_per_kwh` | `number` | $\ge 0.0$ | Utility price in Bangladeshi Taka (BDT) per kWh imported from the grid. |

### 4.4 `battery` Object (`BatterySpecs`)

```typescript
interface BatterySpecs {
  capacity_kwh: number;                // Maximum storage capacity (kWh)
  initial_energy_kwh: number;          // Energy stored at start of hour 0 (kWh)
  minimum_energy_kwh: number;          // Hard minimum reserve floor (kWh)
  max_charge_kwh_per_hour: number;     // Maximum energy chargeable in 1 hour (kWh)
  max_discharge_kwh_per_hour: number;  // Maximum energy dischargeable in 1 hour (kWh)
}
```

| Field | Type | Bounds | Description |
|---|---|---|---|
| `capacity_kwh` | `number` | $> 0.0$ | Total nameplate energy capacity of the battery. |
| `initial_energy_kwh` | `number` | $0.0 \le \text{initial} \le \text{capacity}$ | Battery state of charge (SoC) at beginning of planning horizon (hour 0). |
| `minimum_energy_kwh` | `number` | $0.0 \le \text{min} \le \text{capacity}$ | Base safety reserve floor that the battery must never breach. |
| `max_charge_kwh_per_hour` | `number` | $\ge 0.0$ | Peak charging power limit per 1-hour interval. |
| `max_discharge_kwh_per_hour` | `number` | $\ge 0.0$ | Peak discharging power limit per 1-hour interval. |

---

## 5. Detailed Response Schema & Fields

### 5.1 Top-Level Response Structure

```typescript
interface ScenarioResponse {
  scenario_id: string;                                // Matches request scenario_id
  directive_interpretation: DirectiveInterpretation[]; // Exactly 1 item per operator note
  hourly_plan: HourlyPlanEntry[];                      // Exactly 24 hourly schedule entries
  total_grid_kwh: number;                             // Total grid electricity imported (sum)
  total_cost_bdt: number;                             // Total electricity cost (sum of grid * tariff)
  peak_grid_kwh: number;                              // Maximum single-hour grid import
  plan_summary: string;                               // Brief summary of optimization strategy
}
```

### 5.2 Field-by-Field Reference (Response)

| JSON Key | Type | Requirement / Constraint | Description |
|---|---|---|---|
| `scenario_id` | `string` | Exact match with request | Identifies the scenario. |
| `directive_interpretation` | `array[object]` | Length equals `len(operator_notes)` | Parsed machine-readable directives ordered by `note_index` $0 \dots N-1$. |
| `hourly_plan` | `array[object]` | Exactly 24 entries ($0 \dots 23$) | Complete hour-by-hour operational dispatch plan. |
| `total_grid_kwh` | `number` | $\sum_{h=0}^{23} \text{grid\_kwh}[h]$ | Total energy purchased from the utility grid across 24 hours. |
| `total_cost_bdt` | `number` | $\sum_{h=0}^{23} (\text{grid\_kwh}[h] \times \text{tariff}[h])$ | Total financial cost in BDT. |
| `peak_grid_kwh` | `number` | $\max_{h=0}^{23} \text{grid\_kwh}[h]$ | Highest single-hour grid energy purchase. |
| `plan_summary` | `string` | Non-empty string | Human-readable strategy explanation. |

### 5.3 `directive_interpretation` Array Element

```typescript
interface DirectiveInterpretation {
  note_index: number;              // 0-based index matching input note position
  applies: boolean;                // true for active directives, false ONLY for no_op
  directive_type: DirectiveType;   // One of the 6 canonical directive types
  structured_adjustment: object | null; // Structured payload or null for no_op
  explanation: string;             // Short rationale
}

type DirectiveType = 
  | "solar_reduction"
  | "minimum_battery_reserve"
  | "no_charge_window"
  | "no_discharge_window"
  | "max_grid_window"
  | "no_op";
```

| Field | Type | Permitted Values | Meaning |
|---|---|---|---|
| `note_index` | `integer` | $0, 1, \dots, N-1$ | Zero-based index of the corresponding operator note in `operator_notes`. Must appear in order. |
| `applies` | `boolean` | `true` or `false` | Must be `true` for all actionable directives. **Must be `false` if and only if `directive_type == "no_op"`**. |
| `directive_type` | `string` | Canonical 6 types | The classification of the note. |
| `structured_adjustment` | `object \| null` | Strict JSON object or `null` | Machine-checkable parameters. **Must be `null` if `directive_type == "no_op"`, and non-null otherwise**. |
| `explanation` | `string` | Free text | Concise explanation of why and how this note was interpreted. |

### 5.4 `hourly_plan` Array Element

```typescript
interface HourlyPlanEntry {
  hour: number;                           // Integer: 0 to 23
  grid_kwh: number;                       // Float >= 0: Energy imported from grid
  solar_used_kwh: number;                 // Float >= 0: Solar energy consumed
  battery_action: "charge" | "discharge" | "idle"; // Discrete battery state
  battery_kwh: number;                    // Float >= 0: Action magnitude (0 if idle)
  battery_energy_after_kwh: number;       // Float: Energy level at end of this hour
}
```

| Field | Type | Permitted Values | Meaning |
|---|---|---|---|
| `hour` | `integer` | $0 \le \text{hour} \le 23$ | Sequential hour index (0 to 23). |
| `grid_kwh` | `number` | $\ge 0.0$ | Electricity purchased from the grid in this hour. |
| `solar_used_kwh` | `number` | $0.0 \le \text{used} \le \text{effective\_solar}$ | Rooftop solar energy directly utilized to serve demand or charge the battery. Unused solar is curtailed. |
| `battery_action` | `string` | `"charge"`, `"discharge"`, or `"idle"` | Exactly one of these three strings. |
| `battery_kwh` | `number` | $\ge 0.0$ | Magnitude of battery charge or discharge. **Must be exactly `0.0` when `battery_action == "idle"`**. |
| `battery_energy_after_kwh` | `number` | $\text{min\_reserve} \le E \le \text{capacity}$ | Battery energy content immediately at the completion of this hour. |

---

## 6. Operator Directives Input-Output Mapping Reference

All structured adjustments use whole-hour intervals $[start, end)$ where the **start hour is included** and the **end hour is excluded**.

| Directive Type | Input Phrase Example | `applies` | `structured_adjustment` JSON Shape | Guardrail Constraints |
|---|---|---|---|---|
| `solar_reduction` | *"Solar output will drop to about 20% from 1 PM to 3 PM."* | `true` | `{"hours": [13, 14], "factor": 0.2}` | `0.0 <= factor <= 1.0`<br>`factor` is the remaining usable solar fraction (e.g. 80% reduction means factor = 0.2). |
| `minimum_battery_reserve` | *"Keep at least 120 kWh in reserve from 6 PM until 9 PM."* | `true` | `{"hours": [18, 19, 20], "minimum_energy_kwh": 120.0}` | `0.0 <= minimum_energy_kwh <= battery.capacity_kwh` |
| `no_charge_window` | *"Do not charge the battery between 2 PM and 4 PM."* | `true` | `{"hours": [14, 15]}` | Hours must be sorted ascending unique integers $0 \dots 23$. |
| `no_discharge_window` | *"No battery discharge permitted between 05:00 and 07:00."* | `true` | `{"hours": [5, 6]}` | Hours must be sorted ascending unique integers $0 \dots 23$. |
| `max_grid_window` | *"Grid import capped at 40 kWh from 8 AM to 11 AM due to substation line maintenance."* | `true` | `{"hours": [8, 9, 10], "max_grid_kwh": 40.0}` | `max_grid_kwh >= 0.0` |
| `no_op` | *"The cafeteria menu changes tomorrow."* | `false` | `null` | Must always set `applies: false` and `structured_adjustment: null`. |

---

## 7. Full 24-Hour End-to-End Example

### 7.1 Sample HTTP Request (`POST /optimize-energy`)

```json
{
  "scenario_id": "BUP-PRELI-SAMPLE-01",
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
```

---

### 7.2 Sample HTTP Response (`200 OK`)

```json
{
  "scenario_id": "BUP-PRELI-SAMPLE-01",
  "directive_interpretation": [
    {
      "note_index": 0,
      "applies": true,
      "directive_type": "solar_reduction",
      "structured_adjustment": {
        "hours": [13, 14],
        "factor": 0.2
      },
      "explanation": "Solar availability reduced to 20% between 1 PM and 3 PM."
    },
    {
      "note_index": 1,
      "applies": true,
      "directive_type": "no_charge_window",
      "structured_adjustment": {
        "hours": [14, 15]
      },
      "explanation": "Battery charging prohibited between 2 PM and 4 PM."
    },
    {
      "note_index": 2,
      "applies": false,
      "directive_type": "no_op",
      "structured_adjustment": null,
      "explanation": "Cafeteria operational notice is irrelevant to energy dispatch."
    }
  ],
  "hourly_plan": [
    {"hour": 0, "grid_kwh": 120.0, "solar_used_kwh": 0.0, "battery_action": "idle", "battery_kwh": 0.0, "battery_energy_after_kwh": 200.0},
    {"hour": 1, "grid_kwh": 110.0, "solar_used_kwh": 0.0, "battery_action": "idle", "battery_kwh": 0.0, "battery_energy_after_kwh": 200.0},
    {"hour": 2, "grid_kwh": 205.0, "solar_used_kwh": 0.0, "battery_action": "charge", "battery_kwh": 100.0, "battery_energy_after_kwh": 300.0},
    {"hour": 3, "grid_kwh": 200.0, "solar_used_kwh": 0.0, "battery_action": "charge", "battery_kwh": 100.0, "battery_energy_after_kwh": 400.0},
    {"hour": 4, "grid_kwh": 210.0, "solar_used_kwh": 0.0, "battery_action": "charge", "battery_kwh": 100.0, "battery_energy_after_kwh": 500.0},
    {"hour": 5, "grid_kwh": 130.0, "solar_used_kwh": 0.0, "battery_action": "idle", "battery_kwh": 0.0, "battery_energy_after_kwh": 500.0},
    {"hour": 6, "grid_kwh": 160.0, "solar_used_kwh": 10.0, "battery_action": "idle", "battery_kwh": 0.0, "battery_energy_after_kwh": 500.0},
    {"hour": 7, "grid_kwh": 180.0, "solar_used_kwh": 40.0, "battery_action": "idle", "battery_kwh": 0.0, "battery_energy_after_kwh": 500.0},
    {"hour": 8, "grid_kwh": 180.0, "solar_used_kwh": 100.0, "battery_action": "idle", "battery_kwh": 0.0, "battery_energy_after_kwh": 500.0},
    {"hour": 9, "grid_kwh": 30.0, "solar_used_kwh": 180.0, "battery_action": "discharge", "battery_kwh": 100.0, "battery_energy_after_kwh": 400.0},
    {"hour": 10, "grid_kwh": 0.0, "solar_used_kwh": 240.0, "battery_action": "discharge", "battery_kwh": 90.0, "battery_energy_after_kwh": 310.0},
    {"hour": 11, "grid_kwh": 0.0, "solar_used_kwh": 280.0, "battery_action": "discharge", "battery_kwh": 70.0, "battery_energy_after_kwh": 240.0},
    {"hour": 12, "grid_kwh": 40.0, "solar_used_kwh": 300.0, "battery_action": "idle", "battery_kwh": 0.0, "battery_energy_after_kwh": 240.0},
    {"hour": 13, "grid_kwh": 266.0, "solar_used_kwh": 54.0, "battery_action": "idle", "battery_kwh": 0.0, "battery_energy_after_kwh": 240.0},
    {"hour": 14, "grid_kwh": 256.0, "solar_used_kwh": 44.0, "battery_action": "idle", "battery_kwh": 0.0, "battery_energy_after_kwh": 240.0},
    {"hour": 15, "grid_kwh": 130.0, "solar_used_kwh": 150.0, "battery_action": "idle", "battery_kwh": 0.0, "battery_energy_after_kwh": 240.0},
    {"hour": 16, "grid_kwh": 180.0, "solar_used_kwh": 80.0, "battery_action": "idle", "battery_kwh": 0.0, "battery_energy_after_kwh": 240.0},
    {"hour": 17, "grid_kwh": 170.0, "solar_used_kwh": 20.0, "battery_action": "discharge", "battery_kwh": 100.0, "battery_energy_after_kwh": 140.0},
    {"hour": 18, "grid_kwh": 240.0, "solar_used_kwh": 0.0, "battery_action": "discharge", "battery_kwh": 90.0, "battery_energy_after_kwh": 50.0},
    {"hour": 19, "grid_kwh": 310.0, "solar_used_kwh": 0.0, "battery_action": "idle", "battery_kwh": 0.0, "battery_energy_after_kwh": 50.0},
    {"hour": 20, "grid_kwh": 260.0, "solar_used_kwh": 0.0, "battery_action": "idle", "battery_kwh": 0.0, "battery_energy_after_kwh": 50.0},
    {"hour": 21, "grid_kwh": 210.0, "solar_used_kwh": 0.0, "battery_action": "idle", "battery_kwh": 0.0, "battery_energy_after_kwh": 50.0},
    {"hour": 22, "grid_kwh": 220.0, "solar_used_kwh": 0.0, "battery_action": "charge", "battery_kwh": 50.0, "battery_energy_after_kwh": 100.0},
    {"hour": 23, "grid_kwh": 240.0, "solar_used_kwh": 0.0, "battery_action": "charge", "battery_kwh": 100.0, "battery_energy_after_kwh": 200.0}
  ],
  "total_grid_kwh": 4047.0,
  "total_cost_bdt": 39387.0,
  "peak_grid_kwh": 310.0,
  "plan_summary": "Charge battery during low-cost hours (2-4 AM, 10-11 PM) and discharge during peak tariff hours (9-11 AM, 5-7 PM), while respecting solar deratings and charge prohibition windows."
}
```

---

## 8. Error Responses & Status Codes

### 8.1 Status Codes Reference
| HTTP Status | Trigger Conditions | Example Scenario |
|---|---|---|
| **200 OK** | Successful request interpretation and optimization. | Valid scenario passed and solved. |
| **400 Bad Request** | Request body is not valid JSON, has missing top-level fields, or structural violations. | Malformed JSON string, missing `battery` object, or missing `scenario_id`. |
| **422 Unprocessable Entity** | Well-formed JSON but semantically invalid data. | `hours` array has 23 or 25 elements; `capacity_kwh <= 0`; invalid types. |
| **500 Internal Server Error** | Unexpected server-side failure. **Secrets and stack traces must never be returned**. | Unhandled runtime exception or solver timeout. |

### 8.2 Standard Error Response Payload
When returning a `400`, `422`, or `500`, adhere to a controlled error shape:
```json
{
  "detail": "Descriptive error message explaining what failed."
}
```

> [!CAUTION]
> Under no circumstances should raw Python tracebacks, API keys (`GEMINI_API_KEY`, etc.), or internal environment variables be exposed in error responses.

---

## 9. Validation Constraints & Precision Rules

### 9.1 Independent Calculation Checks
The test harness independently replays your returned `hourly_plan` using the following exact relations:

1. **Hourly Energy Balance**:
   $$\text{grid\_kwh}[h] + \text{solar\_used\_kwh}[h] + \text{discharge}[h] = \text{demand\_kwh}[h] + \text{charge}[h]$$
   - Where $\text{charge}[h] = \text{battery\_kwh}[h]$ if `battery_action == "charge"`, else $0$.
   - Where $\text{discharge}[h] = \text{battery\_kwh}[h]$ if `battery_action == "discharge"`, else $0$.

2. **Solar Ceiling**:
   $$\text{solar\_used\_kwh}[h] \le \text{effective\_solar\_kwh}[h]$$

3. **Battery Dynamics**:
   $$E[h] = E[h-1] + \text{charge}[h] - \text{discharge}[h] \quad (E[-1] = \text{initial\_energy\_kwh})$$

4. **Battery Bounds**:
   $$\text{dynamic\_minimum\_reserve}[h] \le E[h] \le \text{capacity\_kwh}$$

5. **End-of-Day Neutrality**:
   $$E[23] = \text{initial\_energy\_kwh}$$

6. **Summary Field Recalculations**:
   $$\text{total\_grid\_kwh} = \sum_{h=0}^{23} \text{grid\_kwh}[h]$$
   $$\text{total\_cost\_bdt} = \sum_{h=0}^{23} \left( \text{grid\_kwh}[h] \times \text{tariff\_bdt\_per_kwh}[h] \right)$$
   $$\text{peak\_grid\_kwh} = \max_{h=0}^{23} \text{grid\_kwh}[h]$$

### 9.2 Numeric Tolerance
Judge evaluations use an absolute numerical tolerance of:
- **$\pm 0.01$ kWh** for all energy quantities (`grid_kwh`, `solar_used_kwh`, `battery_kwh`, `battery_energy_after_kwh`, `total_grid_kwh`, `peak_grid_kwh`).
- **$\pm 0.01$ BDT** for monetary values (`total_cost_bdt`).

---
*Created for the BUP CSE Fest 2026 Hackathon (Preliminaries).*
