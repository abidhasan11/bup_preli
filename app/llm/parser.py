import json
import re
from typing import List, Dict, Any, Optional, Tuple


def extract_time_window(text: str) -> Optional[List[int]]:
    """
    Extracts whole-hour half-open [start, end) interval from natural language text.
    Examples:
      - '1 PM to 3 PM' -> [13, 14]
      - 'between 2 PM and 4 PM' -> [14, 15]
      - '13:00 and 15:00' -> [13, 14]
      - 'from 6 PM until 9 PM' -> [18, 19, 20]
      - '5 AM to 7 AM' -> [5, 6]
      - '8 AM to 11 AM' -> [8, 9, 10]
      - '1-3 PM' -> [13, 14]
      - 'one until three' -> [13, 14]
    """
    text_lower = text.lower()

    # 1. Check for word numbers: 'one until three', 'one to three' (typically afternoon 13..15 in this context)
    word_map = {
        "one": 13, "two": 14, "three": 15, "four": 16, "five": 17,
        "six": 18, "seven": 19, "eight": 8, "nine": 9, "ten": 10, "eleven": 11, "twelve": 12
    }
    for w1, h1 in word_map.items():
        for w2, h2 in word_map.items():
            pattern = rf"\b{w1}\s+(?:until|to|and|-)\s+{w2}\b"
            if re.search(pattern, text_lower):
                if h2 > h1:
                    return list(range(h1, h2))

    # 2. Check 24-hour format: '13:00 to 15:00' or 'between 13:00 and 15:00'
    m_24 = re.search(r"(\d{1,2}):00\s*(?:to|until|and|-)\s*(\d{1,2}):00", text_lower)
    if m_24:
        start = int(m_24.group(1))
        end = int(m_24.group(2))
        if 0 <= start < end <= 24:
            return list(range(start, end))

    # 3. Check 12-hour format with AM/PM: '1 PM to 3 PM' or '8 AM to 11 AM'
    m_ampm = re.search(r"(\d{1,2})\s*(am|pm)\s*(?:to|until|and|-)\s*(\d{1,2})\s*(am|pm)", text_lower)
    if m_ampm:
        h1 = int(m_ampm.group(1))
        p1 = m_ampm.group(2)
        h2 = int(m_ampm.group(3))
        p2 = m_ampm.group(4)

        if p1 == "pm" and h1 != 12:
            h1 += 12
        elif p1 == "am" and h1 == 12:
            h1 = 0

        if p2 == "pm" and h2 != 12:
            h2 += 12
        elif p2 == "am" and h2 == 12:
            h2 = 0

        if 0 <= h1 < h2 <= 24:
            return list(range(h1, h2))

    # 4. Check compressed range: '1-3 PM' or '2-4 PM'
    m_comp = re.search(r"(\d{1,2})\s*-\s*(\d{1,2})\s*(am|pm)", text_lower)
    if m_comp:
        h1 = int(m_comp.group(1))
        h2 = int(m_comp.group(2))
        period = m_comp.group(3)
        if period == "pm":
            if h1 != 12:
                h1 += 12
            if h2 != 12:
                h2 += 12
        if 0 <= h1 < h2 <= 24:
            return list(range(h1, h2))

    return None


def format_hours_window(hours: List[int]) -> str:
    """Formats whole-hour intervals into natural time descriptions."""
    if not hours:
        return "during specified hours"
    start_h = hours[0]
    end_h = hours[-1] + 1

    def to_ampm(h: int) -> str:
        if h == 0 or h == 24:
            return "12 AM"
        elif h < 12:
            return f"{h} AM"
        elif h == 12:
            return "12 PM"
        else:
            return f"{h - 12} PM"

    return f"between {to_ampm(start_h)} and {to_ampm(end_h)}"


def regex_fallback_parse_note(note: str, note_index: int) -> Dict[str, Any]:
    """
    Robust deterministic rule-based parser used when offline or as a secondary check.
    Generates clean, human-readable, and context-accurate explanations.
    """
    text = note.strip()
    text_lower = text.lower()

    # Rule 1: Distractor checks
    distractor_words = ["cafeteria", "menu", "lunch", "dinner", "shuttle", "bus", "library", "meeting", "holiday", "syllabus"]
    if any(w in text_lower for w in distractor_words) and not any(k in text_lower for k in ["solar", "battery", "grid", "kwh"]):
        return {
            "note_index": note_index,
            "applies": False,
            "directive_type": "no_op",
            "structured_adjustment": None,
            "explanation": "This note does not affect today's energy schedule."
        }

    hours = extract_time_window(text)
    time_str = format_hours_window(hours) if hours else "during specified hours"

    # Rule 2: Solar reduction
    if any(k in text_lower for k in ["solar", "pv production", "rooftop solar", "panel cleaning", "panel washing"]):
        factor = 0.2  # Default common benchmark
        if "one-fifth" in text_lower:
            factor = 0.2
        elif "one-fourth" in text_lower or "quarter" in text_lower:
            factor = 0.25
        elif "half" in text_lower:
            factor = 0.5
        else:
            # Check for percentages: "drop to about 20%" vs "80% reduction"
            m_drop_to = re.search(r"(?:drop to|leave roughly|about|at)\s*(\d{1,2})%", text_lower)
            m_reduc = re.search(r"(\d{1,2})%\s*(?:reduction|drop|cut)", text_lower)
            if m_drop_to:
                factor = float(m_drop_to.group(1)) / 100.0
            elif m_reduc:
                reduc_pct = float(m_reduc.group(1))
                factor = max(0.0, (100.0 - reduc_pct) / 100.0)

        if hours:
            pct = int(round(factor * 100))
            return {
                "note_index": note_index,
                "applies": True,
                "directive_type": "solar_reduction",
                "structured_adjustment": {"hours": hours, "factor": factor},
                "explanation": f"Solar availability reduced to {pct}% {time_str}."
            }

    # Rule 3: No charge window
    if any(k in text_lower for k in ["not charge", "no charging", "stop charging", "charge unavailable", "no battery charging"]):
        if hours:
            return {
                "note_index": note_index,
                "applies": True,
                "directive_type": "no_charge_window",
                "structured_adjustment": {"hours": hours},
                "explanation": f"Battery charging prohibited {time_str}."
            }

    # Rule 4: No discharge window
    if any(k in text_lower for k in ["not discharge", "no discharging", "stop discharging", "discharge unavailable", "do not pull battery power"]):
        if hours:
            return {
                "note_index": note_index,
                "applies": True,
                "directive_type": "no_discharge_window",
                "structured_adjustment": {"hours": hours},
                "explanation": f"Battery discharging prohibited {time_str}."
            }

    # Rule 5: Minimum battery reserve
    if any(k in text_lower for k in ["reserve", "minimum energy", "keep at least"]):
        m_kwh = re.search(r"(\d+(?:\.\d+)?)\s*kwh", text_lower)
        kwh = float(m_kwh.group(1)) if m_kwh else 100.0
        val_str = f"{int(kwh)}" if kwh.is_integer() else f"{kwh}"
        if hours:
            return {
                "note_index": note_index,
                "applies": True,
                "directive_type": "minimum_battery_reserve",
                "structured_adjustment": {"hours": hours, "minimum_energy_kwh": kwh},
                "explanation": f"Keep at least {val_str} kWh in reserve {time_str}."
            }

    # Rule 6: Max grid window
    if any(k in text_lower for k in ["grid import", "caps import", "not exceed", "max grid", "import capped"]):
        m_kwh = re.search(r"(\d+(?:\.\d+)?)\s*kwh", text_lower)
        kwh = float(m_kwh.group(1)) if m_kwh else 50.0
        val_str = f"{int(kwh)}" if kwh.is_integer() else f"{kwh}"
        if hours:
            return {
                "note_index": note_index,
                "applies": True,
                "directive_type": "max_grid_window",
                "structured_adjustment": {"hours": hours, "max_grid_kwh": kwh},
                "explanation": f"Grid import capped at {val_str} kWh {time_str}."
            }

    # Default fallback: no_op
    return {
        "note_index": note_index,
        "applies": False,
        "directive_type": "no_op",
        "structured_adjustment": None,
        "explanation": "This note does not affect today's energy schedule."
    }


def parse_json_from_llm_response(raw_text: str) -> List[Dict[str, Any]]:
    """
    Safely extracts a JSON list of directive interpretations from LLM output text.
    Handles Markdown code blocks and surrounding whitespace.
    """
    cleaned = raw_text.strip()
    if cleaned.startswith("```"):
        # Remove opening fence
        lines = cleaned.split("\n")
        if lines[0].startswith("```"):
            lines = lines[1:]
        if lines and lines[-1].strip().startswith("```"):
            lines = lines[:-1]
        cleaned = "\n".join(lines).strip()

    try:
        data = json.loads(cleaned)
        if isinstance(data, list):
            return data
        if isinstance(data, dict):
            # Sometimes an LLM wraps the list in {"directives": [...]}
            for val in data.values():
                if isinstance(val, list):
                    return val
            return [data]
    except json.JSONDecodeError:
        pass

    # Regex search for first JSON array in string
    match = re.search(r"\[\s*\{.*\}\s*\]", raw_text, re.DOTALL)
    if match:
        try:
            return json.loads(match.group(0))
        except json.JSONDecodeError:
            pass

    return []
