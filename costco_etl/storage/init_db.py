# pipeline/init_db.py
import sqlite3

def recreate_costco_db(db_path: str) -> None:
    """
    Drops and recreates all Costco tables (Phase 1 snapshot model).
    No historical data.
    Fresh rebuild every execution.
    """

    conn = sqlite3.connect(db_path)

    try:
        # ---------- DROP ALL ----------
        conn.execute("DROP TABLE IF EXISTS product_categories")
        conn.execute("DROP TABLE IF EXISTS products")
        conn.execute("DROP TABLE IF EXISTS categories")
        conn.execute("DROP TABLE IF EXISTS category_map")

        # ---------- PRODUCTS ----------
        conn.execute("""
            CREATE TABLE products (
                id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                min_price REAL,
                max_price REAL,
                rating REAL,
                image_url TEXT,
                review_count INTEGER
            )
        """)

        # ---------- PRODUCT ↔ CATEGORY (PUENTE) ----------
        conn.execute("""
            CREATE TABLE product_categories (
                product_id TEXT NOT NULL,
                category_url TEXT NOT NULL,
                PRIMARY KEY (product_id, category_url)
            )
        """)

        # ---------- CATEGORIES (ENTIDAD REAL) ----------
        conn.execute("""
            CREATE TABLE categories (
                url TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                level INTEGER NOT NULL,
                product_count INTEGER NOT NULL,
                total_reviews INTEGER NOT NULL,
                avg_rating REAL,
                avg_min_price REAL,
                sale_count INTEGER NOT NULL
            )
        """)

        # ---------- CATEGORY MAP (JSON COMPLETO) ----------
        conn.execute("""
            CREATE TABLE category_map (
                id INTEGER PRIMARY KEY,
                payload TEXT NOT NULL,
                updated_at TEXT NOT NULL
            )
        """)

        conn.commit()

    finally:
        conn.close()