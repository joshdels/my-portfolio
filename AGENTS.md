# Repository Guide

## Purpose

This is Joshua De Leon's personal geospatial developer portfolio,
branded as Joshdels.

The site showcases GIS automation, spatial data systems, and WebGIS
work, with an emphasis on energy, land, and infrastructure.

Prioritize employer understanding, clear project evidence,
accessibility, performance, and search discoverability.

## Working boundaries

- Preserve the existing architecture and established visual direction.
- Do not modify porfolio/models/ or porfolio/migrations/ unless the
  user explicitly lifts that restriction.
- Do not generate or apply migrations under the current restriction.
- For analysis-only requests, return findings and proposed changes
  without editing files.
- Preserve existing user changes.
- Do not rename the porfolio package to correct its spelling.
- Never invent project outcomes, credentials, clients, or testimonials.
- Do not expose .env contents or credentials.

## Stack

- Python 3.14+
- Django and Wagtail
- Django templates and plain CSS
- PostgreSQL for production
- SQLite in test settings
- uv for dependency management
- Gunicorn and WhiteNoise
- S3-compatible Backblaze B2 media storage
- Docker Compose and GitHub Actions

Use pyproject.toml and uv.lock as dependency sources of truth.

## Repository layout

- config/settings/base.py: shared application settings
- config/settings/local.py: local settings
- config/settings/prod.py: production settings
- config/settings/test.py: isolated test configuration
- config/urls.py: admin, contact routing, and Wagtail routing
- porfolio/models/: Wagtail page types and supporting data models
- porfolio/views.py: contact form processing and email notifications
- porfolio/forms.py: contact inquiry form
- porfolio/templates/porfolio/: page templates and reusable sections
- porfolio/static/css/: global, component, and section styles
- porfolio/test/: Django tests
- .docker/: container and Compose configuration
- .github/workflows/ci.yml: test, build, and deployment pipeline
- docs/: architecture and installation documentation

## Content and routing

The intended Wagtail page hierarchy is:

HomePage
└── ProjectsIndexPage
    └── Project

Public content is routed through Wagtail.
Contact uses /guest/contact/.
Wagtail admin uses /admin/.
Django admin uses /django-admin/.

Project data supports descriptions, dates, clients, locations,
tools, categories, images, videos, links, and testimonials.

Homepage selected work currently uses publication ordering.
The project index uses manually entered project dates.

Hero, about, navigation, and footer content is largely maintained
in templates. Do not assume it is editable through Wagtail.

## Frontend conventions

- Keep server-rendered HTML and the existing CSS approach.
- Reuse project-card markup and styles where practical.
- Scope navigation and page-specific selectors.
- Preserve responsive behavior.
- Use semantic landmarks and a clear heading hierarchy.
- Provide visible keyboard focus and reduced-motion support.
- Use responsive Wagtail image renditions and reserve image space.
- Lazy-load below-the-fold images, not critical initial images.
- Prefer resolved CMS URLs over hardcoded page paths.

## SEO and editorial conventions

- Use accurate, page-specific titles and descriptions.
- Use existing Wagtail SEO fields before proposing new fields.
- Keep Joshua De Leon and Joshdels branding consistent.
- Use absolute canonical URLs for the production site.
- Keep public sitemaps aligned with published, public content.
- Define an intentional policy for filter and search URLs.
- Include useful social-sharing metadata.
- Write project case studies around the problem, contribution,
  technical decisions, evidence, and outcome.
- Distinguish source-code findings from verified production behavior.
- Do not promise rankings or treat audit scores as ranking guarantees.

## Development and verification

Local development:
    uv run python manage.py runserver

Tests for authorized implementation work:
    uv run python manage.py test porfolio --settings=config.settings.test

Read-only template lint:
    uv run djlint porfolio/templates --lint

Cautions:
- make lint reformats files.
- make migrate generates and applies migrations.
- The Docker default startup command applies migrations.
- Do not use those mutation paths during an analysis-only review.

For frontend changes, verify desktop and mobile layouts,
keyboard navigation, empty states, and long project content.

For functional changes, test the relevant behavior and failures.
Report what was tested and what remains unverified.

## Deployment

GitHub Actions tests and builds pull requests and main pushes.
Pushes to main also trigger production deployment.

Treat a push to main as deployment-affecting.
Do not deploy unless authorized.