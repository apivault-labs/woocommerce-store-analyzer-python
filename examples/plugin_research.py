"""
Aggregate WordPress plugin usage across a niche.

Pulls store analyses for many WC stores and ranks plugins by frequency.
Useful for understanding which plugins / tools dominate in a vertical.

    export APIFY_API_TOKEN=apify_api_xxxxxx
    python examples/plugin_research.py
"""

from collections import Counter

from woocommerce_analyzer import WooCommerceAnalyzerClient


NICHE_STORES = [
    "https://woocommerce.com",
    # Replace with niche competitor stores
]


def main() -> None:
    client = WooCommerceAnalyzerClient(timeout=900)
    results = client.analyze(NICHE_STORES, max_concurrency=5)
    results = [r for r in results if r.get("success")]
    if not results:
        print("No data."); return

    plugin_counter = Counter()
    tech_counter = Counter()
    namespace_counter = Counter()

    for r in results:
        for p in r.get("plugins_detected") or []:
            plugin_counter[p] += 1
        for t in r.get("tech_stack") or []:
            tech_counter[t] += 1
        for ns in r.get("wp_namespaces") or []:
            # strip /v1 suffix
            base = ns.split("/")[0]
            namespace_counter[base] += 1

    print(f"\n=== Plugin research: {len(results)} stores ===\n")

    print("Most-used plugins (HTML scan):")
    for plugin, count in plugin_counter.most_common(15):
        pct = count / len(results) * 100
        print(f"  {plugin:30} {count:>3} ({pct:>5.1f}%)")

    print(f"\nMost-used tech / apps:")
    for app, count in tech_counter.most_common(15):
        pct = count / len(results) * 100
        print(f"  {app:30} {count:>3} ({pct:>5.1f}%)")

    print(f"\nMost-active WP REST namespaces:")
    for ns, count in namespace_counter.most_common(15):
        pct = count / len(results) * 100
        print(f"  {ns:30} {count:>3} ({pct:>5.1f}%)")


if __name__ == "__main__":
    main()
