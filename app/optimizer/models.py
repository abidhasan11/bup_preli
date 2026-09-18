from typing import List, Dict, Optional, Set
from pydantic import BaseModel
from app.schemas.response import HourlyPlanEntry


class OptimizationResult(BaseModel):
    success: bool
    message: str
    hourly_plan: List[HourlyPlanEntry]
    total_grid_kwh: float
    total_cost_bdt: float
    peak_grid_kwh: float
