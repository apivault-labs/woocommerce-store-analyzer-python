"""
Quickstart: analyze one WooCommerce store and print key metrics.

    pip install -r requirements.txt
    export APIFY_API_TOKEN=apify_api_xxxxxx
    python examples/quickstart.py
"""

from woocommerce_analyzer import WooCommerceAnalyzerClient


def main() -> None:
    client = WooCommerceAnalyzerClient()  # picks up APIFY_API_TOKEN from env

    store = "https://woocommerce.com"
    rec = client.analyze_one(store)

    print(f"\n=== {rec['domain']} ===\n")

    traffic = rec.get("traffic") or {}
    revenue = rec.get("revenue_estimate") or {}

    print(f"WordPress version:     {rec.get('wordpress_version', '?')}")
    print(f"WooCommerce version:   {rec.get('woocommerce_version', '?')}")
    print(f"Theme:                 {rec.get('theme_slug', '?')}")
    print(f"Currency:              {rec.get('currency', '?')}")
    print()
    print(f"Monthly visits:        {traffic.get('monthly_visits') or '-':,}")
    print(f"Monthly revenue:       ${revenue.get('monthly_revenue_usd_est') or 0:,}")
    print(f"Annualized revenue:    ${revenue.get('annualized_revenue_usd_est') or 0:,}")
    print(f"AOV estimate:          ${rec.get('avg_order_value') or 0}")
    print(f"Customer segment:      {rec.get('customer_segment', '?')}")
    print(f"Marketing mix:         {rec.get('marketing_channel_mix', '?')}")
    print()
    print(f"Tech quality score:    {rec.get('tech_quality_score', '?')}/100")
    for s in (rec.get("tech_quality_signals") or [])[:5]:
        print(f"  + {s}")
    print()
    print(f"Plugins detected:      {rec.get('plugins_count', 0)}")
    print(f"WP REST namespaces:    {len(rec.get('wp_namespaces') or [])}")
    print()
    print(f"Tech stack ({len(rec.get('tech_stack') or [])}):")
    for app in (rec.get("tech_stack") or [])[:10]:
        print(f"  - {app}")

    tracking = rec.get("tracking_ids") or {}
    if tracking:
        print(f"\nTracking IDs:")
        for k, v in tracking.items():
            print(f"  - {k}: {v}")

    print(f"\nDropshipper risk:      {rec.get('dropshipper_risk_score', 0)}/100 "
          f"({rec.get('dropshipper_risk_bucket', '?')})")

    age = rec.get("estimated_brand_age_years")
    if age is not None:
        print(f"Brand age:             {age} years (since {rec.get('estimated_founded_year')})")

    intl = rec.get("international_expansion_score")
    if intl is not None:
        print(f"International score:   {intl}/100")
        print(f"  hreflangs: {len(rec.get('hreflangs') or [])}")


if __name__ == "__main__":
    main()
