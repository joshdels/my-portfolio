"""Presentation metadata and site navigation; no changes to content models."""
import json
from urllib.parse import urljoin

from django import template
from django.templatetags.static import static
from django.urls import reverse
from django.utils.html import strip_tags
from django.utils.safestring import mark_safe
from wagtail.models import Site

from apps.porfolio.models import HomePage, Project, ProjectsIndexPage

register = template.Library()


@register.simple_tag(takes_context=True)
def portfolio_meta(context):
    request = context["request"]
    page = context.get("page")
    site = Site.find_for_request(request)
    origin = site.root_url if site else request.build_absolute_uri("/").rstrip("/")
    home = site.root_page.get_url(request) if site else "/"
    home = home or "/"
    index = (ProjectsIndexPage.objects.descendant_of(site.root_page).live().public().first()
             if site else None)
    projects_url = index.get_url(request) if index else None
    is_home = isinstance(page, HomePage)
    is_project = isinstance(page, Project)
    is_index = isinstance(page, ProjectsIndexPage)
    is_contact = request.path == reverse("contact")
    is_services = request.path == reverse("services:index")
    description = "Joshua De Leon is a GIS developer in the Philippines who helps firms and teams bring their spatial data into one organised system that handles large datasets and gives people maps and tools they can use. Pursuing remote GIS Developer and Geospatial Developer roles."
    title = "Joshua De Leon | GIS Developer & Geospatial Developer"
    if is_index:
        title = "GIS Development & Spatial Systems | Joshua De Leon"
        description = "Explore Joshua De Leon's GIS development work: large parcel datasets, automated map preparation, spatial databases, and browser based mapping tools that help a team work from one system."
    elif is_project:
        title = f"{page.title} | Joshua De Leon"
        description = page.description
    elif is_contact:
        title = "Contact Joshua De Leon | GIS Developer"
        description = "Contact Joshua De Leon in Davao, Philippines (UTC+8) about a remote GIS Developer role, geospatial development, or a clearly scoped GIS project."
    elif is_services:
        title = "GIS Development & Services | Joshua De Leon"
        description = "How Joshua De Leon helps a team work from one spatial system: large datasets, automated map work, databases, and browser based mapping tools."
    elif not is_home:
        title = "Page not found | Joshua De Leon"
        description = "This page could not be found. Explore Joshua De Leon's geospatial and GIS projects or get in touch about geospatial roles and projects."
    if page:
        title = page.seo_title or title
        description = page.search_description or description
    description = " ".join(strip_tags(description).split())
    canonical = (page.get_full_url(request) if page else None) or urljoin(origin + "/", request.path)
    image_url = urljoin(origin + "/", static("assets/joshua.png"))
    if is_project:
        first_image = page.project_images.select_related("image").first()
        if first_image:
            image_url = urljoin(origin + "/", first_image.image.get_rendition("fill-1200x630").url)
    home_absolute = urljoin(origin + "/", home)
    person_id = home_absolute + "#person"
    graph = [{"@type": "Person", "@id": person_id, "name": "Joshua De Leon",
              "alternateName": "Joshdels", "url": home_absolute,
              "jobTitle": "GIS Developer and Geospatial Developer",
              "description": "GIS developer in Davao, Philippines who helps firms and teams bring their spatial data into one system. Pursuing remote GIS Developer and Geospatial Developer roles compatible with UTC+8.",
              "homeLocation": {"@type": "Place", "name": "Davao, Philippines",
                               "address": {"@type": "PostalAddress", "addressLocality": "Davao",
                                           "addressCountry": "PH"}},
              "knowsAbout": ["GIS development", "Geospatial development", "Spatial data systems", "Large spatial datasets", "Parcel data", "Remote sensing", "Cartography", "GIS/CAD workflows", "Spatial databases", "Web mapping", "QGIS", "ArcGIS", "PostGIS", "Python", "Django"],
              "sameAs": ["https://github.com/joshdels", "https://www.linkedin.com/in/joshua-de-leon-8b0310301/"]},
             {"@type": "WebSite", "@id": home_absolute + "#website", "url": home_absolute,
              "name": "Joshua De Leon — Joshdels", "inLanguage": "en",
              "author": {"@id": person_id}},
             {"@type": ("ProfilePage" if is_home else
                         "CollectionPage" if is_index else "WebPage"),
              "@id": canonical + "#webpage",
              "url": canonical, "name": title, "description": description,
              "inLanguage": "en",
              "isPartOf": {"@id": home_absolute + "#website"},
              "about": {"@id": person_id}}]
    if is_home:
        graph[-1]["mainEntity"] = {"@id": person_id}
    if is_index:
        listed_projects = [
            *context.get("selected_projects", []),
            *context.get("projects", []),
        ]
        item_list_id = canonical + "#projects"
        items = []
        for position, project in enumerate(listed_projects, start=1):
            project_url = project.get_full_url(request)
            project_item = {"@type": "CreativeWork", "@id": project_url + "#project",
                            "url": project_url, "name": project.title,
                            "description": project.description,
                            "creator": {"@id": person_id}}
            if project.date:
                project_item["dateCreated"] = project.date.isoformat()
            items.append({"@type": "ListItem", "position": position,
                          "item": project_item})
        graph[-1]["mainEntity"] = {"@id": item_list_id}
        graph.append({"@type": "ItemList", "@id": item_list_id,
                      "name": "Joshua De Leon's GIS and geospatial projects",
                      "numberOfItems": len(items), "itemListElement": items})
    if is_project:
        work_id = canonical + "#project"
        work = {"@type": "CreativeWork", "@id": work_id, "name": page.title,
                "url": canonical, "description": description, "image": image_url,
                "creator": {"@id": person_id}}
        if page.date:
            work["dateCreated"] = page.date.isoformat()
        project_types = list(page.project_types.values_list("name", flat=True))
        tools = list(page.tools.values_list("name", flat=True))
        if project_types:
            work["genre"] = project_types
        if tools:
            work["keywords"] = tools
        if page.location:
            work["spatialCoverage"] = page.location
        graph[-1]["mainEntity"] = {"@id": work_id}
        graph.append(work)
    # Escape HTML delimiters before embedding JSON in a script element.
    schema = json.dumps({"@context": "https://schema.org", "@graph": graph}, ensure_ascii=True)
    schema = schema.replace("&", "\\u0026").replace("<", "\\u003c").replace(">", "\\u003e")
    return {"title": title, "description": description, "canonical": canonical,
            "image": image_url, "schema": mark_safe(schema), "home": home,
            "projects_url": projects_url, "is_home": is_home, "is_services": is_services,
            # Index real content; keep previews and filter/search URLs out of search.
            "noindex": bool(getattr(request, "is_preview", False) or request.GET.get("type") or request.GET.get("q") or (not page and not is_contact and not is_services))}
