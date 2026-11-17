"""Small, conservative cache for anonymous public Wagtail pages."""

from django.conf import settings
from django.utils.cache import add_never_cache_headers
from django.views.decorators.cache import cache_page


class PublicPageCacheMiddleware:
    """Cache only clean, anonymous GET/HEAD requests handled by Wagtail.

    Admin, forms, previews, query-string filters, and operational endpoints are
    deliberately excluded so caching cannot hide edits or user-specific state.
    """

    excluded_prefixes = (
        "/admin/",
        "/django-admin/",
        "/guest/",
        "/services/",
        "/healthz/",
        "/robots.txt",
        "/sitemap.xml",
    )

    def __init__(self, get_response):
        self.get_response = get_response
        self.timeout = getattr(settings, "PUBLIC_PAGE_CACHE_SECONDS", 0)

    def __call__(self, request):
        should_cache = (
            self.timeout > 0
            and request.method in {"GET", "HEAD"}
            and not request.GET
            and not request.user.is_authenticated
            and not request.path.startswith(self.excluded_prefixes)
            and not getattr(request, "is_preview", False)
        )

        if not should_cache:
            response = self.get_response(request)
            if request.path.startswith(("/admin/", "/django-admin/")):
                add_never_cache_headers(response)
            return response

        return cache_page(self.timeout, key_prefix="public-wagtail")(
            self.get_response
        )(request)
