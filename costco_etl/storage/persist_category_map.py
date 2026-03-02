import sqlite3
import json
from datetime import datetime


def persist_category_map(db_path: str, category_tree: dict) -> None:
    """
    Stores the full category tree JSON into category_map table.
    Replaces previous snapshot (Phase 1 model).
    """

    conn = sqlite3.connect(db_path)

    try:
        # Always keep single snapshot row (id = 1)
        conn.execute("DELETE FROM category_map")

        conn.execute(
            """
            INSERT INTO category_map (id, payload, updated_at)
            VALUES (?, ?, ?)
            """,
            (
                1,
                json.dumps(category_tree, ensure_ascii=False),
                datetime.utcnow().isoformat(),
            ),
        )

        conn.commit()

    finally:
        conn.close()