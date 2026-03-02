from costco_etl.scraping.get_key import run_get_key
from costco_etl.scraping.get_megamenu import run_get_megamenu
from costco_etl.scraping.parse_megamenu import run_parse_megamenu
from costco_etl.scraping.navigation_crawler import crawl_category

def _sanitize_unusual_terminators(obj):
    """
    Recursively remove problematic Unicode line separators
    (U+2028 and U+2029) from all string fields.
    """
    if isinstance(obj, dict):
        return {
            k: _sanitize_unusual_terminators(v)
            for k, v in obj.items()
        }

    if isinstance(obj, list):
        return [
            _sanitize_unusual_terminators(v)
            for v in obj
        ]

    if isinstance(obj, str):
        return (
            obj
            .replace("\u2028", " ")
            .replace("\u2029", " ")
        )

    return obj

def scrape_costco_catalog(demo: bool = False, demo_url: str = "/jewelry.html"):

    # -------------------------
    # STEP 1 — API KEY
    # -------------------------
    api_key = run_get_key()
    if not api_key:
        raise RuntimeError("API key not found")

    # -------------------------
    # STEP 2 — MEGAMENU
    # -------------------------
    megamenu = run_get_megamenu(api_key=api_key)
    if not megamenu:
        raise RuntimeError("Megamenu not found")


    # -------------------------
    # STEP 3 — PARSE MEGAMENU
    # -------------------------
    parsed = run_parse_megamenu(megamenu)

    if not parsed:
        raise RuntimeError("Parsed megamenu returned empty list")
    
    # -------------------------
    # DEMO MODE FILTER
    # -------------------------
    if demo:
        crawl_targets = [c for c in parsed if c.get("url") == demo_url]

        if not crawl_targets:
            raise RuntimeError(f"Demo category {demo_url} not found in megamenu")

        print(f"[DEMO MODE] Crawling only category: {demo_url}")
    else:
        crawl_targets = parsed

    # -------------------------
    # STEP 4 — CRAWL ALL CATEGORIES
    # -------------------------
    all_products = []

    for i, category in enumerate(crawl_targets, start=1):

        url = category["url"]

        docs = crawl_category(
            api_key=api_key,
            category_url=url,
            category_count=category["count"],
        )

        all_products.extend(docs)

    # -------------------------
    # STEP 5 — DEDUPE
    # -------------------------
    unique = {}
    duplicate_counter = 0

    for p in all_products:
        pid = p.get("id")
        if not pid:
            continue

        if pid not in unique:
            # primera vez que vemos este producto
            unique[pid] = p
        else:
            # ya existe → mergeamos categoryPath_ss
            existing = unique[pid]
            duplicate_counter += 1

            existing_paths = set(existing.get("categoryPath_ss", []))
            new_paths = set(p.get("categoryPath_ss", []))

            merged_paths = list(existing_paths.union(new_paths))

            existing["categoryPath_ss"] = merged_paths

    deduped_products = list(unique.values())

    # -------------------------
    # STEP 6 — SANITIZE
    # -------------------------
    sanitized_products = _sanitize_unusual_terminators(deduped_products)
    return sanitized_products, parsed

if __name__ == "__main__":
    scrape_costco_catalog()