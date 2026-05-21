"""
Analyze WooCommerce stores and export the flattened results to CSV.

Drop into Excel, Google Sheets, Numbers, or import into a database.

    pip install -r requirements.txt
    export APIFY_API_TOKEN=apify_api_xxxxxx
    python examples/export_to_csv.py > stores.csv
"""

import csv
import sys

from woocommerce_analyzer import WooCommerceAnalyzerClient


STORES = [
    "https://woocommerce.com",
    # Add more stores
]

COLUMNS = [
    "domain",
    "wordpress_version",
    "woocommerce_version",
    "theme_slug",
    "currency",
    "monthly_visits",
    "monthly_revenue_usd_est",
    "annualized_revenue_usd_est",
    "avg_order_value",
    "price_min",
    "price_max",
    "price_median",
    "products_on_sale_pct",
    "in_stock_pct",
    "new_products_30d",
    "estimated_brand_age_years",
    "estimated_founded_year",
    "customer_segment",
    "marketing_channel_mix",
    "tech_quality_score",
    "dropshipper_risk_score",
    "dropshipper_risk_bucket",
    "international_expansion_score",
    "tech_stack_count",
    "tech_stack",
    "plugins_count",
    "plugins_detected",
    "wp_namespaces_count",
    "google_tag_manager",
    "facebook_pixel",
    "klaviyo_public_key",
    "instagram_handle",
]


def flatten(rec: dict) -> dict:
    traffic = rec.get("traffic") or {}
    revenue = rec.get("revenue_estimate") or {}
    tracking = rec.get("tracking_ids") or {}
    socials = rec.get("socials") or {}
    tech = rec.get("tech_stack") or []
    plugins = rec.get("plugins_detected") or []
    namespaces = rec.get("wp_namespaces") or []

    return {
        "domain": rec.get("domain"),
        "wordpress_version": rec.get("wordpress_version"),
        "woocommerce_version": rec.get("woocommerce_version"),
        "theme_slug": rec.get("theme_slug"),
        "currency": rec.get("currency"),
        "monthly_visits": traffic.get("monthly_visits"),
        "monthly_revenue_usd_est": revenue.get("monthly_revenue_usd_est"),
        "annualized_revenue_usd_est": revenue.get("annualized_revenue_usd_est"),
        "avg_order_value": rec.get("avg_order_value"),
        "price_min": rec.get("price_min"),
        "price_max": rec.get("price_max"),
        "price_median": rec.get("price_median"),
        "products_on_sale_pct": rec.get("products_on_sale_pct"),
        "in_stock_pct": rec.get("in_stock_pct"),
        "new_products_30d": rec.get("new_products_30d"),
        "estimated_brand_age_years": rec.get("estimated_brand_age_years"),
        "estimated_founded_year": rec.get("estimated_founded_year"),
        "customer_segment": rec.get("customer_segment"),
        "marketing_channel_mix": rec.get("marketing_channel_mix"),
        "tech_quality_score": rec.get("tech_quality_score"),
        "dropshipper_risk_score": rec.get("dropshipper_risk_score"),
        "dropshipper_risk_bucket": rec.get("dropshipper_risk_bucket"),
        "international_expansion_score": rec.get("international_expansion_score"),
        "tech_stack_count": len(tech),
        "tech_stack": "; ".join(tech),
        "plugins_count": rec.get("plugins_count"),
        "plugins_detected": "; ".join(plugins),
        "wp_namespaces_count": len(namespaces),
        "google_tag_manager": tracking.get("google_tag_manager"),
        "facebook_pixel": tracking.get("facebook_pixel"),
        "klaviyo_public_key": tracking.get("klaviyo_public_key"),
        "instagram_handle": socials.get("instagram"),
    }


def main() -> None:
    client = WooCommerceAnalyzerClient()
    results = client.analyze(STORES, max_concurrency=5)

    writer = csv.DictWriter(sys.stdout, fieldnames=COLUMNS)
    writer.writeheader()
    for r in results:
        if not r.get("success"):
            continue
        writer.writerow(flatten(r))


if __name__ == "__main__":
    main()
