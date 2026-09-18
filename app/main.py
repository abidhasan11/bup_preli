import logging
from fastapi import FastAPI, HTTPException, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.schemas.request import ScenarioRequest
from app.schemas.response import ScenarioResponse
from app.llm.client import interpret_operator_notes
from app.guardrails.validator import validate_and_sanitize_directives
from app.optimizer.solver import solve_energy_schedule
from app.verifier.replay import verify_and_replay_schedule
from app.ui import DASHBOARD_HTML

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("gridwise")

app = FastAPI(
    title=settings.app_name,
    version=settings.version,
    description="Smart Campus Energy Optimization API (BUP CSE Fest 2026)",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """Handles structurally invalid or semantically invalid requests."""
    # If the JSON itself was malformed, return 400
    errors = exc.errors()
    for err in errors:
        if "json_invalid" in err.get("type", ""):
            return JSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                content={"detail": "Malformed JSON payload in request."},
            )
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={"detail": f"Request validation error: {errors[0].get('msg', 'Invalid data')}"},
    )


@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    """Guarantees internal errors are controlled and never leak secrets or stack traces."""
    logger.error(f"Unhandled internal server error: {exc}", exc_info=True)
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"detail": "Controlled internal server error occurred during optimization."},
    )


@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    """Interactive visual dashboard and local test console."""
    accept = request.headers.get("accept", "")
    if "application/json" in accept and "text/html" not in accept:
        return JSONResponse({
            "app": settings.app_name,
            "version": settings.version,
            "status": "online",
            "docs_url": "/docs",
            "health_url": "/health",
            "optimize_url": "/optimize-energy",
        })
    return HTMLResponse(content=DASHBOARD_HTML)


@app.get("/health", status_code=status.HTTP_200_OK)
async def health_check():
    """Health readiness probe endpoint."""
    return {"status": "ok"}


@app.post("/optimize-energy", response_model=ScenarioResponse, status_code=status.HTTP_200_OK)
async def optimize_energy(payload: ScenarioRequest):
    """
    Accepts 24-hour campus scenario + operator notes.
    Interprets directives, solves Linear Program, verifies schedule, and returns plan.
    """
    # Stage 1: LLM Directive Interpretation
    raw_directives = await interpret_operator_notes(payload.operator_notes)

    # Stage 2: Deterministic Guardrails & Sanitization
    clean_directives = validate_and_sanitize_directives(
        raw_directives=raw_directives,
        expected_note_count=len(payload.operator_notes),
        battery=payload.battery,
    )

    # Stage 3: Mathematical Optimization (Linear Program)
    opt_result = solve_energy_schedule(
        hours=payload.hours,
        battery=payload.battery,
        applied_directives=clean_directives,
    )

    if not opt_result.success:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"Infeasible energy scheduling scenario: {opt_result.message}",
        )

    # Stage 4: Independent Replay Verification
    is_valid, violations = verify_and_replay_schedule(
        hourly_plan=opt_result.hourly_plan,
        hours=payload.hours,
        battery=payload.battery,
        applied_directives=clean_directives,
        tolerance=settings.tolerance_kwh,
    )

    if not is_valid:
        logger.warning(f"Replay check encountered discrepancies: {violations}")

    # Stage 5: Strategy Plan Summary
    active_count = sum(1 for d in clean_directives if d.applies)
    summary = (
        f"Optimized 24-hour dispatch schedule for scenario {payload.scenario_id}. "
        f"Applied {active_count} active operator directive(s). "
        f"Total grid import: {opt_result.total_grid_kwh:.2f} kWh across 24h costing {opt_result.total_cost_bdt:.2f} BDT "
        f"with peak grid import of {opt_result.peak_grid_kwh:.2f} kWh."
    )

    return ScenarioResponse(
        scenario_id=payload.scenario_id,
        directive_interpretation=clean_directives,
        hourly_plan=opt_result.hourly_plan,
        total_grid_kwh=opt_result.total_grid_kwh,
        total_cost_bdt=opt_result.total_cost_bdt,
        peak_grid_kwh=opt_result.peak_grid_kwh,
        plan_summary=summary,
    )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host=settings.host, port=settings.port, reload=True)
