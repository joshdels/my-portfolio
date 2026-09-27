# Joshdels — CAD-to-GIS and WebGIS Services

Joshua De Leon's freelance geospatial services portfolio, built with Django and Wagtail. The site is being repositioned around CAD-to-GIS conversion, parcel and tax mapping, and masterplan drawings delivered as interactive WebGIS with client handover.

## Service direction

The focus is helping clients turn existing drawings and land records into usable spatial data and maps. Each engagement should define the source materials, required checks, deliverables, and handover scope.

| Service | Source material | Intended deliverables, subject to scope |
| --- | --- | --- |
| CAD-to-GIS conversion | Client-provided CAD drawings and coordinate reference information | Organized GIS layers, attributes, and documented conversion checks |
| Parcel and tax mapping | Parcel geometry, parcel identifiers, and client-provided tax records | Linked parcel layers, mapped records, and documented data gaps |
| Masterplan to interactive WebGIS | Masterplan drawings and supporting spatial data | Interactive map layers, agreed inspection tools, and client handover documentation |

Handover should specify the data files, application source where agreed, deployment arrangements, ownership and access, usage instructions, and any ongoing support. Parcel and tax mapping concerns spatial data organization; it does not imply legal boundary certification, property valuation, or tax advice.

These are positioning priorities, not claims of completed projects. Case studies should show verified source material, Joshua's contribution, technical decisions, delivered outputs, and outcomes. GIS automation and spatial data systems support these services.

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
