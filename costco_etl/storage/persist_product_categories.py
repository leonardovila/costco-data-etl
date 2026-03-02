import sqlite3


def persist_product_categories(db_path: str, products_flat: list[dict]) -> None:
    """
    Inserts many-to-many product ↔ category relationships.
    Each product appears once per categoryPath_ss entry.
    """

    conn = sqlite3.connect(db_path)

    try:
        rows = []

        for product in products_flat:

            product_id = product.get("id")

            if not product_id:
                continue

            raw_paths = product.get("categoryPath_ss") or []
            seen = set()

            for category_url in raw_paths:
                if not category_url or not isinstance(category_url, str):
                    continue
                category_url = category_url.strip()
                if not category_url.startswith("/"):
                    continue
                if category_url in seen:
                    continue
                seen.add(category_url)
                rows.append((product_id, category_url))

        conn.executemany(
            """
            INSERT OR IGNORE INTO product_categories (product_id, category_url)
            VALUES (?, ?)
            """,
            rows
        )

        conn.commit()

    finally:
        conn.close()

    return {
        "relations_inserted": len(rows),
        "unique_categories_linked": len({r[1] for r in rows})
    }