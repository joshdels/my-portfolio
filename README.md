# Joshdels — Junior GIS Practitioner Portfolio

Joshua De Leon's GIS career and project portfolio, built with Django and Wagtail. The site positions Joshua as a Philippines-based junior GIS practitioner seeking offshore roles with Australian planning, environmental, surveying, civil, and land-development teams. Small, bounded freelance production tasks are secondary.

## Career direction

The focus is careful, reviewable GIS production: cartography, spatial-data preparation, basic documented analysis, GIS/CAD support, QA, and clear handover. Portfolio projects may demonstrate WebGIS and automation, but public copy must not imply seniority, independent Australian professional judgment, or unsupported production outcomes.

| Junior capability | Evidence expected |
| --- | --- | --- |
| Map production | Readable layouts, source and projection notes, and review-ready files |
| Spatial-data preparation | Organized layers, basic attribute/geometry checks, counts, and change notes |
| Basic spatial analysis | Reproducible buffer, overlay, and area workflows with stated assumptions |
| GIS/CAD support | Preserved inputs, confirmed CRS/units, documented preparation and exceptions |
| WebGIS and automation learning | Working demonstrations with code, tests or QA, README, and honest limits |

Employment is the primary path. Freelance work is limited to demonstrated, bounded tasks with written inputs, reviewer, checks, payment, and handover. Never imply legal boundary certification, surveying, planning approval, valuation, or regulatory advice.

Case studies should show the task, data source, Joshua's actual contribution, method, QA, output, reviewer feedback where available, and limitations.

Site copy and default metadata follow this direction. Existing Wagtail content and editor-supplied SEO fields remain unchanged and should be reviewed before publishing. `/services/` is a coming-soon page for future freelance offerings.

![Background](public/image.png)


## Stack

* Django
* Wagtail
* PostgreSQL
* HTML / CSS / JavaScript
* Docker

## Features

* Wagtail-managed pages and project content
* Project portfolio and project history
* Contact inquiry form with email notifications
* Services coming-soon page at `/services/`, linked from navigation
* Standalone 500 error page that does not depend on the database
* Responsive frontend with section color themes and shared project cards
* Page-specific SEO, social previews, structured data, and XML sitemap
* Dockerized deployment
* Automated CI/CD with GitHub Actions

## CI/CD

The project uses GitHub Actions for automated builds and deployment.

### Build

Every push and pull request targeting `main` runs the Django tests in Docker, then builds the application image.

### Deploy

Every push to `main` triggers deployment to the production server through SSH.

The deployment:

1. Updates the server repository to the latest `main`.
2. Builds the Docker image.
3. Starts the application with Docker Compose.
4. Removes unused Docker images.

The pipeline is located in:

```text
.github/
└── workflows/
    └── ci.yml
```

## Documentation

* [Installation](docs/installation.md)
* [Architecture](docs/architecture.md)
* [SEO and publishing](docs/seo.md)

## Development

Current working restrictions: do not generate or apply migrations, and do not modify `apps/porfolio/models/` or `apps/porfolio/migrations/`. The portfolio lives in `apps/porfolio`; the future services area lives in `apps/services`.

For an already configured local database:

```bash
uv sync --locked
uv run python manage.py runserver
```

If database setup requires migrations, stop until that restriction is explicitly lifted. Avoid `make migrate` and the default Docker startup path, which also apply migrations.

Wagtail admin:

```text
http://127.0.0.1:8000/admin/
```

Local development uses SQLite; production uses PostgreSQL. See the installation guide for environment and Wagtail site setup.

Run the test suite:

```bash
uv run python manage.py test apps.porfolio apps.services --settings=config.settings.test
```
