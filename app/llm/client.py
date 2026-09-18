import logging
import httpx
from typing import List, Dict, Any
from app.config import settings
from app.llm.prompts import SYSTEM_PROMPT
from app.llm.parser import parse_json_from_llm_response, regex_fallback_parse_note

logger = logging.getLogger(__name__)


async def interpret_operator_notes(notes: List[str]) -> List[Dict[str, Any]]:
    """
    Interprets 1-3 operator notes using the Gemini API.
    If no API key is provided or if network fails, falls back gracefully to the deterministic parser.
    """
    if not notes:
        return []

    # If Gemini API key is configured, invoke the model
    if settings.gemini_api_key:
        try:
            # Build prompt with exact note indices
            user_content = "Please parse the following campus operator notes into structured directives:\n"
            for i, note in enumerate(notes):
                user_content += f"Note {i}: \"{note}\"\n"

            payload = {
                "contents": [
                    {
                        "role": "user",
                        "parts": [{"text": user_content}]
                    }
                ],
                "systemInstruction": {
                    "parts": [{"text": SYSTEM_PROMPT}]
                },
                "generationConfig": {
                    "responseMimeType": "application/json",
                    "temperature": 0.0,
                }
            }

            url = f"https://generativelanguage.googleapis.com/v1beta/models/{settings.gemini_model}:generateContent?key={settings.gemini_api_key}"
            
            async with httpx.AsyncClient(timeout=10.0) as client:
                resp = await client.post(url, json=payload)
                if resp.status_code == 200:
                    data = resp.json()
                    candidates = data.get("candidates", [])
                    if candidates:
                        part_text = candidates[0].get("content", {}).get("parts", [{}])[0].get("text", "")
                        parsed = parse_json_from_llm_response(part_text)
                        if parsed and len(parsed) == len(notes):
                            return parsed
                else:
                    logger.warning(f"Gemini API returned status {resp.status_code}: {resp.text}")
        except Exception as e:
            logger.warning(f"Failed to query Gemini API: {e}. Falling back to deterministic NLP parser.")

    # Graceful fallback: run deterministic rule-based extractor
    fallback_results: List[Dict[str, Any]] = []
    for i, note in enumerate(notes):
        fallback_results.append(regex_fallback_parse_note(note, i))

    return fallback_results
