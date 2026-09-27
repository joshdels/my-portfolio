from django.test import RequestFactory, TestCase
from wagtail.models import Site

from apps.porfolio.models import HomePage, Project, ProjectsIndexPage, ProjectType


class HomePageTests(TestCase):
    def setUp(self):
        self.root_page = Site.objects.get(is_default_site=True).root_page

        self.home_page = HomePage(
            title="Home",
        )

        self.root_page.add_child(instance=self.home_page)

    def test_home_page_creation(self):
        self.assertEqual(self.home_page.title, "Home")

    def test_home_page_context(self):
        project = Project(
            title="Selected GIS Project",
            description="Test project",
            selected=True,
        )

        self.home_page.add_child(instance=project)
        project.save_revision().publish()

        request = RequestFactory().get("/")

        context = self.home_page.get_context(request)

        self.assertIn("selected_projects", context)
        self.assertEqual(
            context["selected_projects"].count(),
            1,
        )


class ProjectsIndexPageTests(TestCase):
    def setUp(self):
        self.root_page = Site.objects.get(is_default_site=True).root_page

        self.index_page = ProjectsIndexPage(
            title="Projects",
        )

        self.root_page.add_child(instance=self.index_page)

    def test_projects_index_page_creation(self):
        self.assertEqual(self.index_page.title, "Projects")

    def test_projects_index_page_context(self):
        request = RequestFactory().get("/projects/")

        context = self.index_page.get_context(request)

        self.assertIn("selected_projects", context)
        self.assertIn("projects", context)
        self.assertIn("project_types", context)
        self.assertIn("active_type", context)

        self.assertIsNone(context["active_type"])

    def test_project_type_filter(self):
        project_type = ProjectType.objects.create(
            name="GIS Development",
        )

        project = Project(
            title="GIS Project",
            description="Test GIS project",
            selected=False,
        )

        self.index_page.add_child(instance=project)
        project.save_revision().publish()

        ProjectType.objects.get(pk=project_type.pk)

        request = RequestFactory().get(f"/projects/?type={project_type.pk}")

        context = self.index_page.get_context(request)

        self.assertEqual(
            context["active_type"],
            str(project_type.pk),
        )
