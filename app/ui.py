DASHBOARD_HTML = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>GridWise LLM - Smart Campus Energy Optimizer</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600&display=swap" rel="stylesheet">
    <style>
        :root {
            --bg-primary: #0b0f19;
            --bg-card: #111827;
            --bg-card-hover: #1f2937;
            --border-color: #374151;
            --text-main: #f9fafb;
            --text-muted: #9ca3af;
            --accent-green: #10b981;
            --accent-blue: #3b82f6;
            --accent-amber: #f59e0b;
            --accent-purple: #8b5cf6;
        }

        * {
            box-sizing: border-box;
            margin: 0;
            padding: 0;
        }

        body {
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
            background-color: var(--bg-primary);
            color: var(--text-main);
            min-height: 100vh;
            display: flex;
            flex-direction: column;
        }

        header {
            background: rgba(17, 24, 39, 0.8);
            backdrop-filter: blur(12px);
            border-bottom: 1px solid var(--border-color);
            padding: 1rem 2rem;
            display: flex;
            justify-content: space-between;
            align-items: center;
            position: sticky;
            top: 0;
            z-index: 50;
        }

        .logo-box {
            display: flex;
            align-items: center;
            gap: 0.75rem;
        }

        .logo-icon {
            width: 38px;
            height: 38px;
            background: linear-gradient(135deg, var(--accent-blue), var(--accent-green));
            border-radius: 10px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 1.25rem;
            font-weight: 800;
        }

        .logo-title {
            font-size: 1.2rem;
            font-weight: 700;
            letter-spacing: -0.02em;
        }

        .logo-sub {
            font-size: 0.75rem;
            color: var(--text-muted);
            text-transform: uppercase;
            letter-spacing: 0.05em;
        }

        .status-badge {
            display: inline-flex;
            align-items: center;
            gap: 0.5rem;
            background: rgba(16, 185, 129, 0.1);
            color: var(--accent-green);
            border: 1px solid rgba(16, 185, 129, 0.3);
            padding: 0.35rem 0.85rem;
            border-radius: 9999px;
            font-size: 0.8rem;
            font-weight: 600;
        }

        .pulse-dot {
            width: 8px;
            height: 8px;
            background-color: var(--accent-green);
            border-radius: 50%;
            box-shadow: 0 0 10px var(--accent-green);
            animation: pulse 2s infinite;
        }

        @keyframes pulse {
            0%, 100% { opacity: 1; }
            50% { opacity: 0.4; }
        }

        main {
            flex: 1;
            max-width: 1200px;
            width: 100%;
            margin: 0 auto;
            padding: 2.5rem 1.5rem;
            display: flex;
            flex-direction: column;
            gap: 2rem;
        }

        .hero {
            text-align: center;
            padding: 1.5rem 0 2.5rem;
        }

        .hero h1 {
            font-size: 2.5rem;
            font-weight: 800;
            margin-bottom: 0.75rem;
            background: linear-gradient(135deg, #60a5fa, #34d399);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }

        .hero p {
            color: var(--text-muted);
            font-size: 1.1rem;
            max-width: 700px;
            margin: 0 auto;
            line-height: 1.6;
        }

        .actions-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
            gap: 1.25rem;
        }

        .card {
            background: var(--bg-card);
            border: 1px solid var(--border-color);
            border-radius: 14px;
            padding: 1.5rem;
            transition: transform 0.2s, border-color 0.2s;
        }

        .card:hover {
            transform: translateY(-2px);
            border-color: #4b5563;
        }

        .card-header {
            display: flex;
            align-items: center;
            gap: 0.75rem;
            margin-bottom: 1rem;
        }

        .card-icon {
            width: 32px;
            height: 32px;
            border-radius: 8px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 1rem;
        }

        .card-title {
            font-size: 1.1rem;
            font-weight: 600;
        }

        .card p {
            color: var(--text-muted);
            font-size: 0.9rem;
            margin-bottom: 1.25rem;
            line-height: 1.5;
        }

        .btn {
            display: inline-flex;
            align-items: center;
            justify-content: center;
            gap: 0.5rem;
            padding: 0.65rem 1.25rem;
            border-radius: 8px;
            font-size: 0.9rem;
            font-weight: 600;
            text-decoration: none;
            cursor: pointer;
            transition: all 0.2s;
            border: none;
        }

        .btn-primary {
            background: var(--accent-blue);
            color: #ffffff;
        }

        .btn-primary:hover {
            background: #2563eb;
        }

        .btn-secondary {
            background: #1f2937;
            color: #d1d5db;
            border: 1px solid #374151;
        }

        .btn-secondary:hover {
            background: #374151;
            color: #ffffff;
        }

        .tester-section {
            background: var(--bg-card);
            border: 1px solid var(--border-color);
            border-radius: 16px;
            padding: 2rem;
        }

        .tester-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 1.5rem;
        }

        .tester-title {
            font-size: 1.3rem;
            font-weight: 700;
        }

        .json-preview {
            background: #000000;
            border: 1px solid #1f2937;
            border-radius: 10px;
            padding: 1rem;
            font-family: 'JetBrains Mono', monospace;
            font-size: 0.85rem;
            color: #a7f3d0;
            max-height: 250px;
            overflow-y: auto;
            margin-bottom: 1.25rem;
        }

        .results-box {
            margin-top: 1.5rem;
            padding: 1.25rem;
            border-radius: 10px;
            background: #0f172a;
            border: 1px solid #334155;
            display: none;
        }

        .metrics-grid {
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 1rem;
            margin-bottom: 1.25rem;
        }

        .metric-card {
            background: #1e293b;
            padding: 1rem;
            border-radius: 8px;
            text-align: center;
        }

        .metric-label {
            font-size: 0.75rem;
            color: var(--text-muted);
            text-transform: uppercase;
        }

        .metric-value {
            font-size: 1.4rem;
            font-weight: 700;
            margin-top: 0.25rem;
            color: #38bdf8;
        }

        table {
            width: 100%;
            border-collapse: collapse;
            font-size: 0.85rem;
            margin-top: 1rem;
        }

        th, td {
            padding: 0.6rem 0.75rem;
            text-align: left;
            border-bottom: 1px solid #1e293b;
        }

        th {
            color: var(--text-muted);
            font-weight: 600;
        }

        .badge-charge {
            background: rgba(16, 185, 129, 0.2);
            color: #34d399;
            padding: 0.2rem 0.5rem;
            border-radius: 4px;
            font-size: 0.75rem;
            font-weight: 600;
        }

        .badge-discharge {
            background: rgba(245, 158, 11, 0.2);
            color: #fbbf24;
            padding: 0.2rem 0.5rem;
            border-radius: 4px;
            font-size: 0.75rem;
            font-weight: 600;
        }

        .badge-idle {
            background: rgba(148, 163, 184, 0.2);
            color: #94a3b8;
            padding: 0.2rem 0.5rem;
            border-radius: 4px;
            font-size: 0.75rem;
            font-weight: 600;
        }

        footer {
            border-top: 1px solid var(--border-color);
            padding: 1.5rem 2rem;
            text-align: center;
            font-size: 0.85rem;
            color: var(--text-muted);
            background: var(--bg-card);
        }
    </style>
</head>
<body>

    <header>
        <div class="logo-box">
            <div class="logo-icon">⚡</div>
            <div>
                <div class="logo-title">GridWise LLM</div>
                <div class="logo-sub">Smart Campus Energy Optimizer</div>
            </div>
        </div>
        <div class="status-badge">
            <div class="pulse-dot"></div>
            <span>API Ready (GET /health: OK)</span>
        </div>
    </header>

    <main>
        <section class="hero">
            <h1>Campus Energy Scheduling Service</h1>
            <p>High-performance mathematical Linear Programming optimizer paired with LLM-assisted operator directive interpretation for BUP CSE Fest 2026.</p>
        </section>

        <section class="actions-grid">
            <div class="card">
                <div class="card-header">
                    <div class="card-icon" style="background: rgba(59, 130, 246, 0.2); color: #60a5fa;">📖</div>
                    <div class="card-title">Interactive API Docs</div>
                </div>
                <p>Explore the live OpenAPI / Swagger documentation, inspect schemas, and test endpoints interactively.</p>
                <a href="/docs" class="btn btn-primary" target="_blank">Open Swagger UI →</a>
            </div>

            <div class="card">
                <div class="card-header">
                    <div class="card-icon" style="background: rgba(139, 92, 246, 0.2); color: #a78bfa;">📑</div>
                    <div class="card-title">Alternative ReDoc</div>
                </div>
                <p>View clean, responsive, human-readable ReDoc API documentation with field breakdowns.</p>
                <a href="/redoc" class="btn btn-secondary" target="_blank">Open ReDoc →</a>
            </div>

            <div class="card">
                <div class="card-header">
                    <div class="card-icon" style="background: rgba(16, 185, 129, 0.2); color: #34d399;">💓</div>
                    <div class="card-title">Health Check</div>
                </div>
                <p>Direct HTTP probe verifying service readiness and container vitality for the automated judge harness.</p>
                <a href="/health" class="btn btn-secondary" target="_blank">View /health JSON →</a>
            </div>
        </section>

        <section class="tester-section">
            <div class="tester-header">
                <div class="tester-title">⚡ Live 24-Hour Optimization Test</div>
                <button id="run-btn" class="btn btn-primary" onclick="runOptimization()">Run Test Optimization</button>
            </div>
            <p style="color: var(--text-muted); font-size: 0.9rem; margin-bottom: 1rem;">
                Clicking the button will submit the 24-hour benchmark scenario to <code>POST /optimize-energy</code>, extract natural language directives, solve the exact Linear Program, and display the optimal schedule.
            </p>

            <div id="loading" style="display: none; text-align: center; padding: 1.5rem; color: #60a5fa; font-weight: 600;">
                Solving Linear Program & validating constraints...
            </div>

            <div id="results" class="results-box">
                <div class="metrics-grid">
                    <div class="metric-card">
                        <div class="metric-label">Total Grid Import</div>
                        <div id="m-grid" class="metric-value">-</div>
                    </div>
                    <div class="metric-card">
                        <div class="metric-label">Total Cost</div>
                        <div id="m-cost" class="metric-value">-</div>
                    </div>
                    <div class="metric-card">
                        <div class="metric-label">Peak Grid Load</div>
                        <div id="m-peak" class="metric-value">-</div>
                    </div>
                </div>

                <div style="margin-bottom: 1rem;">
                    <strong style="color: #f8fafc;">Strategy Summary:</strong>
                    <p id="m-summary" style="color: var(--text-muted); font-size: 0.9rem; margin-top: 0.25rem;"></p>
                </div>

                <div style="margin-bottom: 1rem;">
                    <strong style="color: #f8fafc;">Parsed Operator Directives:</strong>
                    <ul id="m-directives" style="margin-left: 1.25rem; margin-top: 0.5rem; color: #cbd5e1; font-size: 0.85rem; line-height: 1.6;"></ul>
                </div>

                <div style="max-height: 320px; overflow-y: auto; border: 1px solid #334155; border-radius: 8px;">
                    <table>
                        <thead>
                            <tr>
                                <th>Hour</th>
                                <th>Grid (kWh)</th>
                                <th>Solar Used (kWh)</th>
                                <th>Battery Action</th>
                                <th>Action Magnitude</th>
                                <th>Battery SoC (kWh)</th>
                            </tr>
                        </thead>
                        <tbody id="plan-rows"></tbody>
                    </table>
                </div>
            </div>
        </section>
    </main>

    <footer>
        BUP CSE FEST 2026 Hackathon &bull; GridWise LLM Track &bull; In association with Poridhi
    </footer>

    <script>
        const samplePayload = {
            "scenario_id": "BUP-LIVE-TEST-01",
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
        };

        async function runOptimization() {
            const btn = document.getElementById("run-btn");
            const loading = document.getElementById("loading");
            const results = document.getElementById("results");

            btn.disabled = true;
            loading.style.display = "block";
            results.style.display = "none";

            try {
                const res = await fetch("/optimize-energy", {
                    method: "POST",
                    headers: {"Content-Type": "application/json"},
                    body: JSON.stringify(samplePayload)
                });
                const data = await res.json();
                
                document.getElementById("m-grid").innerText = data.total_grid_kwh.toFixed(1) + " kWh";
                document.getElementById("m-cost").innerText = data.total_cost_bdt.toFixed(2) + " BDT";
                document.getElementById("m-peak").innerText = data.peak_grid_kwh.toFixed(1) + " kWh";
                document.getElementById("m-summary").innerText = data.plan_summary;

                const dirList = document.getElementById("m-directives");
                dirList.innerHTML = "";
                data.directive_interpretation.forEach(d => {
                    const li = document.createElement("li");
                    const statusText = d.applies ? '<span style="color:#34d399">[ACTIVE]</span>' : '<span style="color:#94a3b8">[IGNORED]</span>';
                    li.innerHTML = `${statusText} <strong>${d.directive_type}</strong>: ${d.explanation}`;
                    dirList.appendChild(li);
                });

                const tbody = document.getElementById("plan-rows");
                tbody.innerHTML = "";
                data.hourly_plan.forEach(p => {
                    const tr = document.createElement("tr");
                    let badgeClass = "badge-idle";
                    if (p.battery_action === "charge") badgeClass = "badge-charge";
                    if (p.battery_action === "discharge") badgeClass = "badge-discharge";

                    tr.innerHTML = `
                        <td><strong>${p.hour}:00</strong></td>
                        <td>${p.grid_kwh.toFixed(1)}</td>
                        <td>${p.solar_used_kwh.toFixed(1)}</td>
                        <td><span class="${badgeClass}">${p.battery_action.toUpperCase()}</span></td>
                        <td>${p.battery_kwh.toFixed(1)} kWh</td>
                        <td><strong>${p.battery_energy_after_kwh.toFixed(1)} kWh</strong></td>
                    `;
                    tbody.appendChild(tr);
                });

                results.style.display = "block";
            } catch (err) {
                alert("Error calling optimization endpoint: " + err);
            } finally {
                btn.disabled = false;
                loading.style.display = "none";
            }
        }
    </script>
</body>
</html>
"""
