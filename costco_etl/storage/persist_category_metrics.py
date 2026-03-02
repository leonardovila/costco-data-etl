import sqlite3

def persist_category_metrics(db_path: str, clean_category_tree: dict) -> None:
    """
    Calculates category metrics and stores them in categories table.
    """

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    try:

        categories = extract_categories(clean_category_tree)

        # ---- DEDUPE POR URL (evita UNIQUE constraint failed) ----
        unique_by_url = {}
        for c in categories:
            url = c.get("url")
            if not url:
                continue
            unique_by_url[url] = c

        categories = list(unique_by_url.values())
        # ----------------------------------------------------------

        for cat in categories:

            url = cat["url"]
            name = cat["name"]
            level = cat["level"]

            cursor.execute(
                """
                SELECT
                    COUNT(DISTINCT p.id),
                    SUM(COALESCE(p.review_count, 0)),
                    AVG(p.rating),
                    AVG(p.min_price),
                    SUM(
                        CASE
                            WHEN p.min_price IS NOT NULL
                             AND p.max_price IS NOT NULL
                             AND p.min_price < p.max_price
                            THEN 1
                            ELSE 0
                        END
                    )
                FROM product_categories pc
                JOIN products p ON p.id = pc.product_id
                WHERE pc.category_url = ?
                """,
                (url,)
            )

            result = cursor.fetchone()

            product_count = result[0] or 0
            total_reviews = result[1] or 0
            avg_rating = result[2]
            avg_min_price = result[3]
            sale_count = result[4] or 0

            cursor.execute(
                """
                INSERT INTO categories (
                    url,
                    name,
                    level,
                    product_count,
                    total_reviews,
                    avg_rating,
                    avg_min_price,
                    sale_count
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    url,
                    name,
                    level,
                    product_count,
                    total_reviews,
                    avg_rating,
                    avg_min_price,
                    sale_count,
                )
            )

        conn.commit()

    finally:
        conn.close()


def extract_categories(tree: dict) -> list:
    """
    Flattens category tree into list of {url, name, level}
    """

    result = []

    def traverse(node):
        result.append({
            "url": node["url"],
            "name": node["name"],
            "level": node["level"],
        })

        for child in node.get("children", {}).values():
            traverse(child)

    for root in tree.values():
        traverse(root)

    return result