# services/__init__.py
from .auth_service_headless import XafiroAuthServiceHeadless
from .scraping_service_headless import ScrapingServiceHeadless

__all__ = [
    "XafiroAuthServiceHeadless",
    "ScrapingServiceHeadless"
]
