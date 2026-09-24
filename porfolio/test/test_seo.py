import json
import re

from django.test import TestCase
from wagtail.models import Page, Site

from porfolio.models import HomePage, Project, ProjectsIndexPage


class PortfolioSEOTests(TestCase):
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
        self.assertContains(response, "Joshua De Leon | Geospatial Developer")
        self.assertContains(response, 'href="/work/"')
        self.assertContains(response, 'href="/#about"')
        self.assertContains(response, 'class="home-scroll"')
        html = response.content.decode()
        self.assertEqual(len(re.findall(r"<h1(?:\s|>)", html)), 1)
        self.assertEqual(len(re.findall(r"<main(?:\s|>)", html)), 1)
        schema = json.loads(re.search(r'<script type="application/ld\+json">(.*?)</script>', html).group(1))
        self.assertEqual(schema["@graph"][0]["name"], "Joshua De Leon")
        self.assertNotIn('name="robots" content="noindex', html)

    def test_project_uses_editor_seo_fields(self):
        response = self.client.get("/work/spatial-pipeline/")
        self.assertContains(response, '<title>Spatial pipeline | Joshua De Leon</title>', html=True)
        self.assertContains(response, 'content="A Python spatial data workflow for infrastructure."')
        self.assertContains(response, 'href="http://testserver/work/spatial-pipeline/"')
        self.assertNotContains(response, "css/sections/hero.css")

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
