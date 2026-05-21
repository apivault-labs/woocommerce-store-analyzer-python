"""
Detect brand networks: WooCommerce stores sharing the same Facebook Pixel
or Google Tag Manager container.

Same FB Pixel ID across multiple domains = same operator.
Useful for:
- OSINT / journalism (uncovering hidden brand networks)
- Investment DD (one company running 5 'independent' brands)
- Competitive intelligence (find a competitor's full portfolio)

    export APIFY_API_TOKEN=apify_api_xxxxxx
    python examples/brand_network_detector.py
"""

from collections import defaultdict

from woocommerce_analyzer import WooCommerceAnalyzerClient


CANDIDATES = [
    "https://woocommerce.com",
    # Add candidate stores you want to fingerprint
]


def main() -> None:
    client = WooCommerceAnalyzerClient()
    results = client.analyze(CANDIDATES, max_concurrency=5)

    fb_pixels = defaultdict(list)
    gtms = defaultdict(list)
    klaviyo_keys = defaultdict(list)

    for r in results:
        if not r.get("success"):
            continue
        domain = r.get("domain")
        tracking = r.get("tracking_ids") or {}
        if "facebook_pixel" in tracking:
            fb_pixels[tracking["facebook_pixel"]].append(domain)
        if "google_tag_manager" in tracking:
            gtms[tracking["google_tag_manager"]].append(domain)
        if "klaviyo_public_key" in tracking:
            klaviyo_keys[tracking["klaviyo_public_key"]].append(domain)

    def _report(groups, label):
        clusters = {k: v for k, v in groups.items() if len(v) > 1}
        print(f"\n=== {label} clusters: {len(clusters)} ===")
        for tid, domains in clusters.items():
            print(f"  ID {tid}:")
            for d in domains:
                print(f"    - {d}")

    _report(fb_pixels, "Facebook Pixel")
    _report(gtms, "Google Tag Manager")
    _report(klaviyo_keys, "Klaviyo")

    if (not any(len(v) > 1 for v in fb_pixels.values())
            and not any(len(v) > 1 for v in gtms.values())
            and not any(len(v) > 1 for v in klaviyo_keys.values())):
        print("\nNo shared tracking IDs found — these stores appear independent.")


if __name__ == "__main__":
    main()
