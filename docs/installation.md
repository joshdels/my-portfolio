# Installation

## Requirements

- Python 3.14+
- uv
- PostgreSQL (production; local development uses SQLite)
- Git
- Docker (optional)

## Local Development

Clone the repository:

```bash
git clone <repository-url>
cd my-portfolio
```

Install the locked dependencies (uv creates `.venv`):

```bash
uv sync --locked
```

Create the environment configuration:

```bash
cp .env.example .env
```

Configure the database and other required settings in `.env`.

For a new installation, initialize the database using existing migrations:

```bash
uv run python manage.py migrate
```

Create a Wagtail administrator:

```bash
uv run python manage.py createsuperuser
```

Start the development server:

```bash
uv run python manage.py runserver
```

Open the portfolio at:

```text
http://127.0.0.1:8000/
```

Wagtail admin:

```text
http://127.0.0.1:8000/admin/
```

## Wagtail Setup

After logging into Wagtail:

1. Create the **Home Page**.
2. Set it as the site root under **Settings → Sites**.
3. Set the correct hostname and port: local development uses `localhost:8000`; production HTTPS uses your public hostname and port `443`. These settings determine canonical and sitemap URLs.
4. Create a **Projects Index Page** beneath the Home Page.
5. Create **Project** pages beneath the Projects Index Page, then publish the pages.

Hero, about, and footer copy lives in templates. Project content and page SEO fields live in Wagtail.

## Projects

Create projects through the Wagtail admin.

For each project, add the available project information such as:

- Title
- Description
- Project image
- Tools / technologies
- Project links
- Project types, project date, and Selected status

Publish the project when complete. Mark up to three strong projects as selected for a focused homepage; the homepage displays the first three selected projects by publication order. All selected projects remain visible in the project index.

Use the existing SEO title and search description fields in Wagtail’s Promote tab. See [SEO and publishing](seo.md).

## Docker

The production application can be built and started with:

```bash
docker compose -f .docker/docker-compose.yml up -d --build
```

GitHub Actions automatically builds the Docker image and deploys the `main` branch to the production server.

## Checks

```bash
uv run python manage.py check
uv run python manage.py test apps.porfolio apps.services --settings=config.settings.test
uv run djlint apps/porfolio/templates apps/services/templates --lint
```

Enable the version-controlled pre-push checks once after cloning:

```bash
make install-hooks
```

Every push will then run `make verify`'s Django checks and full test suite. A
failure cancels the push; no bypass is performed automatically.

`make lint` reformats templates. `make migrate` generates and applies migrations;
neither is a read-only check. Production migrations run as an explicit
deployment step before the new web container starts.
