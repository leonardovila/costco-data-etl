import argparse

from costco_etl.scraping.costco_scraper import scrape_costco_catalog
from costco_etl.product_categories.build_category_tree import build_category_tree
from costco_etl.product_categories.prune_category_tree import prune_category_tree
from costco_etl.storage.init_db import recreate_costco_db
from costco_etl.storage.persist_products import persist_products
from costco_etl.storage.persist_product_categories import persist_product_categories
from costco_etl.storage.persist_category_map import persist_category_map
from costco_etl.storage.persist_category_metrics import persist_category_metrics

from costco_etl.storage.paths import DB_PATH

parser = argparse.ArgumentParser(description="Costco ETL Runner")

parser.add_argument(
    "--demo",
    action="store_true",
    help="Run Costco scraper in demo mode (single category)"
)

args = parser.parse_args()

products_flat, parsed_megamenu = scrape_costco_catalog(demo=args.demo)
base_category_tree = build_category_tree(parsed_megamenu)
clean_category_tree = prune_category_tree(base_category_tree, products_flat)

recreate_costco_db(DB_PATH)
persist_products(DB_PATH, products_flat)
persist_product_categories(DB_PATH, products_flat)
persist_category_map(DB_PATH, clean_category_tree)
persist_category_metrics(DB_PATH, clean_category_tree)

