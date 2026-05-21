"""
WooCommerceAnalyzerClient — synchronous wrapper around the Apify
``apivault_labs/woocommerce-store-analyzer`` actor.

The actor handles all heavy work (HTTP, parallelism, plugin detection,
brand-age estimation, FX rates, derived signals) on Apify infrastructure.
This client forwards inputs, polls until the run finishes, then downloads
the dataset.

Usage:

    from woocommerce_analyzer import WooCommerceAnalyzerClient

    client = WooCommerceAnalyzerClient(api_token="apify_api_xxxxxx")
    rec = client.analyze_one("https://store.com")

    print(rec["revenue_estimate"]["monthly_revenue_usd_est"])
    print(rec["tech_quality_score"])
"""

from __future__ import annotations

import os
import time
from typing import Any, Iterable

import requests

from .exceptions import (
    ActorRunError,
    ActorTimeoutError,
    AuthenticationError,
    WooCommerceAnalyzerError,
)


ACTOR_ID = "apivault_labs~woocommerce-store-analyzer"
APIFY_API_BASE = "https://api.apify.com/v2"

TERMINAL_OK = {"SUCCEEDED"}
TERMINAL_FAIL = {"FAILED", "TIMED-OUT", "ABORTED"}


def _wp_version_tuple(s: str | None) -> tuple[int, int, int]:
    """Parse '6.4.2' or '7.0' to (major, minor, patch). Returns (0,0,0) if invalid."""
    if not s:
        return (0, 0, 0)
    parts = str(s).split(".")
    out = [0, 0, 0]
    for i, p in enumerate(parts[:3]):
        try:
            out[i] = int(p)
        except (ValueError, TypeError):
            return (0, 0, 0)
    return tuple(out)


class WooCommerceAnalyzerClient:
    """Synchronous client for the WooCommerce Store Analyzer Apify actor.

    Parameters
    ----------
    api_token : str, optional
        Apify Personal API token. If omitted, falls back to the
        ``APIFY_API_TOKEN`` environment variable.
    timeout : int, optional
        Maximum seconds to wait for an actor run to finish. Default 600.
    poll_interval : float, optional
        Seconds between status polls. Default 3.
    base_url : str, optional
        Override the Apify API base URL (mostly for testing).
    """

    def __init__(
        self,
        api_token: str | None = None,
        timeout: int = 600,
        poll_interval: float = 3.0,
        base_url: str = APIFY_API_BASE,
    ):
        token = api_token or os.environ.get("APIFY_API_TOKEN")
        if not token:
            raise AuthenticationError(
                "Apify API token is required. Pass api_token='apify_api_...' "
                "or set the APIFY_API_TOKEN environment variable. "
                "Get a token at https://console.apify.com/account/integrations"
            )
        self._token = token
        self._timeout = int(timeout)
        self._poll_interval = float(poll_interval)
        self._base_url = base_url.rstrip("/")
        self._session = requests.Session()
        self._session.headers.update({
            "Authorization": f"Bearer {self._token}",
            "Content-Type": "application/json",
            "User-Agent": "woocommerce-analyzer-python/0.1.0",
        })

    # ------------------------------------------------------------------ public

    def analyze(
        self,
        store_urls: Iterable[str],
        *,
        conversion_rate: float = 1.8,
        product_sample_size: int = 200,
        max_concurrency: int = 3,
        actor_timeout_secs: int = 420,
        extract_products: bool = True,
        extract_velocity: bool = True,
        extract_categories: bool = True,
        extract_sitemap: bool = True,
        extract_traffic: bool = True,
        extract_revenue_estimate: bool = True,
        extract_tech_stack: bool = True,
        extract_plugins: bool = True,
        extract_wp_namespaces: bool = True,
        extract_socials: bool = True,
        extract_contact: bool = True,
        extract_wp_meta: bool = True,
        extract_international: bool = True,
        extract_brand_age: bool = True,
        extract_derived_signals: bool = True,
    ) -> list[dict[str, Any]]:
        """Run the actor and return the result records.

        See the README for the full output schema.
        """
        urls = [u for u in store_urls if u]
        if not urls:
            raise ValueError("store_urls must contain at least one non-empty URL")

        payload = {
            "storeUrls": list(urls),
            "conversionRate": float(conversion_rate),
            "productSampleSize": int(product_sample_size),
            "maxConcurrency": int(max_concurrency),
            "extractProducts": extract_products,
            "extractVelocity": extract_velocity,
            "extractCategories": extract_categories,
            "extractSitemap": extract_sitemap,
            "extractTraffic": extract_traffic,
            "extractRevenueEstimate": extract_revenue_estimate,
            "extractTechStack": extract_tech_stack,
            "extractPlugins": extract_plugins,
            "extractWpNamespaces": extract_wp_namespaces,
            "extractSocials": extract_socials,
            "extractContact": extract_contact,
            "extractWpMeta": extract_wp_meta,
            "extractInternational": extract_international,
            "extractBrandAge": extract_brand_age,
            "extractDerivedSignals": extract_derived_signals,
        }

        run_id = self._start_run(payload, actor_timeout_secs=actor_timeout_secs)
        run = self._wait_for_run(run_id)
        return self._fetch_dataset(run["defaultDatasetId"])

    def analyze_one(self, store_url: str, **kwargs: Any) -> dict[str, Any]:
        """Convenience wrapper for a single-store analysis.

        Returns the first (and only) record.
        """
        results = self.analyze([store_url], **kwargs)
        if not results:
            raise ActorRunError(
                f"Actor returned no records for {store_url!r} — "
                "the URL might not be a valid WooCommerce store."
            )
        return results[0]

    def find_by_revenue(
        self,
        store_urls: Iterable[str],
        min_usd_per_month: float,
        **kwargs: Any,
    ) -> list[dict[str, Any]]:
        """Analyze stores and return only those above a minimum monthly revenue."""
        results = self.analyze(store_urls, **kwargs)
        return [
            r for r in results
            if r.get("success")
            and (r.get("revenue_estimate") or {}).get("monthly_revenue_usd_est", 0)
            >= float(min_usd_per_month)
        ]

    def find_outdated_wp(
        self,
        store_urls: Iterable[str],
        max_wp_version: float = 6.0,
        **kwargs: Any,
    ) -> list[dict[str, Any]]:
        """Find WooCommerce stores running WordPress older than `max_wp_version`.

        Useful for WP-agency lead generation: outdated WP sites are prime
        candidates for upgrade / security / hosting pitches.

        `max_wp_version` is the threshold (e.g. 6.0 means anything < 6.0).
        """
        results = self.analyze(store_urls, **kwargs)
        threshold = (int(max_wp_version), int((max_wp_version * 10) % 10), 0)
        outdated = []
        for r in results:
            if not r.get("success"):
                continue
            wp_ver = _wp_version_tuple(r.get("wordpress_version"))
            if wp_ver != (0, 0, 0) and wp_ver < threshold:
                outdated.append(r)
        return outdated

    def estimate_cost(self, store_count: int) -> float:
        """Return estimated USD cost for `store_count × $0.01`."""
        return round(store_count * 0.01, 4)

    # ------------------------------------------------------------------ private

    def _start_run(self, payload: dict[str, Any], actor_timeout_secs: int) -> str:
        url = f"{self._base_url}/acts/{ACTOR_ID}/runs"
        params = {"timeout": int(actor_timeout_secs)}
        try:
            r = self._session.post(url, params=params, json=payload, timeout=30)
        except requests.RequestException as e:
            raise WooCommerceAnalyzerError(f"Failed to start actor run: {e}") from e

        if r.status_code == 401:
            raise AuthenticationError(
                "Apify rejected the API token. Generate a new one at "
                "https://console.apify.com/account/integrations"
            )
        if r.status_code >= 400:
            raise ActorRunError(
                f"Apify returned HTTP {r.status_code} when starting run: {r.text[:300]}"
            )

        data = r.json().get("data") or {}
        run_id = data.get("id")
        if not run_id:
            raise ActorRunError(f"Apify response missing run id: {r.text[:300]}")
        return run_id

    def _wait_for_run(self, run_id: str) -> dict[str, Any]:
        url = f"{self._base_url}/actor-runs/{run_id}"
        deadline = time.time() + self._timeout
        while True:
            try:
                r = self._session.get(url, timeout=30)
            except requests.RequestException as e:
                raise WooCommerceAnalyzerError(f"Failed to poll run status: {e}") from e

            if r.status_code >= 400:
                raise ActorRunError(
                    f"Apify returned HTTP {r.status_code} when polling run: {r.text[:300]}"
                )

            run = r.json().get("data") or {}
            status = run.get("status")
            if status in TERMINAL_OK:
                return run
            if status in TERMINAL_FAIL:
                raise ActorRunError(
                    f"Actor run {run_id} ended with status={status}: "
                    f"{run.get('statusMessage') or '(no message)'}"
                )

            if time.time() > deadline:
                raise ActorTimeoutError(
                    f"Actor run {run_id} did not finish within {self._timeout}s "
                    f"(last status={status}). Increase `timeout=` or fetch the dataset manually."
                )

            time.sleep(self._poll_interval)

    def _fetch_dataset(self, dataset_id: str) -> list[dict[str, Any]]:
        url = f"{self._base_url}/datasets/{dataset_id}/items"
        params = {"clean": "true", "format": "json"}
        try:
            r = self._session.get(url, params=params, timeout=120)
        except requests.RequestException as e:
            raise WooCommerceAnalyzerError(f"Failed to download dataset: {e}") from e

        if r.status_code >= 400:
            raise ActorRunError(
                f"Apify returned HTTP {r.status_code} when fetching dataset: "
                f"{r.text[:300]}"
            )

        try:
            data = r.json()
        except ValueError as e:
            raise ActorRunError(f"Apify dataset is not valid JSON: {e}") from e

        if not isinstance(data, list):
            raise ActorRunError(
                f"Unexpected dataset payload (not a list): {type(data).__name__}"
            )
        return data
