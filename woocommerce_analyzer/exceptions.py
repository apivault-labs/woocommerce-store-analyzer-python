"""Exception classes for the WooCommerce Store Analyzer SDK."""


class WooCommerceAnalyzerError(Exception):
    """Base exception for all SDK errors."""


class AuthenticationError(WooCommerceAnalyzerError):
    """Raised when the Apify API token is missing or invalid."""


class ActorRunError(WooCommerceAnalyzerError):
    """Raised when the actor run fails on Apify infrastructure."""


class ActorTimeoutError(WooCommerceAnalyzerError):
    """Raised when the actor run does not finish within the allowed timeout."""
