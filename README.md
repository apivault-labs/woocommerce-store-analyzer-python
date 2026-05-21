# WooCommerce Store Analyzer — Python SDK

> **Spy on any WooCommerce store: revenue, traffic, brand age, 70+ plugins detected, tech stack, tracking IDs, dropshipper risk, international expansion — all in one API call.**

Python client for the [WooCommerce Store Analyzer Apify Actor](https://apify.com/apivault_labs/woocommerce-store-analyzer) — get **56+ intelligence fields** for any WooCommerce store using only public data sources.

[![Apify Actor](https://img.shields.io/badge/Apify-Actor-blue?logo=apify)](https://apify.com/apivault_labs/woocommerce-store-analyzer)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Python 3.9+](https://img.shields.io/badge/python-3.9%2B-blue.svg)](https://www.python.org/)
[![PyPI-friendly](https://img.shields.io/badge/install-pip-success)](#installation)

---

## What it does

WooCommerce powers ~30% of all online stores worldwide. For any WooCommerce URL, this actor returns a single rich JSON record combining **8 public data sources** and **20+ derived intelligence signals**.

A direct, pay-per-use alternative to:
- [BuiltWith](https://builtwith.com) ($295+/mo)
- [Wappalyzer](https://wappalyzer.com) ($150+/mo)
- [SimilarWeb Pro](https://www.similarweb.com)
- [Commerce Inspector](https://commerceinspector.com) ($10/mo, Shopify-focused)

**Pricing:** $0.01 per store analyzed. No subscriptions, no credits expiring, no rate limits.

---

## Quick start

```python
from woocommerce_analyzer import WooCommerceAnalyzerClient

client = WooCommerceAnalyzerClient(api_token="apify_api_xxxxxx")

result = client.analyze_one("https://store.com")

print(f"Revenue:       ${result['revenue_estimate']['monthly_revenue_usd_est']:,}/mo")
print(f"Traffic:       {result['traffic']['monthly_visits']:,} visits/mo")
print(f"WP version:    {result.get('wordpress_version', '?')}")
print(f"WC version:    {result.get('woocommerce_version', '?')}")
print(f"Plugins:       {result['plugins_count']}")
print(f"Tech quality:  {result['tech_quality_score']}/100")
print(f"Risk:          {result['dropshipper_risk_score']}/100 ({result['dropshipper_risk_bucket']})")
```

Output:
```
Revenue:       $1,843,570/mo
Traffic:       1,393,477 visits/mo
WP version:    7.0
WC version:    8.4.1
Plugins:       3
Tech quality:  90/100
Risk:          0/100 (low)
```

---

## Installation

```bash
pip install git+https://github.com/apivault-labs/woocommerce-store-analyzer-python.git
```

Or clone and use directly:

```bash
git clone https://github.com/apivault-labs/woocommerce-store-analyzer-python.git
cd woocommerce-store-analyzer-python
pip install -r requirements.txt
```

Requires Python 3.9+ and the [`requests`](https://pypi.org/project/requests/) library.

---

## Get your API token (free)

1. Sign up at [apify.com](https://apify.com) — free tier includes $5 monthly credits, no card required
2. Go to [Account → Integrations](https://console.apify.com/account/integrations)
3. Copy your Personal API token

```bash
export APIFY_API_TOKEN=apify_api_xxxxxxxxxxxxxxxxxxxxxxxx
```

Or pass it explicitly:

```python
client = WooCommerceAnalyzerClient(api_token="apify_api_xxxxxx")
```

---

## What you get for $0.01 per store

### 💰 Revenue & Traffic Intelligence
- **Estimated monthly revenue** (visits × CR × AOV)
- **Annualized revenue** projection
- **Monthly visits** + 3-month trend (SimilarWeb)
- Global rank, country rank, category rank
- Bounce rate, page per visit, avg time on site
- Top 5 countries by traffic share
- Traffic sources breakdown (search/social/paid/direct/...)
- Top 10 keywords with search volume + CPC

### 🔌 Plugin Detection (two methods)
1. **HTML scan** — plugin slugs from `/wp-content/plugins/<slug>/`
2. **WP REST namespaces** — plugins that register REST endpoints (more reliable)

### 🛠️ Tech Stack (70+ apps)
- **Page builders:** Elementor, Divi, WPBakery, Beaver Builder, Oxygen, Bricks
- **Payments:** Stripe, PayPal, Square, Klarna, Afterpay, Sezzle, Affirm
- **Reviews:** Judge.me, Yotpo, Loox, Trustpilot
- **Email:** Klaviyo, Mailchimp, MailPoet, ActiveCampaign, ConvertKit, HubSpot
- **SEO:** Yoast, Rank Math, AIOSEO
- **Cache:** WP Rocket, W3 Total Cache, LiteSpeed, NitroPack, Cloudflare
- **Pixels:** Facebook, TikTok, Pinterest, Google, Microsoft Clarity, Hotjar
- **Hosting hints:** WP Engine, Kinsta, SiteGround, Hostinger
- **Security:** Wordfence, Sucuri, iThemes Security
- **Multilingual:** WPML, Polylang, TranslatePress
- **LMS:** MemberPress, LearnDash, LifterLMS

### 🎯 Tracking IDs (unique feature)
Public advertising IDs for **brand-network mapping**:
- Google Tag Manager, GA4, Universal Analytics
- Facebook Pixel, TikTok Pixel, Pinterest Tag
- Klaviyo public key, Hotjar, Microsoft Clarity

> Same FB Pixel on two domains = same operator. Detect parallel WooCommerce brands.

### 🌐 Sitemap Totals
- Real product / page / post / category counts (from `/sitemap.xml`)

### ⏱️ Brand Age
- Earliest Wayback Machine snapshot
- Earliest SSL certificate (via crt.sh)
- Estimated brand age + founding year

### 🌍 International Expansion
- All hreflang languages
- Currency switcher / country selector flags
- WPML / Polylang detection
- **International expansion score (0-100)**

### 🏷️ WordPress Meta
- WordPress version (from generator meta)
- WooCommerce version (from asset paths)
- Active theme, currency, OG metadata

### 🧠 Derived Intelligence
- **`tech_quality_score`** (0-100) with explained signals — composite quality
- **`dropshipper_risk_score`** (0-100) — heuristic detection (alidropship, dropified, spocket)
- **`customer_segment`** — mass-market / mid-market / premium / luxury
- **`marketing_channel_mix`** — search-driven / social-driven / paid-driven / brand-driven
- **`international_expansion_score`** (0-100)

### 📱 Social & Contact
- Instagram, Facebook, Twitter/X, TikTok, YouTube, Pinterest, LinkedIn handles
- Public emails and phones from homepage

---

## Examples

See [`examples/`](examples) for full code:

| File | What it does |
|---|---|
| [`quickstart.py`](examples/quickstart.py) | Analyze one store, print key metrics |
| [`bulk_analyze.py`](examples/bulk_analyze.py) | Analyze 50+ stores in parallel |
| [`find_dropshippers.py`](examples/find_dropshippers.py) | Filter stores by dropshipper risk score |
| [`agency_prospecting.py`](examples/agency_prospecting.py) | Find WC stores with outdated WP/WC for agency leads |
| [`plugin_research.py`](examples/plugin_research.py) | Aggregate plugin usage across niche stores |
| [`brand_network_detector.py`](examples/brand_network_detector.py) | Detect domains sharing the same FB Pixel/GTM |
| [`export_to_csv.py`](examples/export_to_csv.py) | Save results to CSV / Excel |

---

## API reference

### `WooCommerceAnalyzerClient(api_token=None, timeout=600)`

| Param | Type | Description |
|---|---|---|
| `api_token` | `str` | Apify API token. Falls back to `APIFY_API_TOKEN` env var. |
| `timeout` | `int` | Max seconds to wait for analysis. Default 600 (10 min). |

### `client.analyze(store_urls, **kwargs)`

Analyze multiple stores synchronously.

| Param | Type | Default | Description |
|---|---|---|---|
| `store_urls` | `list[str]` | required | WooCommerce store URLs (or bare domains) |
| `conversion_rate` | `float` | 1.8 | % for revenue formula. Industry: 1.5–2% |
| `product_sample_size` | `int` | 200 | Products to sample (0 = full catalog) |
| `max_concurrency` | `int` | 3 | Parallel stores to analyze |

Plus boolean toggles to skip layers for speed:

| Flag | Default | Effect |
|---|---|---|
| `extract_traffic` | `True` | Pull SimilarWeb data |
| `extract_revenue_estimate` | `True` | Compute revenue formula |
| `extract_tech_stack` | `True` | Detect 70+ apps + tracking IDs |
| `extract_plugins` | `True` | Plugin slugs from HTML |
| `extract_wp_namespaces` | `True` | Active plugins via WP REST |
| `extract_sitemap` | `True` | Real totals from sitemap.xml |
| `extract_brand_age` | `True` | Wayback + crt.sh lookups |
| `extract_international` | `True` | hreflang + currency switcher |
| `extract_derived_signals` | `True` | tech_quality_score, dropshipper_risk_score |

Returns: `list[dict]` — one record per store.

### `client.analyze_one(store_url, **kwargs)`
Convenience wrapper for single-store analysis. Returns one `dict`.

### `client.find_by_revenue(store_urls, min_usd_per_month, **kwargs)`
Filter analyzed stores by minimum estimated monthly revenue.

### `client.find_outdated_wp(store_urls, max_wp_version=6.0, **kwargs)`
Find stores running WordPress older than X.Y — agency lead generation.

### `client.estimate_cost(store_count)`
Returns the estimated USD cost for analyzing `store_count` stores.

---

## Sample output

```json
{
  "domain": "store.com",
  "wordpress_version": "6.4.2",
  "woocommerce_version": "8.4.1",
  "theme_slug": "astra",
  "currency": "USD",
  "tech_stack": ["WooCommerce", "Elementor", "Stripe", "Klaviyo", "Yoast SEO", "WP Rocket"],
  "tracking_ids": {
    "google_tag_manager": "GTM-ABC1234",
    "facebook_pixel": "1234567890123456"
  },
  "plugins_detected": ["woocommerce", "elementor", "klaviyo", "yoast-seo"],
  "plugins_count": 24,
  "wp_namespaces": ["yoast/v1", "wpforms/v1", "elementor/v1"],
  "wp_rest_alive": true,
  "sitemap_products": 487,
  "sitemap_pages": 24,
  "hreflangs_count": 3,
  "international_expansion_score": 50,
  "estimated_brand_age_years": 4.2,
  "estimated_founded_year": 2022,
  "traffic": {
    "monthly_visits": 187432,
    "global_rank": 89321,
    "category_rank": 421,
    "top_countries": [{"country_code": "US", "share": 0.74}]
  },
  "revenue_estimate": {
    "monthly_revenue_usd_est": 247943,
    "annualized_revenue_usd_est": 2975316,
    "conversion_rate_used_pct": 1.8
  },
  "customer_segment": "mid-market",
  "marketing_channel_mix": "search-driven (52%)",
  "tech_quality_score": 90,
  "tech_quality_signals": ["WP 6.3+", "WC 8.x+", "modern payments", "caching layer", "SEO plugin", "email marketing"],
  "dropshipper_risk_score": 0,
  "dropshipper_risk_bucket": "low"
}
```

---

## Use cases

### 🥇 WP-agency prospecting
Find stores with **outdated WordPress / WooCommerce versions**, **no caching**, **no security plugin**, **no SEO plugin** — perfect leads for WP optimization services.

```python
candidates = ["https://store1.com", "https://store2.com", ...]
outdated = client.find_outdated_wp(candidates, max_wp_version=6.0)
# → list of stores with WP < 6.0 — pitch WP upgrade
```

### 🥈 Plugin/SaaS sales
Find WC stores **using your competitor** (e.g. Mailchimp → pitch Klaviyo) or **NOT using** your category (e.g. no Wordfence → pitch security).

```python
stores = client.analyze(candidates)
no_klaviyo = [s for s in stores
              if "Klaviyo" not in (s.get("tech_stack") or [])
              and s.get("revenue_estimate", {}).get("monthly_revenue_usd_est", 0) > 50000]
```

### 🥉 Dropshipping competitor research
Verify a competitor's revenue **before** copying. Filter `dropshipper_risk_score < 25 + revenue > $50K/mo` to find legit niches worth entering.

### 🎯 Plugin research at scale
Aggregate `top_plugins` across 100 stores in a niche → see which plugin combinations correlate with success.

### 📊 Investment due diligence
Verify claimed revenue. Cross-check brand age via Wayback + SSL. Detect tech stack maturity.

### Brand network detection
Use `tracking_ids` to detect domains sharing the same Facebook Pixel or GTM container — same operator behind multiple WC brands.

```python
stores = client.analyze(candidates)
fb_pixel_groups = {}
for s in stores:
    pixel = s.get("tracking_ids", {}).get("facebook_pixel")
    if pixel:
        fb_pixel_groups.setdefault(pixel, []).append(s["domain"])

# Detect networks
for pixel, domains in fb_pixel_groups.items():
    if len(domains) > 1:
        print(f"Same FB Pixel {pixel}: {domains}")
```

### Market research
Track 100+ WC competitors weekly. Compare AOV, plugin choices, customer segment.

---

## Pricing

Pay only for what you analyze:

| Volume | Cost |
|---|---|
| 1 store | $0.01 |
| 100 stores | $1.00 |
| 1,000 stores | $10.00 |
| 10,000 stores | $100.00 |

Free Apify tier includes ~$5 monthly credit — analyze ~500 stores per month for free.

---

## How it works

All sources are **public and free** — no logins, no API keys, no proxies:

1. **`/wp-json/wc/store/v1/products`** — WooCommerce Store API (default-on since WC 4.7)
2. **`/wp-json/wc/store/v1/products/categories`** — public category metadata
3. **`/wp-json/`** — list of registered REST namespaces (active plugins fingerprint)
4. **`/sitemap.xml` / `/wp-sitemap.xml`** — recursive child sitemaps for real totals
5. **Homepage HTML** — parsed for plugins, theme, tech stack, tracking IDs, hreflang, currency
6. **SimilarWeb public API** — stable for years
7. **Wayback Machine** — first snapshot date
8. **crt.sh** — SSL certificate transparency logs

Revenue estimate uses the industry-standard formula:
```
estimated_revenue = monthly_visits × conversion_rate × AOV
AOV = median_price × 1.5
```

---

## Speed & reliability

- **8–12 seconds per store** (parallel HTTP, no rendering)
- **3 stores in parallel** by default (configurable up to 10)
- **No proxies needed** — all sources work from datacenter IPs
- **Graceful degradation** — if Wayback is slow, other layers still return data

---

## FAQ

**Q: Will it work on every WooCommerce store?**
A: Yes — every store with the Store API enabled (default since WC 4.7, ~95%+ of stores). Stores that disable it return an error and skip cleanly.

**Q: How accurate is the revenue estimate?**
A: For stores with 100K+ monthly visits: usually within ±25% of public revenue. Smaller stores: less reliable due to SimilarWeb sampling. Treat as an order-of-magnitude estimate.

**Q: Can I detect Shopify stores too?**
A: Use the companion **[Shopify Store Analyzer](https://apify.com/apivault_labs/shopify-store-analyzer)**.

**Q: How is `tech_quality_score` computed?**
A: Composite of WP/WC versions + modern payments + caching + security + SEO + email marketing + premium hosting. Stores scoring 70+ are well-maintained DTC brands; <30 = abandoned/legacy.

**Q: How accurate is `dropshipper_risk_score`?**
A: Heuristic. Scores 50+ almost always indicate dropshippers. Under 25 = legit brands. 25–50 needs manual review.

**Q: How is brand age estimated?**
A: Earliest of (Wayback first snapshot, crt.sh first SSL cert). For domains older than ~2010, usually within ±1–2 years of actual founding.

**Q: Can I run this without Apify?**
A: This package is a thin wrapper around the hosted actor. The actor handles infrastructure, retries, parallelism. Self-hosted scraping at scale is a separate undertaking.

---

## Related Apify actors

- [WooCommerce Product Scraper](https://apify.com/apivault_labs/woocommerce-product-scraper) — full catalog extraction with variants
- [Shopify Store Analyzer](https://apify.com/apivault_labs/shopify-store-analyzer) — same intelligence for Shopify
- [WordPress Plugin Detector](https://apify.com/apivault_labs/wp-plugin-detector) — detect WP plugins on any site
- [Domain Intelligence Scraper](https://apify.com/apivault_labs/domain-intelligence-scraper) — WHOIS, DNS, SSL, subdomains

See [all actors by apivault_labs](https://apify.com/apivault_labs).

---

## License

MIT — see [LICENSE](LICENSE).

This client is open source. The underlying Apify actor is a paid service ($0.01/store).

---

## Keywords

`woocommerce-analyzer` `woocommerce-store-analyzer` `wordpress-analyzer` `wp-analyzer` `wp-plugin-detector` `wordpress-plugin-detection` `ecommerce-intelligence` `store-intelligence` `builtwith-alternative` `wappalyzer-alternative` `similarweb-alternative` `commerce-inspector-alternative` `competitor-intelligence` `wp-agency-prospecting` `wp-lead-generation` `dropshipper-detection` `dropshipper-risk-score` `brand-network-mapping` `tracking-id-extraction` `wc-store-api` `wp-rest-api` `wordpress-rest` `web-scraping` `apify` `apify-actor` `python-sdk` `tech-stack-detection`
