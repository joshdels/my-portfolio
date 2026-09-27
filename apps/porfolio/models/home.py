from wagtail.admin.panels import FieldPanel
from wagtail.fields import RichTextField
from wagtail.models import Page

from .projects import Project


class HomePage(Page):
    intro = RichTextField(blank=True)

    template = "porfolio/home_page.html"

    content_panels = Page.content_panels + [
        FieldPanel("intro"),
    ]

    subpage_types = [
        "porfolio.ProjectsIndexPage",
    ]

    class Meta:
        verbose_name = "Home Page"
        verbose_name_plural = "Home Pages"

    def get_context(self, request):
        context = super().get_context(request)

        context["selected_projects"] = (
            Project.objects.live()
            .public()
            .filter(selected=True)
            .order_by("-first_published_at")
        )

        return context
