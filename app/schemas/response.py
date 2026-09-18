from typing import List, Optional, Literal, Dict, Any, Union
from pydantic import BaseModel, Field, model_validator

DirectiveType = Literal[
    "solar_reduction",
    "minimum_battery_reserve",
    "no_charge_window",
    "no_discharge_window",
    "max_grid_window",
    "no_op",
]

BatteryAction = Literal["charge", "discharge", "idle"]


class DirectiveInterpretation(BaseModel):
    note_index: int = Field(..., ge=0, description="Zero-based index of operator note")
    applies: bool = Field(..., description="true for applicable directives, false only for no_op")
    directive_type: DirectiveType = Field(..., description="Canonical directive type")
    structured_adjustment: Optional[Dict[str, Any]] = Field(
        None, description="Exact machine-checkable object or null for no_op"
    )
    explanation: str = Field(..., description="Brief explanation of the interpretation")

    @model_validator(mode="after")
    def validate_applies_and_adjustment(self) -> "DirectiveInterpretation":
        if self.directive_type == "no_op":
            if self.applies:
                raise ValueError("applies must be false when directive_type is 'no_op'")
            if self.structured_adjustment is not None:
                raise ValueError("structured_adjustment must be null when directive_type is 'no_op'")
        else:
            if not self.applies:
                raise ValueError(f"applies must be true when directive_type is '{self.directive_type}'")
            if self.structured_adjustment is None:
                raise ValueError(f"structured_adjustment cannot be null when directive_type is '{self.directive_type}'")
        return self


class HourlyPlanEntry(BaseModel):
    hour: int = Field(..., ge=0, le=23, description="Hour 0 through 23")
    grid_kwh: float = Field(..., ge=0.0, description="Non-negative grid energy purchased in this hour")
    solar_used_kwh: float = Field(..., ge=0.0, description="Solar energy utilized in this hour")
    battery_action: BatteryAction = Field(..., description="Exactly one of: charge, discharge, idle")
    battery_kwh: float = Field(..., ge=0.0, description="Magnitude of battery action, 0 when idle")
    battery_energy_after_kwh: float = Field(..., ge=0.0, description="Battery energy at completion of this hour")

    @model_validator(mode="after")
    def validate_action_magnitude(self) -> "HourlyPlanEntry":
        if self.battery_action == "idle" and abs(self.battery_kwh) > 1e-4:
            raise ValueError("battery_kwh must be 0 when battery_action is 'idle'")
        return self


class ScenarioResponse(BaseModel):
    scenario_id: str = Field(..., description="Matches request scenario_id")
    directive_interpretation: List[DirectiveInterpretation] = Field(
        ..., description="One machine-checkable entry for every operator note"
    )
    hourly_plan: List[HourlyPlanEntry] = Field(..., min_length=24, max_length=24, description="24 hourly entries")
    total_grid_kwh: float = Field(..., ge=0.0, description="Sum of grid_kwh across all 24 hours")
    total_cost_bdt: float = Field(..., ge=0.0, description="Calculated total grid electricity cost in BDT")
    peak_grid_kwh: float = Field(..., ge=0.0, description="Maximum hourly grid_kwh in returned plan")
    plan_summary: str = Field(..., description="Short explanation of final dispatch strategy")
