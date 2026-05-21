"""
Agency lead generation: find WooCommerce stores with low tech-quality score.

These are prime candidates for WP-agency pitches: WordPress upgrades,
caching, security, SEO consulting.

    export APIFY_API_TOKEN=apify_api_xxxxxx
    python examples/agency_prospecting.py
"""

from woocommerce_analyzer import WooCommerceAnalyzerClient


CANDIDATES = [
    "https://woocommerce.com",
    # Replace with target stores
]


def main() -> None:
    client = WooCommerceAnalyzerClient()
    results = client.analyze(CANDIDATES, max_concurrency=5)

    leads_low_quality = []
    leads_no_seo = []
    leads_no_caching = []
    leads_no_security = []
    leads_outdated_wp = []

    for r in results:
        if not r.get("success"):
            continue
        tech = set(r.get("tech_stack") or [])
        score = r.get("tech_quality_score") or 0
        wp_ver = r.get("wordpress_version") or ""

        if score < 30:
            leads_low_quality.append(r)
        if not (tech & {"Yoast SEO", "Rank Math", "All in One SEO"}):
            leads_no_seo.append(r)
        if not (tech & {"WP Rocket", "LiteSpeed Cache", "W3 Total Cache",
                        "WP Super Cache", "Cloudflare"}):
            leads_no_caching.append(r)
        if not (tech & {"Wordfence", "Sucuri", "iThemes Security"}):
            leads_no_security.append(r)
        # Outdated WP detection: anything < 6.0
        try:
            major = int(wp_ver.split(".")[0]) if wp_ver else 0
            if 0 < major < 6:
                leads_outdated_wp.append(r)
        except Exception:
            pass

    def _print_group(group, label, pitch):
        print(f"\n=== {label} ({len(group)}) — pitch: {pitch} ===")
        for r in group[:10]:
            score = r.get("tech_quality_score", 0)
            rev = (r.get("revenue_estimate") or {}).get("monthly_revenue_usd_est") or 0
            wp = r.get("wordpress_version") or "?"
            print(f"  {r.get('domain', '?')[:30]:<30} quality={score:>3} "
                  f"WP={wp:<7} rev=${rev:,.0f}/mo")

    _print_group(leads_outdated_wp, "OUTDATED WORDPRESS",
                 "WordPress upgrade + security audit")
    _print_group(leads_no_caching, "NO CACHING PLUGIN",
                 "Site speed optimization service")
    _print_group(leads_no_security, "NO SECURITY PLUGIN",
                 "Wordfence/Sucuri install + monthly monitoring")
    _print_group(leads_no_seo, "NO SEO PLUGIN",
                 "SEO setup + content strategy")
    _print_group(leads_low_quality, "LOW TECH QUALITY (< 30)",
                 "Full WP overhaul / migration to managed hosting")


if __name__ == "__main__":
    main()
