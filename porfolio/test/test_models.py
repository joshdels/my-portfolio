from django.test import TestCase

from porfolio.models import (
    ContactInquiry,
    Project,
    ProjectLink,
    ProjectQuote,
    ProjectsIndexPage,
    ProjectType,
    ProjectVideo,
    Tool,
)


class ContactInquiryModelTests(TestCase):
    def test_contact_inquiry_creation(self):
        inquiry = ContactInquiry.objects.create(
            name="Test User",
            email="test@example.com",
            industry="other",
            inquiry="Testing the contact inquiry model.",
        )

        self.assertIsNotNone(inquiry.pk)
        self.assertEqual(inquiry.name, "Test User")
        self.assertEqual(inquiry.email, "test@example.com")
        self.assertEqual(inquiry.industry, "other")
        self.assertEqual(str(inquiry), "Test User — other")


class ProjectTypeTests(TestCase):
    def test_project_type_creation(self):
        project_type = ProjectType.objects.create(
            name="GIS Development",
        )

        self.assertEqual(project_type.name, "GIS Development")
        self.assertEqual(str(project_type), "GIS Development")


class ToolTests(TestCase):
    def test_tool_creation(self):
        tool = Tool.objects.create(
            name="Django",
        )

        self.assertEqual(tool.name, "Django")
        self.assertEqual(str(tool), "Django")


class ProjectsIndexPageTests(TestCase):
    def test_projects_index_page_creation(self):
        root_page = ProjectsIndexPage.get_first_root_node()

        index_page = ProjectsIndexPage(
            title="Projects",
            slug="projects",
        )

        root_page.add_child(instance=index_page)

        self.assertIsNotNone(index_page.pk)
        self.assertEqual(index_page.title, "Projects")
        self.assertEqual(str(index_page), "Projects")


class ProjectTests(TestCase):
    def setUp(self):
        root_page = ProjectsIndexPage.get_first_root_node()

        self.projects_index = ProjectsIndexPage(
            title="Projects",
            slug="projects",
        )

        root_page.add_child(instance=self.projects_index)

    def test_project_creation(self):
        project = Project(
            title="Test GIS Project",
            slug="test-gis-project",
            description="A test GIS project.",
            client="Test Client",
            location="Davao",
            selected=False,
        )

        self.projects_index.add_child(instance=project)

        self.assertIsNotNone(project.pk)
        self.assertEqual(str(project), "Test GIS Project")
        self.assertEqual(project.title, "Test GIS Project")
        self.assertEqual(project.client, "Test Client")
        self.assertEqual(project.location, "Davao")
        self.assertFalse(project.selected)


class ProjectRelatedModelTests(TestCase):
    def test_project_video_string(self):
        video = ProjectVideo(
            title="Project Demo",
            url="https://example.com/video",
        )

        self.assertEqual(str(video), "Project Demo")

    def test_project_video_uses_url_when_title_is_empty(self):
        video = ProjectVideo(
            title="",
            url="https://example.com/video",
        )

        self.assertEqual(
            str(video),
            "https://example.com/video",
        )

    def test_project_link_string(self):
        link = ProjectLink(
            title="Project Website",
            url="https://example.com",
        )

        self.assertEqual(str(link), "Project Website")

    def test_project_quote_string(self):
        quote = ProjectQuote(
            quote="A test quote.",
            author="Test Author",
        )

        self.assertEqual(str(quote), "Test Author")
