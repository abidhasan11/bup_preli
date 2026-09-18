from typing import List, Dict, Any, Optional
from app.schemas.response import DirectiveInterpretation, DirectiveType
from app.schemas.request import BatterySpecs

VALID_DIRECTIVE_TYPES = {
    "solar_reduction",
    "minimum_battery_reserve",
    "no_charge_window",
    "no_discharge_window",
    "max_grid_window",
    "no_op",
}


def sanitize_hours(raw_hours: Any) -> List[int]:
    """
    Cleans raw hours input to guarantee unique integers between 0 and 23 in strictly ascending order.
    """
    if not isinstance(raw_hours, list):
        return []
    valid_hours = set()
    for h in raw_hours:
        try:
            h_int = int(h)
            if 0 <= h_int <= 23:
                valid_hours.add(h_int)
        except (ValueError, TypeError):
            continue
    return sorted(list(valid_hours))


def create_safe_no_op(note_index: int, reason: str = "Directive fell back to no_op") -> DirectiveInterpretation:
    return DirectiveInterpretation(
        note_index=note_index,
        applies=False,
        directive_type="no_op",
        structured_adjustment=None,
        explanation=reason,
    )


def validate_and_sanitize_directives(
    raw_directives: List[Dict[str, Any]],
    expected_note_count: int,
    battery: BatterySpecs,
) -> List[DirectiveInterpretation]:
    """
    Strictly validates raw LLM output against Section 08 Guardrails and Section 04 schemas.
    Always returns exactly one entry per note in ascending note_index order (0..N-1).
    Fails safely to no_op instead of crashing.
    """
    indexed_map: Dict[int, Dict[str, Any]] = {}

    for item in raw_directives:
        if not isinstance(item, dict):
            continue
        idx = item.get("note_index")
        if isinstance(idx, int) and 0 <= idx < expected_note_count:
            # First occurrence takes priority
            if idx not in indexed_map:
                indexed_map[idx] = item

    sanitized: List[DirectiveInterpretation] = []

    for i in range(expected_note_count):
        raw_item = indexed_map.get(i)
        if not raw_item:
            sanitized.append(create_safe_no_op(i, "Note did not produce valid structured output; safely defaulted to no_op."))
            continue

        raw_type = str(raw_item.get("directive_type", "")).strip()
        explanation = str(raw_item.get("explanation", "Interpreted operator note.")).strip()

        if raw_type not in VALID_DIRECTIVE_TYPES or raw_type == "no_op":
            sanitized.append(create_safe_no_op(i, explanation if explanation else "Irrelevant note or unrecognized directive."))
            continue

        adj = raw_item.get("structured_adjustment")
        if not isinstance(adj, dict):
            sanitized.append(create_safe_no_op(i, f"Missing structured_adjustment for {raw_type}."))
            continue

        hours = sanitize_hours(adj.get("hours"))
        if not hours:
            sanitized.append(create_safe_no_op(i, f"No valid hours specified for {raw_type}."))
            continue

        if raw_type == "solar_reduction":
            try:
                factor = float(adj.get("factor", -1))
                if factor < 0.0 or factor > 1.0:
                    sanitized.append(create_safe_no_op(i, "Invalid factor for solar_reduction (must be between 0 and 1)."))
                    continue
                sanitized.append(
                    DirectiveInterpretation(
                        note_index=i,
                        applies=True,
                        directive_type="solar_reduction",
                        structured_adjustment={"hours": hours, "factor": round(factor, 4)},
                        explanation=explanation,
                    )
                )
            except (ValueError, TypeError):
                sanitized.append(create_safe_no_op(i, "Malformed factor for solar_reduction."))

        elif raw_type == "minimum_battery_reserve":
            try:
                req_kwh = float(adj.get("minimum_energy_kwh", -1))
                if req_kwh < 0.0 or req_kwh > battery.capacity_kwh:
                    sanitized.append(create_safe_no_op(i, "Reserve level out of bounds (must be >= 0 and <= battery capacity)."))
                    continue
                sanitized.append(
                    DirectiveInterpretation(
                        note_index=i,
                        applies=True,
                        directive_type="minimum_battery_reserve",
                        structured_adjustment={"hours": hours, "minimum_energy_kwh": round(req_kwh, 4)},
                        explanation=explanation,
                    )
                )
            except (ValueError, TypeError):
                sanitized.append(create_safe_no_op(i, "Malformed minimum_energy_kwh value."))

        elif raw_type == "no_charge_window":
            sanitized.append(
                DirectiveInterpretation(
                    note_index=i,
                    applies=True,
                    directive_type="no_charge_window",
                    structured_adjustment={"hours": hours},
                    explanation=explanation,
                )
            )

        elif raw_type == "no_discharge_window":
            sanitized.append(
                DirectiveInterpretation(
                    note_index=i,
                    applies=True,
                    directive_type="no_discharge_window",
                    structured_adjustment={"hours": hours},
                    explanation=explanation,
                )
            )

        elif raw_type == "max_grid_window":
            try:
                max_kwh = float(adj.get("max_grid_kwh", -1))
                if max_kwh < 0.0:
                    sanitized.append(create_safe_no_op(i, "max_grid_kwh must be non-negative."))
                    continue
                sanitized.append(
                    DirectiveInterpretation(
                        note_index=i,
                        applies=True,
                        directive_type="max_grid_window",
                        structured_adjustment={"hours": hours, "max_grid_kwh": round(max_kwh, 4)},
                        explanation=explanation,
                    )
                )
            except (ValueError, TypeError):
                sanitized.append(create_safe_no_op(i, "Malformed max_grid_kwh value."))

    return sanitized
