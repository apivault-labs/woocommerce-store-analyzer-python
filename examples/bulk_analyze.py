"""
Analyze many WooCommerce stores in one batch.

Sorts results by estimated monthly revenue and prints a summary table.

    export APIFY_API_TOKEN=apify_api_xxxxxx
    python examples/bulk_analyze.py
"""

from woocommerce_analyzer import WooCommerceAnalyzerClient


STORES = [
    "https://woocommerce.com",
    # Replace with your competitors
]


def main() -> None:
    client = WooCommerceAnalyzerClient(timeout=1800)
    print(f"Analyzing {len(STORES)} WooCommerce stores "
          f"(estimated cost: ${client.estimate_cost(len(STORES))})...\n")

    results = client.analyze(
        STORES,
        max_concurrency=5,
        # Speed-ups: skip slowest layers if you don't need them
        extract_brand_age=True,    # Wayback + crt.sh — slowest
        extract_traffic=True,
    )

    print(f"{'Domain':<30} {'Visits/mo':>12} {'Revenue/mo':>14} "
          f"{'Quality':>8} {'Risk':>5} {'WP':>5}")
    print("-" * 80)

    sorted_r = sorted(
        results,
        key=lambda x: -((x.get("revenue_estimate") or {})
                        .get("monthly_revenue_usd_est") or 0),
    )

    for r in sorted_r:
        if not r.get("success"):
            print(f"  ERROR: {r.get('domain', r.get('input_url', '?'))}: "
                  f"{r.get('error', '?')}")
            continue
        traffic = r.get("traffic") or {}
        revenue = r.get("revenue_estimate") or {}
        visits = traffic.get("monthly_visits") or 0
        rev = revenue.get("monthly_revenue_usd_est") or 0
        quality = r.get("tech_quality_score", 0)
        risk = r.get("dropshipper_risk_bucket", "?")[:4]
        wp = r.get("wordpress_version", "?")[:5]
        print(f"{r.get('domain', '?'):<30} {visits:>12,} "
              f"{f'${rev:,.0f}':>14} {quality:>8}/100 {risk:>5} {wp:>5}")


if __name__ == "__main__":
    main()
