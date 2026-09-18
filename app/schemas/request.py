from typing import List
from pydantic import BaseModel, Field, field_validator, model_validator


class HourInput(BaseModel):
    hour: int = Field(..., ge=0, le=23, description="Hour of the day from 0 to 23")
    demand_kwh: float = Field(..., ge=0.0, description="Campus electricity demand in this hour")
    solar_kwh: float = Field(..., ge=0.0, description="Base solar generation available")
    tariff_bdt_per_kwh: float = Field(..., ge=0.0, description="Grid electricity price for this hour")


class BatterySpecs(BaseModel):
    capacity_kwh: float = Field(..., gt=0.0, description="Maximum energy the battery can store")
    initial_energy_kwh: float = Field(..., ge=0.0, description="Battery energy at start of hour 0")
    minimum_energy_kwh: float = Field(..., ge=0.0, description="Base reserve level battery must never breach")
    max_charge_kwh_per_hour: float = Field(..., ge=0.0, description="Maximum energy chargeable per hour")
    max_discharge_kwh_per_hour: float = Field(..., ge=0.0, description="Maximum energy dischargeable per hour")

    @model_validator(mode="after")
    def validate_battery_levels(self) -> "BatterySpecs":
        if self.initial_energy_kwh > self.capacity_kwh:
            raise ValueError(f"initial_energy_kwh ({self.initial_energy_kwh}) cannot exceed capacity_kwh ({self.capacity_kwh})")
        if self.minimum_energy_kwh > self.capacity_kwh:
            raise ValueError(f"minimum_energy_kwh ({self.minimum_energy_kwh}) cannot exceed capacity_kwh ({self.capacity_kwh})")
        return self


class ScenarioRequest(BaseModel):
    scenario_id: str = Field(..., min_length=1, description="Unique scenario identifier")
    operator_notes: List[str] = Field(..., min_length=1, max_length=3, description="1-3 natural-language notes")
    hours: List[HourInput] = Field(..., min_length=24, max_length=24, description="Hourly forecast for hours 0..23")
    battery: BatterySpecs = Field(..., description="Battery specifications")

    @field_validator("operator_notes")
    @classmethod
    def validate_notes(cls, v: List[str]) -> List[str]:
        if not v:
            raise ValueError("operator_notes must contain at least 1 note")
        if len(v) > 3:
            raise ValueError("operator_notes cannot contain more than 3 notes")
        for i, note in enumerate(v):
            if not note.strip():
                raise ValueError(f"operator_notes[{i}] cannot be empty or whitespace only")
        return v

    @field_validator("hours")
    @classmethod
    def validate_hours_sequence(cls, v: List[HourInput]) -> List[HourInput]:
        if len(v) != 24:
            raise ValueError(f"hours array must contain exactly 24 entries, got {len(v)}")
        for idx, item in enumerate(v):
            if item.hour != idx:
                raise ValueError(f"hours[{idx}] has hour={item.hour}, expected sequential hour={idx}")
        return v
