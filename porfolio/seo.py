"""Public crawl endpoints, separate from portfolio business logic."""
from django.contrib.sitemaps import Sitemap
from django.http import HttpResponse
from django.urls import reverse
from wagtail.models import Site


class ContactSitemap(Sitemap):
    def items(self):
        return ["contact"]

    def location(self, item):
        return reverse(item)


def robots(request):
    site = Site.find_for_request(request)
    origin = site.root_url if site else request.build_absolute_uri("/").rstrip("/")
    return HttpResponse(
        "User-agent: *\nAllow: /\nDisallow: /admin/\nDisallow: /django-admin/\n"
        f"Sitemap: {origin}{reverse('sitemap')}\n",
        content_type="text/plain",
    )
