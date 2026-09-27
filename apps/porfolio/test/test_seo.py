import json
import re
from tempfile import TemporaryDirectory
from xml.etree import ElementTree

from django.conf import settings
from django.contrib.staticfiles.storage import staticfiles_storage
from django.core.cache import cache
from django.core.management import call_command
from django.test import RequestFactory, TestCase
from wagtail.models import Page, PageViewRestriction, Site

from apps.porfolio.models import HomePage, Project, ProjectsIndexPage


class PortfolioSEOTests(TestCase):
    def setUp(self):
        # Wagtail caches site roots outside database transaction rollbacks.
        cache.clear()
        self.addCleanup(cache.clear)

    @classmethod
    def setUpTestData(cls):
        root = Page.get_first_root_node()
        cls.home = root.add_child(instance=HomePage(title="Home", slug="portfolio-home"))
        cls.index = cls.home.add_child(instance=ProjectsIndexPage(title="Projects", slug="work"))
        cls.project = cls.index.add_child(instance=Project(
            title="Spatial pipeline", slug="spatial-pipeline", description="A GIS automation workflow.",
            selected=True, seo_title="Spatial pipeline | Joshua De Leon",
            search_description="A Python spatial data workflow for infrastructure.",
        ))
        cls.draft = cls.index.add_child(instance=Project(
            title="Unpublished", slug="unpublished", description="Draft", live=False,
        ))
        site = Site.objects.get(is_default_site=True)
        site.root_page = cls.home
        site.hostname = "testserver"
        site.port = 80
        site.save()

    def test_home_metadata_and_semantics(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "CAD-to-GIS &amp; Masterplan WebGIS | Joshdels")
        self.assertContains(response, "CAD to GIS. Masterplans to interactive WebGIS.")
        self.assertContains(response, 'href="/services/"')
        self.assertNotIn("energy", response.content.decode().lower())
        self.assertContains(response, 'href="/work/"')
        self.assertContains(response, 'href="/#about"')
        self.assertContains(response, 'class="home-scroll"')
        html = response.content.decode()
        self.assertEqual(len(re.findall(r"<h1(?:\s|>)", html)), 1)
        self.assertEqual(len(re.findall(r"<main(?:\s|>)", html)), 1)
        schema = json.loads(re.search(r'<script type="application/ld\+json">(.*?)</script>', html).group(1))
        self.assertEqual(schema["@graph"][0]["name"], "Joshua De Leon")
        self.assertIn("CAD-to-GIS conversion", schema["@graph"][0]["knowsAbout"])
        self.assertNotIn('name="robots" content="noindex', html)

    def test_project_uses_editor_seo_fields(self):
        response = self.client.get("/work/spatial-pipeline/")
        self.assertContains(response, '<title>Spatial pipeline | Joshua De Leon</title>', html=True)
        self.assertContains(response, 'content="A Python spatial data workflow for infrastructure."')
        self.assertContains(response, 'href="http://testserver/work/spatial-pipeline/"')
        self.assertNotContains(response, "css/sections/hero.css")

    def test_public_pages_with_production_static_manifest(self):
        # Collect real assets so deleted or renamed files cannot be hidden by
        # the permissive static storage used by the rest of the test suite.
        storages = {
            **settings.STORAGES,
            "staticfiles": {
                "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
            },
        }
        with TemporaryDirectory() as static_root:
            with self.settings(DEBUG=False, STATIC_ROOT=static_root, STORAGES=storages):
                call_command("collectstatic", interactive=False, verbosity=0)
                portrait_url = staticfiles_storage.url("assets/joshua.png")
                self.assertRegex(portrait_url, r"/assets/joshua\.[0-9a-f]+\.png$")
                with self.assertRaisesMessage(ValueError, "Missing staticfiles manifest entry"):
                    staticfiles_storage.url("assets/nonexistent-regression-check.png")

                for path, status in (
                    ("/", 200),
                    ("/work/", 200),
                    ("/work/?q=GIS", 200),
                    ("/work/spatial-pipeline/", 200),
                    ("/guest/contact/", 200),
                    ("/services/", 200),
                    ("/missing/", 404),
                ):
                    with self.subTest(path=path):
                        response = self.client.get(path)
                        self.assertContains(
                            response,
                            f'content="http://testserver{portrait_url}"',
                            status_code=status,
                        )
                        self.assertNotContains(response, "joshua.jpeg", status_code=status)

    def test_filtered_index_is_not_indexable(self):
        response = self.client.get("/work/?q=GIS")
        self.assertContains(response, 'content="noindex, follow"')
        self.assertContains(response, 'href="http://testserver/work/"')
        self.assertNotContains(response, 'application/ld+json')

    def test_structured_data_cannot_close_script(self):
        self.project.seo_title = '</script><script>alert("x")</script>'
        self.project.save()
        response = self.client.get("/work/spatial-pipeline/")
        html = response.content.decode()
        payload = re.search(r'<script type="application/ld\+json">(.*?)</script>', html).group(1)
        self.assertNotIn("<", payload)
        self.assertEqual(json.loads(payload)["@graph"][2]["name"], self.project.seo_title)

    def test_sitemap_excludes_unpublished_and_includes_contact(self):
        response = self.client.get("/sitemap.xml")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "/work/spatial-pipeline/")
        self.assertContains(response, "/guest/contact/")
        self.assertNotContains(response, "unpublished")

    def test_robots_and_404(self):
        response = self.client.get("/robots.txt")
        self.assertContains(response, "Sitemap: http://testserver/sitemap.xml")
        with self.settings(DEBUG=False):
            response = self.client.get("/missing/")
        self.assertEqual(response.status_code, 404)
        self.assertContains(response, 'content="noindex, follow"', status_code=404)

    def test_home_and_index_editor_metadata_overrides_niche_defaults(self):
        for page, path in ((self.home, "/"), (self.index, "/work/")):
            with self.subTest(path=path):
                page.seo_title = "Drawing conversion & parcel maps | Joshdels"
                page.search_description = "A client-approved description of drawing deliverables."
                page.save()
                response = self.client.get(path)
                self.assertContains(response, "<title>Drawing conversion &amp; parcel maps | Joshdels</title>", html=True)
                self.assertContains(response, f'<meta name="description" content="{page.search_description}">', html=True)
                self.assertContains(response, f'<meta property="og:description" content="{page.search_description}">', html=True)
                self.assertContains(response, f'<meta name="twitter:description" content="{page.search_description}">', html=True)

    def test_project_without_editor_metadata_uses_its_own_evidence(self):
        self.project.seo_title = ""
        self.project.search_description = ""
        self.project.description = "A documented spatial workflow for a planning team."
        self.project.save()
        response = self.client.get("/work/spatial-pipeline/")
        self.assertContains(response, "<title>Spatial pipeline | Joshua De Leon</title>", html=True)
        self.assertContains(response, f'<meta name="description" content="{self.project.description}">', html=True)
        schema = json.loads(re.search(
            r'<script type="application/ld\+json">(.*?)</script>', response.content.decode(),
        ).group(1))
        work = next(item for item in schema["@graph"] if item["@type"] == "CreativeWork")
        self.assertEqual(work["description"], self.project.description)

    def test_https_canonicals_social_urls_and_sitemap_match_site(self):
        site = Site.objects.get(is_default_site=True)
        site.port = 443
        site.save()
        for path in ("/", "/work/", "/work/spatial-pipeline/", "/guest/contact/", "/services/"):
            with self.subTest(path=path):
                response = self.client.get(path, secure=True)
                expected = f"https://testserver{path}"
                self.assertContains(response, f'<link rel="canonical" href="{expected}">', html=True)
                self.assertContains(response, f'<meta property="og:url" content="{expected}">', html=True)
        sitemap = self.client.get("/sitemap.xml", secure=True)
        locations = ElementTree.fromstring(sitemap.content).findall(
            "{http://www.sitemaps.org/schemas/sitemap/0.9}url/{http://www.sitemaps.org/schemas/sitemap/0.9}loc"
        )
        self.assertTrue(locations)
        self.assertTrue(all(item.text.startswith("https://testserver/") for item in locations))
        self.assertContains(self.client.get("/robots.txt", secure=True), "Sitemap: https://testserver/sitemap.xml")

    def test_category_filter_is_noindex_with_clean_canonical(self):
        response = self.client.get("/work/?type=999999")
        self.assertContains(response, 'content="noindex, follow"')
        self.assertContains(response, '<link rel="canonical" href="http://testserver/work/">', html=True)
        self.assertNotContains(response, "application/ld+json")
        self.assertContains(response, "No projects found.")
        self.assertContains(response, '<a href="/work/">browse all projects</a>', html=True)

    def test_preview_is_noindex_and_omits_structured_data(self):
        request = RequestFactory().get("/")
        request.is_preview = True
        response = self.home.serve_preview(request, self.home.default_preview_mode)
        response.render()
        self.assertContains(response, 'content="noindex, follow"')
        self.assertNotContains(response, "application/ld+json")

    def test_private_project_is_excluded_from_public_discovery(self):
        PageViewRestriction.objects.create(
            page=self.project, restriction_type="password", password="test-only-password",
        )
        self.assertNotContains(self.client.get("/sitemap.xml"), "/work/spatial-pipeline/")
        for path in ("/", "/work/"):
            with self.subTest(path=path):
                self.assertNotContains(self.client.get(path), 'href="/work/spatial-pipeline/"')

    def test_unpublished_index_is_not_linked_in_navigation(self):
        self.index.live = False
        self.index.save()
        response = self.client.get("/")
        self.assertNotContains(response, 'href="/work/"')
        self.assertContains(response, 'href="/services/"')
        self.assertContains(response, 'href="/guest/contact/"')

    def test_contact_metadata_is_indexable_and_niche_specific(self):
        response = self.client.get("/guest/contact/")
        self.assertContains(response, "<title>Contact for CAD-to-GIS &amp; WebGIS | Joshdels</title>", html=True)
        self.assertContains(response, 'href="http://testserver/guest/contact/"')
        self.assertNotContains(response, 'content="noindex, follow"')
        self.assertContains(response, "application/ld+json")
        self.assertNotIn("energy", response.content.decode().lower())
