"""
WooCommerce Store Analyzer — Python SDK

Official Python client for the apivault_labs/woocommerce-store-analyzer Apify actor.
Get revenue, traffic, brand age, 70+ plugins detected, tech stack, tracking IDs,
dropshipper risk, international expansion for any WooCommerce store — all in one
API call.

Quick start:

    from woocommerce_analyzer import WooCommerceAnalyzerClient

    client = WooCommerceAnalyzerClient(api_token="apify_api_xxxxxx")
    result = client.analyze_one("https://store.com")

    print(result["revenue_estimate"]["monthly_revenue_usd_est"])
    print(result["tech_quality_score"])

See https://github.com/apivault-labs/woocommerce-store-analyzer-python for full docs.
"""

from .client import WooCommerceAnalyzerClient
from .exceptions import (
    WooCommerceAnalyzerError,
    AuthenticationError,
    ActorRunError,
    ActorTimeoutError,
)

__version__ = "0.1.0"
__all__ = [
    "WooCommerceAnalyzerClient",
    "WooCommerceAnalyzerError",
    "AuthenticationError",
    "ActorRunError",
    "ActorTimeoutError",
]
