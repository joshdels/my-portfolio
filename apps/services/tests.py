from unittest.mock import patch

from django.apps import apps
from django.db import OperationalError
from django.test import RequestFactory, SimpleTestCase, TestCase, override_settings
from django.urls import get_resolver, path, resolve, reverse
from wagtail.models import Page, Site

from apps.porfolio.models import HomePage
from config.urls import custom_500


def broken_view(request):
    raise RuntimeError("Simulated application failure")


urlpatterns = [path("broken/", broken_view)]
handler500 = "config.urls.custom_500"


class ServicesTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        root = Page.get_first_root_node()
        home = root.add_child(instance=HomePage(title="Home", slug="home-services"))
        site = Site.objects.get(is_default_site=True)
        site.root_page = home
        site.hostname = "testserver"
        site.port = 80
        site.save()

    def test_placeholder_metadata_navigation_and_contact(self):
        response = self.client.get(reverse("services:index"))
        self.assertContains(response, "Coming soon")
        self.assertContains(response, "Masterplan drawings to WebGIS")
        self.assertContains(response, 'href="/services/" aria-current="page"')
        self.assertContains(response, 'href="/guest/contact/"')
        self.assertContains(response, 'href="http://testserver/services/"')
        self.assertContains(response, 'content="noindex, follow"')
        self.assertNotContains(response, 'application/ld+json')
        self.assertNotContains(response, "Page not found")
        self.assertNotContains(self.client.get("/sitemap.xml"), "/services/")
        self.assertEqual(self.client.head("/services/").status_code, 200)
        self.assertEqual(self.client.post("/services/").status_code, 405)

    def test_relocated_app_retains_database_identity(self):
        config = apps.get_app_config("porfolio")
        self.assertEqual(config.name, "apps.porfolio")
        self.assertEqual(HomePage._meta.db_table, "porfolio_homepage")
        self.assertFalse(list(apps.get_app_config("services").get_models()))

    def test_services_route_takes_precedence_over_wagtail(self):
        match = resolve("/services/")
        self.assertEqual(match.view_name, "services:index")
        response = self.client.get("/services/")
        self.assertTemplateUsed(response, "services/index.html")
        self.assertTemplateUsed(response, "porfolio/base.html")

    def test_query_parameters_do_not_change_placeholder_canonical(self):
        response = self.client.get("/services/?q=parcels&type=1")
        self.assertContains(response, '<link rel="canonical" href="http://testserver/services/">', html=True)
        self.assertContains(response, 'content="noindex, follow"')
        self.assertNotContains(response, "application/ld+json")


class ServerErrorTests(SimpleTestCase):
    def test_error_template_is_independent_of_database_and_static_storage(self):
        with patch("wagtail.models.Site.find_for_request", side_effect=OperationalError):
            with patch("django.contrib.staticfiles.storage.staticfiles_storage.url", side_effect=ValueError):
                response = custom_500(RequestFactory().get("/broken/"))
        self.assertContains(response, "Something went wrong.", status_code=500)
        self.assertContains(response, 'content="noindex, nofollow"', status_code=500)
        self.assertNotContains(response, "application/ld+json", status_code=500)

    @override_settings(DEBUG=False, ROOT_URLCONF=__name__)
    def test_django_uses_error_handler_for_uncaught_exceptions(self):
        self.client.raise_request_exception = False
        response = self.client.get("/broken/")
        self.assertContains(response, "Something went wrong.", status_code=500)

    def test_production_urlconf_registers_standalone_error_handler(self):
        self.assertIs(get_resolver("config.urls").resolve_error_handler(500), custom_500)

    @override_settings(DEBUG=False, ROOT_URLCONF=__name__)
    def test_error_response_does_not_expose_exception_details(self):
        self.client.raise_request_exception = False
        response = self.client.get("/broken/")
        self.assertNotContains(response, "Simulated application failure", status_code=500)
        self.assertNotContains(response, "Traceback", status_code=500)
        self.assertContains(response, '<a href="/">Back to homepage</a>', status_code=500, html=True)
