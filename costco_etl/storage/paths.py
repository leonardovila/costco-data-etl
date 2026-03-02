# costco_etl/storage/paths.py

from pathlib import Path

# Repo root
REPO_ROOT = Path(__file__).resolve().parents[2]

# --- Deterministic DB path (server-first architecture) ---

SERVER_DB_PATH = Path("/opt/costco_api/data/costco.db")

if SERVER_DB_PATH.parent.exists():
    DB_PATH = SERVER_DB_PATH
else:
    DB_PATH = REPO_ROOT / "costco.db"

LOGS_DIR = REPO_ROOT / "logs"