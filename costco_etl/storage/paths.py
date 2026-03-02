# costco_etl/storage/paths.py

from pathlib import Path
import os

# Repo root
REPO_ROOT = Path(__file__).resolve().parents[2]

DATA_DIR = REPO_ROOT

# Permite override por env var (como Financial)
DB_PATH = Path(
    os.getenv("COSTCO_DB_PATH", DATA_DIR / "costco.db")
)

LOGS_DIR = DATA_DIR / "logs"

LOGS_DIR.mkdir(parents=True, exist_ok=True)