import requests
from costco_etl.observability.run_context import RunContext

BASE_URL = "https://search.costco.com/api/apps/www_costco_com/query/www_costco_com_navigation"

def _build_headers(api_key: str) -> dict:
    return {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/144.0.0.0 Safari/537.36"
        ),
        "Origin": "https://www.costco.com",
        "Referer": "https://www.costco.com/",
        "x-api-key": api_key,
    }


def _build_params(category_url: str, start: int) -> dict:
    return {
        "expoption": "lw",
        "q": "*:*",
        "locale": "en-US",
        "start": start,
        "expand": "false",
        "userLocation": "WA",
        "loc": "115-bd,1-wh,1250-3pl,1321-wm,1456-3pl,283-wm,561-wm,725-wm,731-wm,758-wm,759-wm,"
               "847_0-cor,847_0-cwt,847_0-edi,847_0-ehs,847_0-membership,847_0-mpt,847_0-spc,"
               "847_0-wm,847_1-cwt,847_1-edi,847_d-fis,847_lg_n1f-edi,847_lux_us01-edi,"
               "847_NA-cor,847_NA-pharmacy,847_NA-wm,847_ss_u362-edi,847_wp_r458-edi,"
               "951-wm,952-wm,9847-wcs",
        "whloc": "1-wh",
        "rows": 24,
        "url": category_url,
        "fq": '{!tag=item_program_eligibility}item_program_eligibility:("ShipIt")',
        "chdcategory": "true",
        "chdheader": "true",
    }

def crawl_category(
    api_key: str,
    category_url: str,
    category_count: int,    
    ctx: RunContext,
    demo: bool = False,
    max_demo_pages: int = 3,
) -> list:

    headers = _build_headers(api_key)
    all_docs = []

    # ---- First page ----
    params = _build_params(category_url, start=0)

    response = requests.get(BASE_URL, headers=headers, params=params, timeout=15)
    response.raise_for_status()

    data = response.json()
    response_block = data.get("response", {})

    docs = response_block.get("docs", [])
    num_found = response_block.get("numFound", 0)

    total_pages = (num_found // 24) + (1 if num_found % 24 else 0)
    current_page = 1

    if not docs:
        return []

    all_docs.extend(docs)

    ctx.event(
        "crawl_page_fetched",
        stage="scrape_catalog",
        category=category_url,
        page=current_page,
        total_pages=total_pages
    )

    # ---- Pagination ----
    for start in range(24, num_found, 24):
        current_page += 1

        # 🔥 DEMO LIMIT CONTROL
        if demo and current_page > max_demo_pages:
            ctx.event(
                "demo_pagination_stopped",
                stage="scrape_catalog",
                category=category_url,
                stopped_at_page=current_page - 1,
                total_available_pages=total_pages,
                max_demo_pages=max_demo_pages
            )

            break

        params = _build_params(category_url, start=start)

        response = requests.get(BASE_URL, headers=headers, params=params, timeout=15)
        response.raise_for_status()

        page_data = response.json()
        page_docs = page_data.get("response", {}).get("docs", [])

        if not page_docs:
            break

        all_docs.extend(page_docs)

        ctx.event(
            "crawl_page_fetched",
            stage="scrape_catalog",
            category=category_url,
            page=current_page,
            total_pages=total_pages
        )

    # ---- Integrity check (importante) ----
    return all_docs