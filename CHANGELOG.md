## Changelog

All notable changes to this project will be documented in this file.

## [0.1.0] — 2026-05-22

### Added
- Initial release of the Python SDK
- `WooCommerceAnalyzerClient` with synchronous `analyze()`, `analyze_one()`,
  `find_by_revenue()`, and `find_outdated_wp()` methods
- Full coverage of all 14 input flags of the underlying actor:
  `extractTraffic`, `extractRevenueEstimate`, `extractTechStack`, `extractPlugins`,
  `extractWpNamespaces`, `extractSitemap`, `extractBrandAge`,
  `extractInternational`, `extractDerivedSignals`, ...
- 7 example scripts: quickstart, find_dropshippers, agency_prospecting,
  bulk_analyze, plugin_research, brand_network_detector, export_to_csv
- MIT license
