import os
from pathlib import Path
from dotenv import load_dotenv

# Load .env explicitly from the backend directory
env_path = Path(__file__).resolve().parent.parent / ".env"
load_dotenv(dotenv_path=env_path)

DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise RuntimeError(
        "CRITICAL ERROR: DATABASE_URL environment variable is missing. "
        "PostgreSQL is required for AdaptiveClass AI. "
        "Please specify a valid PostgreSQL connection URL in backend/.env"
    )

if not (DATABASE_URL.startswith("postgresql://") or DATABASE_URL.startswith("postgresql+psycopg://") or DATABASE_URL.startswith("postgresql+psycopg2://")):
    raise RuntimeError(
        f"CRITICAL ERROR: Invalid database scheme in DATABASE_URL: {DATABASE_URL}. "
        "AdaptiveClass AI strictly requires PostgreSQL. SQLite fallback is disabled."
    )

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "").strip()
PORT = int(os.getenv("PORT", "8000"))
HOST = os.getenv("HOST", "0.0.0.0")

CORS_ORIGINS = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]
