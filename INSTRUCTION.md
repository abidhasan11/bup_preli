# Smart Campus Energy Optimization Challenge (GridWise LLM)
## Project Development Guide & Canonical Technical Instructions

> **Competition**: BUP CSE FEST 2026 Hackathon (In association with Poridhi)  
> **Track**: GridWise LLM — Smart Campus Energy Optimization Challenge  
> **Challenge Type**: LLM-Assisted Energy Scheduling and Mathematical Optimization  
> **Required Artifact**: Deployed Public HTTP REST API (`/health` & `/optimize-energy`)  
> **Planning Horizon**: 24 hourly intervals (Hour 0 to Hour 23)  

---

## 1. Executive Summary & Challenge Architecture

### 1.1 Objective
BUP operates a smart campus supplied by:
1. **The Electricity Grid** (dynamic hourly tariff in BDT/kWh)
2. **Rooftop Solar Generation** (varying hourly solar irradiance in kWh)
3. **Battery Energy Storage System (BESS)** (capacity, starting charge, minimum reserve, hourly charge/discharge rate limits)

Campus operators issue **1–3 short natural-language operational notes** affecting the schedule (e.g., maintenance windows, solar cleaning, reserve requirements, grid import caps) or containing irrelevant distractors (e.g., cafeteria changes).

Your service must:
1. Parse and interpret natural-language notes using an **LLM** into machine-checkable structured directives.
2. Validate and sanitize directives using **deterministic guardrails** (with safe fallback).
3. Feed active directives into a **mathematical optimizer** (Linear Programming / MILP) to find the minimum-cost 24-hour operating plan.
4. Deterministically **replay and verify** the plan against all physical and directive constraints.
5. Return the structured response matching the exact JSON schema within the required time limits.

### 1.2 End-to-End Processing Flow

```
   ┌───────────────────────────────────────────────────────────┐
   │                  POST /optimize-energy                    │
   │  - 24h Scenario (demand, solar, tariff)                   │
   │  - Battery Specs (capacity, initial, min, rates)          │
   │  - 1-3 Operator Notes                                     │
   └─────────────────────────────┬─────────────────────────────┘
                                 │
                                 ▼
   ┌───────────────────────────────────────────────────────────┐
   │             Stage 1: LLM Directive Interpreter           │
   │  - Single multi-note prompt with strict JSON Schema       │
   │  - Classify note into 1 of 6 directives or no_op          │
   │  - Extract whole-hour windows [start, end) & parameters   │
   └─────────────────────────────┬─────────────────────────────┘
                                 │
                                 ▼
   ┌───────────────────────────────────────────────────────────┐
   │            Stage 2: Deterministic Guardrails              │
   │  - Validate bounds (hours: 0..23 ascending, factor: 0..1) │
   │  - Check reserve <= capacity, grid cap >= 0               │
   │  - Safe Failure: on invalid output, fallback to no_op     │
   └─────────────────────────────┬─────────────────────────────┘
                                 │
                                 ▼
   ┌───────────────────────────────────────────────────────────┐
   │            Stage 3: Mathematical LP Optimizer             │
   │  - Compute effective solar = base_solar * solar_factor    │
   │  - Set dynamic reserve: max(base_min, directive_min)      │
   │  - Apply charge/discharge blocks & grid import limits     │
   │  - Solve LP: Minimize sum(grid[h] * tariff[h])            │
   │  - Subject to: energy balance, battery state & neutrality │
   └─────────────────────────────┬─────────────────────────────┘
                                 │
                                 ▼
   ┌───────────────────────────────────────────────────────────┐
   │          Stage 4: Plan Replayer & Self-Validator         │
   │  - Replay hourly battery state transitions                │
   │  - Verify no simultaneous charge/discharge                │
   │  - Recalculate total_grid_kwh, total_cost_bdt, peak_grid  │
   │  - Ensure final_battery_energy == initial_battery_energy  │
   └─────────────────────────────┬─────────────────────────────┘
                                 │
                                 ▼
   ┌───────────────────────────────────────────────────────────┐
   │                     HTTP 200 Response                     │
   │  - scenario_id                                            │
   │  - directive_interpretation (note_index 0..N-1)           │
   │  - hourly_plan (hours 0..23)                              │
   │  - total_grid_kwh, total_cost_bdt, peak_grid_kwh          │
   │  - plan_summary                                           │
   └───────────────────────────────────────────────────────────┘
```

---

## 2. API Contract & Schema Specifications

The service must strictly adhere to the following endpoints. Endpoint paths are case-sensitive.

### 2.1 `GET /health`
- **Response**: HTTP 200
```json
{
  "status": "ok"
}
```

### 2.2 `POST /optimize-energy`

#### Request Payload Schema
```json
{
  "scenario_id": "string",
  "operator_notes": ["string"],
  "hours": [
    {
      "hour": 0,
      "demand_kwh": 180.0,
      "solar_kwh": 0.0,
      "tariff_bdt_per_kwh": 7.0
    }
    // ... exactly 24 entries for hour 0 to 23
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

#### Request Validation Rules
1. `scenario_id`: Non-empty string.
2. `operator_notes`: Array of 1 to 3 non-empty strings.
3. `hours`: Exactly 24 items, with `hour` ranging sequentially from `0` to `23`.
4. `battery`: All numerical fields must be finite, non-negative numbers.
   - `initial_energy_kwh` $\le$ `capacity_kwh`
   - `minimum_energy_kwh` $\le$ `capacity_kwh`

#### Response Payload Schema
```json
{
  "scenario_id": "GRID-101",
  "directive_interpretation": [
    {
      "note_index": 0,
      "applies": true,
      "directive_type": "solar_reduction",
      "structured_adjustment": {
        "hours": [13, 14],
        "factor": 0.2
      },
      "explanation": "Solar output reduced to 20% between 1 PM and 3 PM."
    },
    {
      "note_index": 1,
      "applies": false,
      "directive_type": "no_op",
      "structured_adjustment": null,
      "explanation": "Cafeteria notice does not impact energy operations."
    }
  ],
  "hourly_plan": [
    {
      "hour": 0,
      "grid_kwh": 180.0,
      "solar_used_kwh": 0.0,
      "battery_action": "idle",
      "battery_kwh": 0.0,
      "battery_energy_after_kwh": 200.0
    }
    // ... exactly 24 entries for hour 0 to 23
  ],
  "total_grid_kwh": 2450.5,
  "total_cost_bdt": 22100.25,
  "peak_grid_kwh": 220.0,
  "plan_summary": "Optimized schedule leveraging off-peak battery charging and solar prioritization while adhering to operator directives."
}
```

#### HTTP Status Codes
| Code | Meaning | Condition |
|---|---|---|
| **200** | Success | Valid scenario processed, schedule generated |
| **400** | Bad Request | Malformed JSON or structurally invalid payload |
| **422** | Unprocessable Entity | Semantically invalid input (e.g. missing hours) |
| **500** | Internal Error | Controlled internal error (never expose stack traces or API keys) |

---

## 3. Operator Directives & LLM Guardrail Rules

### 3.1 Supported Directive Types & Structures

| Directive Type | Meaning | Required `structured_adjustment` Shape | Notes & Semantics |
|---|---|---|---|
| `solar_reduction` | Reduces usable solar generation | `{"hours": [int, ...], "factor": float}` | `factor` = usable fraction remaining ($0 \le \text{factor} \le 1$). Example: "80% reduction" $\rightarrow$ `factor: 0.2`. |
| `minimum_battery_reserve` | Raises battery floor | `{"hours": [int, ...], "minimum_energy_kwh": float}` | $0 \le \text{reserve} \le \text{capacity\_kwh}$. Overrides base minimum if higher. |
| `no_charge_window` | Disables charging | `{"hours": [int, ...]}` | Battery charge amount must be `0` during these hours. |
| `no_discharge_window`| Disables discharging | `{"hours": [int, ...]}` | Battery discharge amount must be `0` during these hours. |
| `max_grid_window` | Caps grid power import | `{"hours": [int, ...], "max_grid_kwh": float}` | $\text{grid\_kwh}[h] \le \text{max\_grid\_kwh}$ for all listed hours. |
| `no_op` | Irrelevant / distractor note | `null` | Must have `applies: false` and `structured_adjustment: null`. |

### 3.2 Time-Window Interpretation Standard
- **Time indexing**: Hours are whole integers $0, 1, \dots, 23$.
- **Interval convention**: Half-open interval $[start, end)$ — start hour included, end hour excluded.
  - *"1 PM to 3 PM"* $\rightarrow$ Hours $13:00$ to $15:00$ $\rightarrow$ `[13, 14]`
  - *"between 14:00 and 17:00"* $\rightarrow$ `[14, 15, 16]`
  - *"at 6 PM until 9 PM"* $\rightarrow$ `[18, 19, 20]`
- **Array formatting**: The `hours` array inside `structured_adjustment` **must be sorted in strictly ascending order** with **unique integers** within `0..23`.

### 3.3 Guardrails & Safe-Failure Handling
1. **Note Ordering**: Output `directive_interpretation` must have entries for `note_index` in exact ascending order: `0, 1, ..., N-1`. Every note must appear exactly once.
2. **Boolean `applies` Consistency**:
   - If `directive_type == "no_op"`, then `applies` **must** be `false`, and `structured_adjustment` **must** be `null`.
   - If `directive_type != "no_op"`, then `applies` **must** be `true`, and `structured_adjustment` **must not** be `null`.
3. **No Hallucination**: The LLM must not invent changes to base demand, base tariffs, or base battery specifications.
4. **Safe Failure**: If the LLM produces invalid JSON or an unsupported directive type, catch the error deterministically and map that note to `no_op` (`applies: false, structured_adjustment: null`) instead of crashing the API.

---

## 4. Mathematical Optimization Model (Linear Programming)

The 24-hour horizon must be optimized using an exact Linear Program (LP) solver (e.g., PuLP with CBC or SciPy HiGHS).

### 4.1 Decision Variables (for each hour $h \in \{0, 1, \dots, 23\}$)
- $g_h \ge 0$: Grid energy purchased (kWh)
- $s_h \ge 0$: Solar energy consumed by campus (kWh)
- $c_h \ge 0$: Energy charged into the battery (kWh)
- $d_h \ge 0$: Energy discharged from the battery (kWh)
- $E_h \ge 0$: Battery state of energy at the end of hour $h$ (kWh)

### 4.2 Objective Function
Minimize the total electricity purchase cost:
$$\min \quad \text{Total Cost} = \sum_{h=0}^{23} \left( g_h \times \text{tariff}_h \right)$$

### 4.3 Deterministic Effect of Directives
Before constructing the LP constraints, compute adjusted baseline arrays:

1. **Effective Solar Availability**:
   $$\text{effective\_solar}_h = \text{base\_solar}_h \times \prod_{d \in \text{solar\_directives}(h)} d.\text{factor}$$
2. **Dynamic Battery Minimum Reserve**:
   $$\text{min\_reserve}_h = \max\left(\text{base\_min}, \max_{d \in \text{reserve\_directives}(h)} d.\text{minimum\_energy\_kwh}\right)$$
3. **Charge / Discharge Permission**:
   - If $h \in \text{no\_charge\_hours}$: $c_h = 0$ (or upper bound $= 0$).
   - If $h \in \text{no\_discharge\_hours}$: $d_h = 0$ (or upper bound $= 0$).
4. **Grid Import Limit**:
   - If $h \in \text{max\_grid\_hours}$: $g_h \le \min_{d \in \text{grid\_directives}(h)} d.\text{max\_grid\_kwh}$.

### 4.4 Constraints
For every hour $h \in \{0, \dots, 23\}$:

1. **Campus Energy Balance**:
   $$g_h + s_h + d_h = \text{demand}_h + c_h$$
2. **Solar Utilization Limit** (excess solar is curtailed, no grid export):
   $$0 \le s_h \le \text{effective\_solar}_h$$
3. **Battery Energy Dynamics**:
   - For $h = 0$:
     $$E_0 = E_{\text{initial}} + c_0 - d_0$$
   - For $h \in \{1, \dots, 23\}$:
     $$E_h = E_{h-1} + c_h - d_h$$
4. **Battery Energy Bounds**:
   $$\text{min\_reserve}_h \le E_h \le \text{capacity}$$
5. **Battery Rate Limits**:
   $$0 \le c_h \le \text{max\_charge\_per\_hour}$$
   $$0 \le d_h \le \text{max\_discharge\_per\_hour}$$
6. **End-of-Day Neutrality**:
   $$E_{23} = E_{\text{initial}}$$
   *(Ensures the battery is not exploited as a one-time energy depletion source).*

### 4.5 Battery Action Disjunction
Each hour must specify:
- `battery_action`: Exactly one of `"charge"`, `"discharge"`, or `"idle"`.
- `battery_kwh`: Magnitude of the action (non-negative, exactly $0.0$ when `"idle"`).

*Note*: In any optimal solution where electricity tariffs are positive ($\text{tariff}_h > 0$), simultaneous charging and discharging is strictly sub-optimal because round-trip efficiency loss or identical substitution yields higher or equal cost. If numerical tolerances cause minute non-zero values on both sides (e.g. $10^{-6}$), apply a net post-processing cleanup:
- If $c_h > d_h$: $\text{net\_charge} = c_h - d_h$; set action = `"charge"`, `battery_kwh` = $\text{net\_charge}$.
- If $d_h > c_h$: $\text{net\_discharge} = d_h - c_h$; set action = `"discharge"`, `battery_kwh` = $\text{net\_discharge}$.
- If $|c_h - d_h| < 10^{-4}$: set action = `"idle"`, `battery_kwh` = $0.0$.

---

## 5. Plan Replay & Verification Engine

Before returning the HTTP response, the service must run an internal validation pass mimicking the judge's evaluation logic.

### 5.1 Verification Checklist
1. **Hour Count & Order**: `hourly_plan` must contain exactly 24 entries, sorted $0 \dots 23$.
2. **Non-negativity**: All values (`grid_kwh`, `solar_used_kwh`, `battery_kwh`, `battery_energy_after_kwh`) $\ge 0$.
3. **Solar Upper Bound**: $\text{solar\_used\_kwh}[h] \le \text{effective\_solar}[h] + 0.01$.
4. **Energy Balance**:
   $$|\left(\text{grid\_kwh}[h] + \text{solar\_used\_kwh}[h] + \text{discharge}[h]\right) - \left(\text{demand}[h] + \text{charge}[h]\right)| \le 0.01$$
5. **State Transition**:
   $$|E_h - (E_{h-1} + \text{charge}[h] - \text{discharge}[h])| \le 0.01$$
6. **Battery Capacity & Reserve Bounds**:
   $$\text{min\_reserve}_h - 0.01 \le E_h \le \text{capacity} + 0.01$$
7. **Rate Limits**:
   $$\text{charge}[h] \le \text{max\_charge} + 0.01, \quad \text{discharge}[h] \le \text{max\_discharge} + 0.01$$
8. **End-of-Day Neutrality**:
   $$|E_{23} - E_{\text{initial}}| \le 0.01$$
9. **Recalculated Summary Consistency**:
   - `total_grid_kwh` = $\sum_{h=0}^{23} \text{grid\_kwh}[h]$
   - `total_cost_bdt` = $\sum_{h=0}^{23} (\text{grid\_kwh}[h] \times \text{tariff}[h])$
   - `peak_grid_kwh` = $\max_{h=0}^{23} \text{grid\_kwh}[h]$
   *(All summary fields must match the sum/max of the hourly array within 0.01 tolerance)*.

---

## 6. Recommended System Architecture & Directory Structure

```
gridwise-llm-service/
├── app/
│   ├── __init__.py
│   ├── main.py                  # FastAPI application entrypoint & routing
│   ├── config.py                # Environment configurations (API keys, ports)
│   ├── schemas/
│   │   ├── __init__.py
│   │   ├── request.py           # ScenarioRequest, HourEntry, BatterySpecs
│   │   └── response.py          # ScenarioResponse, DirectiveInterpretation, HourlyPlanEntry
│   ├── llm/
│   │   ├── __init__.py
│   │   ├── client.py            # LLM invocation (Gemini / OpenAI / Groq)
│   │   ├── prompts.py           # System instructions & few-shot examples
│   │   └── parser.py            # Robust JSON parser & extractor
│   ├── guardrails/
│   │   ├── __init__.py
│   │   └── validator.py         # Deterministic directive checks & safe fallbacks
│   ├── optimizer/
│   │   ├── __init__.py
│   │   ├── solver.py            # PuLP / SciPy Linear Programming formulation
│   │   └── postprocess.py       # Battery action discretization & rounding
│   └── verifier/
│       ├── __init__.py
│       └── replay.py            # Judge simulator & integrity checker
├── tests/
│   ├── test_api.py              # Health check & integration tests
│   ├── test_llm_parser.py       # Unit tests with diverse operator notes
│   ├── test_optimizer.py        # Edge-case optimization tests
│   └── test_sample_cases.py     # Evaluation on public test cases
├── Dockerfile                   # Production container definition
├── docker-compose.yml           # Local dev & deployment orchestration
├── requirements.txt             # Python dependencies
└── README.md                    # Quickstart & API documentation
```

---

## 7. Step-by-Step Implementation Roadmap

### Phase 1: Environment & Scaffolding
1. Initialize a Python 3.11 virtual environment.
2. Install core dependencies:
   ```bash
   pip install fastapi uvicorn pydantic pulp scipy google-genai httpx pytest
   ```
3. Set up `app/main.py` with `GET /health` returning `{"status": "ok"}`.

### Phase 2: Core Schemas (Pydantic v2)
1. Define `HourInput`, `BatteryInput`, and `ScenarioRequest`.
2. Define `StructuredAdjustment`, `DirectiveInterpretation`, `HourlyPlanEntry`, and `ScenarioResponse`.
3. Add custom validators to guarantee:
   - `hours` has length 24 and sequential hours `0..23`.
   - `directive_interpretation` preserves `note_index` sequence.
   - Values conform to float bounds.

### Phase 3: Mathematical Optimizer Engine (`solver.py`)
1. Implement `solve_energy_schedule(hours, battery, applied_directives)`.
2. Model decision variables using `pulp.LpVariable`.
3. Inject constraints:
   - Energy balance equality.
   - Battery state transitions.
   - Dynamic lower and upper bounds based on parsed directives.
   - Solar curtailment ceiling.
   - Neutrality constraint: $E_{23} == \text{battery.initial\_energy\_kwh}$.
4. Solve using `pulp.PULP_CBC_CMD(msg=0)`.
5. Extract values and compute `battery_action` (`"charge"`, `"discharge"`, `"idle"`).

### Phase 4: LLM Interpretation & Guardrail Engine
1. Select the primary LLM provider (Google Gemini 1.5/2.0 Flash or Groq Llama-3-70b for low latency $< 1.5\text{s}$).
2. Build `prompts.py` containing:
   - Detailed instructions on the 6 supported directive types.
   - Time window rules: $[start, end)$ half-open interval.
   - Reduction factor semantics: $1.0 - \text{reduction\_fraction}$.
   - 6–8 diverse few-shot examples (including distractors and varied phrasing).
3. Implement `guardrails/validator.py`:
   - Validate that `hours` is sorted and within $0..23$.
   - Clamp or validate `factor` between $0.0$ and $1.0$.
   - Ensure `applies == false` and `structured_adjustment is None` for `no_op`.
   - Catch parsing errors and automatically convert malformed notes to safe `no_op`.

### Phase 5: Verification & Replay Engine (`replay.py`)
1. Implement independent replay simulation.
2. Verify all 9 conditions listed in Section 5.
3. Compute exact summary metrics (`total_grid_kwh`, `total_cost_bdt`, `peak_grid_kwh`) rounded to 4 decimal places.

### Phase 6: Integration & API Route
1. Wire all components in `POST /optimize-energy` in `app/main.py`:
   ```python
   @app.post("/optimize-energy", response_model=ScenarioResponse)
   async def optimize_energy(payload: ScenarioRequest):
       # 1. Interpret notes via LLM
       raw_directives = await interpret_notes(payload.operator_notes)
       # 2. Guardrails & Sanitization
       clean_directives = validate_directives(raw_directives, len(payload.operator_notes), payload.battery)
       # 3. Solve Optimization
       schedule, metrics = solve_energy_schedule(payload.hours, payload.battery, clean_directives)
       # 4. Independent Replay Check
       verify_schedule(schedule, payload.hours, payload.battery, clean_directives)
       # 5. Build Response
       return build_response(payload.scenario_id, clean_directives, schedule, metrics)
   ```

### Phase 7: Containerization & Cloud Deployment
1. Write a lightweight Dockerfile based on `python:3.11-slim`.
2. Ensure solver binaries (`glpk` or default CBC bundled in PuLP) run without missing shared libraries.
3. Deploy to the designated host (Poridhi / VM / Cloud Run / VPS).
4. Verify external accessibility over public HTTP.

---

## 8. LLM Prompting & Parsing Reference Guide

### 8.1 System Prompt Template
```text
You are an expert energy operations parser for the BUP Smart Campus Energy System.
Your job is to read 1 to 3 natural-language operator notes and convert EACH note into a strictly valid directive.

SUPPORTED DIRECTIVES:
1. solar_reduction:
   - Use when solar output is decreased, curtailed, or during panel maintenance/cleaning.
   - Required structured_adjustment: {"hours": [int, ...], "factor": float}
   - CRITICAL: "factor" is the USABLE REMAINING fraction (between 0.0 and 1.0).
     Example: "80% drop/reduction" -> factor = 0.2. "Drop to 20%" -> factor = 0.2.

2. minimum_battery_reserve:
   - Use when battery must maintain a minimum charge or emergency reserve level.
   - Required structured_adjustment: {"hours": [int, ...], "minimum_energy_kwh": float}

3. no_charge_window:
   - Use when charging the battery is prohibited or unavailable.
   - Required structured_adjustment: {"hours": [int, ...]}

4. no_discharge_window:
   - Use when discharging the battery is prohibited or unavailable.
   - Required structured_adjustment: {"hours": [int, ...]}

5. max_grid_window:
   - Use when grid energy import/purchase is capped at a maximum kWh.
   - Required structured_adjustment: {"hours": [int, ...], "max_grid_kwh": float}

6. no_op:
   - Use when the note is irrelevant, a distractor, or does not affect today's energy schedule.
   - applies: false
   - structured_adjustment: null

TIME CONVENTION:
- Hours are integers 0 to 23.
- Time intervals are [start, end) where start is included and end is excluded.
  - "1 PM to 3 PM" -> [13, 14]
  - "between 14:00 and 17:00" -> [14, 15, 16]
  - "from 6 PM until 9 PM" -> [18, 19, 20]
  - "during the 1-3 PM maintenance window" -> [13, 14]
- "hours" must be a sorted array of unique integers in ascending order.

OUTPUT FORMAT:
Return a JSON array containing exactly one entry per note, in note_index order (0, 1, ..., N-1).
JSON Schema:
[
  {
    "note_index": 0,
    "applies": true,
    "directive_type": "solar_reduction",
    "structured_adjustment": {"hours": [13, 14], "factor": 0.2},
    "explanation": "Brief explanation"
  },
  {
    "note_index": 1,
    "applies": false,
    "directive_type": "no_op",
    "structured_adjustment": null,
    "explanation": "Brief explanation"
  }
]
```

### 8.2 Paraphrasing Benchmark Examples

| Natural-Language Note | Target Directive | Target `structured_adjustment` |
|---|---|---|
| `"PV production will drop to about 20% between 13:00 and 15:00."` | `solar_reduction` | `{"hours": [13, 14], "factor": 0.2}` |
| `"Panel washing from one until three will leave roughly one-fifth of normal solar output."` | `solar_reduction` | `{"hours": [13, 14], "factor": 0.2}` |
| `"Expect an 80% reduction in rooftop solar during the 1-3 PM maintenance window."` | `solar_reduction` | `{"hours": [13, 14], "factor": 0.2}` |
| `"Do not charge the battery between 2 PM and 4 PM."` | `no_charge_window` | `{"hours": [14, 15]}` |
| `"Inverter testing: no battery charging allowed from 14:00 to 16:00."` | `no_charge_window` | `{"hours": [14, 15]}` |
| `"Keep at least 120 kWh in reserve from 6 PM until 9 PM."` | `minimum_battery_reserve` | `{"hours": [18, 19, 20], "minimum_energy_kwh": 120.0}` |
| `"Grid transformer maintenance caps import at 50 kWh from 8 AM to 11 AM."` | `max_grid_window` | `{"hours": [8, 9, 10], "max_grid_kwh": 50.0}` |
| `"Do not pull battery power from 5 AM to 7 AM."` | `no_discharge_window` | `{"hours": [5, 6]}` |
| `"The campus shuttle schedule will be updated next Monday."` | `no_op` | `null` |
| `"Cafeteria will serve lunch 30 minutes earlier today."` | `no_op` | `null` |

---

## 9. Testing & Validation Checklist

Before submitting the deployed endpoint:

- [ ] **Health Check**: `GET /health` responds in $< 50\text{ms}$ with `{"status": "ok"}`.
- [ ] **Exact Schema Match**: Key names, types, and structure match the specification 100%.
- [ ] **Ascending `hours`**: `hours` arrays in `structured_adjustment` and `hourly_plan` are strictly sorted $0 \dots 23$.
- [ ] **Zero-Hallucination**: LLM never invents base demand or battery specs.
- [ ] **Safe Fallback**: API gracefully handles arbitrary junk text notes without throwing HTTP 500.
- [ ] **End-of-Day Neutrality**: $\text{battery\_energy\_after\_kwh}[23] == \text{initial\_energy\_kwh}$.
- [ ] **No Simultaneous Action**: Each hour has either `"charge"`, `"discharge"`, or `"idle"`. When `"idle"`, `battery_kwh == 0.0`.
- [ ] **Summary Verification**: `total_grid_kwh`, `total_cost_bdt`, and `peak_grid_kwh` strictly match the hourly plan sums.
- [ ] **Latency**: Entire request processing completes well within judge timeout ($< 5\text{s}$).
- [ ] **Deployment Security**: API keys, internal stack traces, and environment variables are never exposed in error responses.

---
*Created for the BUP CSE Fest 2026 Preliminary Round Hackathon.*
