# Changelog

## [1.0.0] - 2026-03-02

### Added
- End-to-end Costco catalog scraping pipeline.
- Structured megamenu parsing and hierarchical category tree construction.
- Recursive pruning of empty categories.
- Many-to-many product-category relational mapping.
- Aggregated category metrics (review totals, average rating, price averages, sale count).
- Demo mode with controlled pagination limit.
- Real-time crawl progress events via RunContext.
- Structured execution reporting (JSON report + JSONL run logs).
- Portable path configuration with optional COSTCO_DB_PATH override.
- Editable install support via pyproject.toml.

### Infrastructure
- Modular package architecture (scraping, category_structuring, storage, observability).
- SQLite schema initialization and full rebuild mode.
- Production-ready RunContext tracing and stage instrumentation.

### Notes
Initial stable release. Designed for API exposure and VPS deployment in Phase 2.