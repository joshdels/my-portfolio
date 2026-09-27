from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static
from django.shortcuts import render
from django.http import HttpResponse
from django.template.loader import get_template

from wagtail.admin import urls as wagtailadmin_urls
from wagtail import urls as wagtail_urls

from apps.porfolio import urls as porfolio_urls
from apps.porfolio.seo import ContactSitemap, robots
from wagtail.contrib.sitemaps.views import sitemap
from wagtail.contrib.sitemaps.sitemap_generator import Sitemap


def custom_404(request, exception):
    return render(request, "404.html", status=404)


def custom_500(request):
    # No request context, CMS queries, or static manifest dependency during an outage.
    return HttpResponse(get_template("500.html").render({}), status=500)


urlpatterns = [
    path("services/", include("apps.services.urls")),
    path("robots.txt", robots, name="robots"),
    path("sitemap.xml", sitemap, {"sitemaps": {"pages": Sitemap, "contact": ContactSitemap}}, name="sitemap"),
    path("django-admin/", admin.site.urls),
    path("admin/", include(wagtailadmin_urls)),
    path("guest/", include(porfolio_urls)),
    path("", include(wagtail_urls)),
]


handler500 = "config.urls.custom_500"
handler404 = "config.urls.custom_404"


if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT,
    )
