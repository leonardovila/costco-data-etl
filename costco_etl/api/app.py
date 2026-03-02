import sqlite3
import json
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from costco_etl.storage.paths import DB_PATH


def get_connection():
    conn = sqlite3.connect(str(DB_PATH), timeout=30)
    conn.row_factory = sqlite3.Row
    return conn


app = FastAPI(title="costco-data-etl api")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root():
    return {"status": "api ok"}

@app.get("/categories/tree")
def get_category_tree():
    try:
        conn = get_connection()
        try:
            row = conn.execute(
                "SELECT payload, updated_at FROM category_map ORDER BY id DESC LIMIT 1"
            ).fetchone()

            if not row:
                raise HTTPException(status_code=404, detail="Category tree not found")

            return {
                "category_tree": json.loads(row["payload"]),
                "updated_at": row["updated_at"]
            }

        finally:
            conn.close()

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))