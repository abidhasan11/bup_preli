import os
from typing import Optional
from pydantic import BaseModel
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseModel):
    # Service settings
    app_name: str = "GridWise LLM Energy Optimizer"
    version: str = "1.0.0"
    host: str = os.getenv("HOST", "0.0.0.0")
    port: int = int(os.getenv("PORT", "8000"))
    
    # LLM Settings
    gemini_api_key: Optional[str] = os.getenv("GEMINI_API_KEY")
    # Default to modern fast Gemini model, with fallback support
    gemini_model: str = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")
    
    # Numeric tolerances
    tolerance_kwh: float = 0.01
    tolerance_bdt: float = 0.01

settings = Settings()
