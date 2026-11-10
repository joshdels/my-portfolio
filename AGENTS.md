# Repository Guide

## Purpose

This is Joshua De Leon's career and project portfolio, branded as
Joshdels.

The primary goal is to help Joshua earn an offshore junior GIS role
with an Australian planning, environmental, surveying, civil, or
land-development team. Small, bounded freelance GIS production tasks
are secondary.

Prioritize credible junior positioning, Australian-team relevance,
inspectable project evidence, documented QA, clear limitations,
qualified job or project inquiries, accessibility, performance, and
search discoverability.

## Career positioning

- Default public identity: Philippines-based Junior GIS Practitioner.
- Target junior GIS technician, cartography, spatial-data, and GIS/CAD
  support roles that explicitly accept offshore workers.
- Present WebGIS, automation, and development projects as evidence of
  learning and range, not proof of seniority or independent ownership.
- Prefer careful production, documented checks, questions, and
  reviewer-ready handover over broad end-to-end claims.
- Explain each capability through the task, source material, provided
  procedure, Joshua's actual contribution, checks, outputs, reviewer
  feedback where available, and limitations.
- Describe CAD-to-GIS only as preparation or support unless a project
  proves independent conversion responsibility.
- Describe parcel, tax, masterplan, WebGIS, automation, and software
  projects only where relevant to actual evidence. They are portfolio
  breadth, not the default service campaign.
- Freelance tasks must be bounded, reviewable, and within demonstrated
  ability. Complex systems require separate qualification and scope.
- Use only verified project evidence. Distinguish intended services
  from completed work; do not invent results or promise unsupported
  accuracy, turnaround times, or business outcomes.
- Follow Joshua's freelance positioning prompts supplied in the
  current conversation. Do not assume access to earlier conversations.

## Working boundaries

- Edit only files authorized by the current request. The current scope
  includes niche positioning, SEO, the apps package
  move, the services placeholder, and error templates.
- Preserve the existing architecture and established visual direction.
- The authorized package move preserves model and migration file contents
  and the Django app label `porfolio`.
- Do not modify apps/porfolio/models/ or apps/porfolio/migrations/ unless the
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
- apps/services/: model-free coming-soon services page and future service work
- apps/porfolio/models/: Wagtail page types and supporting data models
- apps/porfolio/views.py: contact form processing and email notifications
- apps/porfolio/forms.py: contact inquiry form
- apps/porfolio/templates/porfolio/: page templates and reusable sections
- apps/porfolio/static/css/: global, component, and section styles
- apps/porfolio/test/: Django tests
- .docker/: container and Compose configuration
- .github/workflows/ci.yml: test, build, and deployment pipeline
- docs/: architecture and installation documentation

## Content and routing

The intended Wagtail page hierarchy is:

HomePage
└── ProjectsIndexPage
    └── Project

Portfolio content is routed through Wagtail.
Services uses /services/ through apps.services (currently coming soon).
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
  source drawings or data, technical decisions, evidence, outcome,
  and client handover. Identify deliverables and limitations clearly.
- Write first for Australian employers and team leads considering a
  junior offshore GIS practitioner, then for clients with small,
  clearly specified GIS production tasks.
- Distinguish source-code findings from verified production behavior.
- Do not promise rankings or treat audit scores as ranking guarantees.

## Development and verification

Local development:
    uv run python manage.py runserver

Tests for authorized implementation work:
    uv run python manage.py test apps.porfolio apps.services --settings=config.settings.test

Read-only template lint:
    uv run djlint apps/porfolio/templates apps/services/templates --lint

Cautions:
- make lint reformats files.
- make migrate generates and applies migrations.
- The Docker default startup command applies migrations.
- Do not run migration commands or migration-triggering startup
  paths while the no-migrations restriction is in force.
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
