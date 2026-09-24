# My Portfolio

Joshua De Leon’s geospatial developer portfolio, built with Django and Wagtail to showcase spatial data systems, GIS automation, and WebGIS projects.


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

```bash
uv sync --locked
# First-time database setup only:
uv run python manage.py migrate
uv run python manage.py createsuperuser
uv run python manage.py runserver
```

Wagtail admin:

```text
http://127.0.0.1:8000/admin/
```

Local development uses SQLite; production uses PostgreSQL. See the installation guide for environment and Wagtail site setup.

Run the test suite:

```bash
uv run python manage.py test porfolio --settings=config.settings.test
```
