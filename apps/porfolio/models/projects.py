from django.db import models
from django.db.models import F, Q

from modelcluster.fields import ParentalKey

from wagtail.admin.panels import (
    FieldPanel,
    InlinePanel,
    MultipleChooserPanel,
)

from wagtail.fields import RichTextField
from wagtail.models import Orderable, Page
from wagtail.snippets.models import register_snippet


@register_snippet
class ProjectType(models.Model):
    name = models.CharField(
        max_length=100,
        unique=True,
    )

    class Meta:
        ordering = ["name"]
        verbose_name = "Project Type"
        verbose_name_plural = "Project Types"

    def __str__(self):
        return self.name


@register_snippet
class Tool(models.Model):
    name = models.CharField(
        max_length=100,
        unique=True,
    )

    class Meta:
        ordering = ["name"]
        verbose_name = "Tool"
        verbose_name_plural = "Tools"

    def __str__(self):
        return self.name


class ProjectsIndexPage(Page):
    intro = RichTextField(
        blank=True,
    )

    content_panels = Page.content_panels + [
        FieldPanel("intro"),
    ]

    subpage_types = [
        "porfolio.Project",
    ]

    class Meta:
        verbose_name = "Projects Index Page"
        verbose_name_plural = "Projects Index Pages"

    def get_context(self, request):
        context = super().get_context(request)

        project_type = request.GET.get("type")
        search_query = request.GET.get("q", "").strip()

        # Base project queryset
        projects = (
            Project.objects.child_of(self)
            .live()
            .public()
            .order_by(F("date").desc(nulls_last=True))
        )

        # Filter by project type
        if project_type:
            projects = projects.filter(
                project_type_items__project_type__id=project_type
            ).distinct()

        # Search projects
        if search_query:
            projects = projects.filter(
                Q(title__icontains=search_query)
                | Q(description__icontains=search_query)
                | Q(client__icontains=search_query)
                | Q(location__icontains=search_query)
                | Q(project_type_items__project_type__name__icontains=search_query)
                | Q(tool_items__tool__name__icontains=search_query)
            ).distinct()

        # Selected Works
        # Still controlled by selected=True
        # and ordered by the manually entered project date.
        context["selected_projects"] = projects.filter(selected=True)

        # All other projects
        context["projects"] = projects.filter(selected=False)

        # Project filters
        context["project_types"] = ProjectType.objects.all()
        context["tools"] = Tool.objects.all()

        # Current filters
        context["active_type"] = project_type
        context["search_query"] = search_query

        return context


class ProjectProjectType(Orderable):
    project = ParentalKey(
        "Project",
        on_delete=models.CASCADE,
        related_name="project_type_items",
    )

    project_type = models.ForeignKey(
        ProjectType,
        on_delete=models.CASCADE,
        related_name="+",
    )

    panels = [
        FieldPanel("project_type"),
    ]

    def __str__(self):
        return str(self.project_type)


class ProjectTool(Orderable):
    project = ParentalKey(
        "Project",
        on_delete=models.CASCADE,
        related_name="tool_items",
    )

    tool = models.ForeignKey(
        Tool,
        on_delete=models.CASCADE,
        related_name="+",
    )

    panels = [
        FieldPanel("tool"),
    ]

    def __str__(self):
        return str(self.tool)


class Project(Page):
    description = models.TextField(
        help_text="Short description shown on project cards.",
    )

    client = models.CharField(
        max_length=200,
        blank=True,
    )

    location = models.CharField(
        max_length=200,
        blank=True,
    )

    # Manually entered project date.
    # This controls chronological ordering.
    date = models.DateField(
        null=True,
        blank=True,
    )

    content = RichTextField(
        blank=True,
    )

    # Controls whether the project appears
    # in the Selected Works section.
    selected = models.BooleanField(
        default=False,
        help_text="Include this project in the selected work section.",
    )

    content_panels = Page.content_panels + [
        FieldPanel("description"),
        MultipleChooserPanel(
            "project_type_items",
            label="Project Types",
            chooser_field_name="project_type",
        ),
        MultipleChooserPanel(
            "tool_items",
            label="Tools",
            chooser_field_name="tool",
        ),
        FieldPanel("client"),
        FieldPanel("location"),
        FieldPanel("date"),
        FieldPanel("content"),
        FieldPanel("selected"),
        InlinePanel(
            "project_images",
            label="Images",
            heading="Project Images",
        ),
        InlinePanel(
            "videos",
            label="Videos",
            heading="Project Videos",
        ),
        InlinePanel(
            "links",
            label="Links",
            heading="Project Links",
        ),
        InlinePanel(
            "quotes",
            label="Quotes",
            heading="Project Quotes",
        ),
    ]

    parent_page_types = [
        "porfolio.ProjectsIndexPage",
    ]

    class Meta:
        verbose_name = "Project"
        verbose_name_plural = "Projects"

        # Newest manually entered date first.
        ordering = [
            "-date",
        ]

    def __str__(self):
        return self.title

    @property
    def project_types(self):
        return ProjectType.objects.filter(
            pk__in=self.project_type_items.values_list(
                "project_type_id",
                flat=True,
            )
        ).order_by("name")

    @property
    def tools(self):
        return Tool.objects.filter(
            pk__in=self.tool_items.values_list(
                "tool_id",
                flat=True,
            )
        ).order_by("name")


class ProjectImage(Orderable):
    project = ParentalKey(
        Project,
        on_delete=models.CASCADE,
        related_name="project_images",
    )

    image = models.ForeignKey(
        "wagtailimages.Image",
        on_delete=models.CASCADE,
        related_name="+",
    )

    caption = models.CharField(
        max_length=255,
        blank=True,
    )

    panels = [
        FieldPanel("image"),
        FieldPanel("caption"),
    ]

    def __str__(self):
        return self.caption or self.image.title


class ProjectVideo(Orderable):
    project = ParentalKey(
        Project,
        on_delete=models.CASCADE,
        related_name="videos",
    )

    title = models.CharField(
        max_length=200,
        blank=True,
    )

    url = models.URLField()

    panels = [
        FieldPanel("title"),
        FieldPanel("url"),
    ]

    def __str__(self):
        return self.title or self.url


class ProjectLink(Orderable):
    project = ParentalKey(
        Project,
        on_delete=models.CASCADE,
        related_name="links",
    )

    title = models.CharField(
        max_length=100,
    )

    url = models.URLField()

    panels = [
        FieldPanel("title"),
        FieldPanel("url"),
    ]

    def __str__(self):
        return self.title


class ProjectQuote(Orderable):
    project = ParentalKey(
        Project,
        on_delete=models.CASCADE,
        related_name="quotes",
    )

    quote = models.TextField()

    author = models.CharField(
        max_length=200,
        blank=True,
    )

    role = models.CharField(
        max_length=200,
        blank=True,
    )

    panels = [
        FieldPanel("quote"),
        FieldPanel("author"),
        FieldPanel("role"),
    ]

    def __str__(self):
        return self.author or "Project Quote"
