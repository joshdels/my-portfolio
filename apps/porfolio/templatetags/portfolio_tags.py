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
    description = "Joshua De Leon is a GIS practitioner from the Philippines working across mapping, spatial-data preparation, GIS/CAD workflows, automation, and WebGIS. Open to junior opportunities with Australian teams."
    title = "Joshua De Leon | Junior GIS Practitioner"
    if is_index:
        title = "GIS Projects & Work Samples | Joshua De Leon"
        description = "Explore Joshua De Leon's GIS projects, including mapping, spatial-data workflows, automation, and WebGIS."
    elif is_project:
        title = f"{page.title} | Joshua De Leon"
        description = page.description
    elif is_contact:
        title = "Contact | Joshua De Leon, Junior GIS Practitioner"
        description = "Contact Joshua De Leon about junior GIS opportunities with Australian teams, remote collaboration, or a clearly scoped GIS project."
    elif is_services:
        title = "Junior GIS Capabilities | Joshua De Leon"
        description = "How Joshua De Leon approaches spatial-data preparation, GIS analysis, map production, GIS/CAD workflows, and project handover."
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
              "jobTitle": "Junior GIS Practitioner",
              "knowsAbout": ["GIS", "Cartography", "Spatial data preparation", "GIS quality assurance", "CAD to GIS support", "WebGIS", "QGIS", "ArcGIS", "PostGIS", "Python", "Django"],
              "sameAs": ["https://github.com/joshdels", "https://www.linkedin.com/in/joshua-de-leon-8b0310301/"]},
             {"@type": "WebSite", "@id": home_absolute + "#website", "url": home_absolute,
              "name": "Joshua De Leon — Joshdels", "author": {"@id": person_id}},
             {"@type": "ProfilePage" if is_home else "WebPage", "@id": canonical + "#webpage",
              "url": canonical, "name": title, "description": description,
              "isPartOf": {"@id": home_absolute + "#website"},
              "about": {"@id": person_id}}]
    if is_home:
        graph[-1]["mainEntity"] = {"@id": person_id}
    if is_project:
        graph.append({"@type": "CreativeWork", "name": page.title, "url": canonical,
                      "description": description, "image": image_url, "creator": {"@id": person_id}})
    # Escape HTML delimiters before embedding JSON in a script element.
    schema = json.dumps({"@context": "https://schema.org", "@graph": graph}, ensure_ascii=True)
    schema = schema.replace("&", "\\u0026").replace("<", "\\u003c").replace(">", "\\u003e")
    return {"title": title, "description": description, "canonical": canonical,
            "image": image_url, "schema": mark_safe(schema), "home": home,
            "projects_url": projects_url, "is_home": is_home, "is_services": is_services,
            # Index real content; keep previews and filter/search URLs out of search.
            "noindex": bool(getattr(request, "is_preview", False) or request.GET.get("type") or request.GET.get("q") or (not page and not is_contact and not is_services))}
