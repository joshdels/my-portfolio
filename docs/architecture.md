# Architecture

The portfolio is a Django application using Wagtail as the content management system.

```text
my-portfolio/
├── config/
│   ├── settings/
│   ├── urls.py
│   └── wsgi.py
│
├── porfolio/
│   ├── models/
│   ├── views.py
│   ├── forms.py
│   ├── urls.py
│   ├── templatetags/
│   ├── seo.py
│   ├── templates/
│   └── static/
│
├── docs/
│   ├── installation.md
│   └── architecture.md
│
├── .github/
│   └── workflows/
│       └── ci.yml
│
├── manage.py
└── README.md
```

## Application

**Django** handles application logic, routing, forms, database access, and email.

**Wagtail** manages editable portfolio content such as the homepage and projects.

**PostgreSQL** stores production data. Local development and tests use SQLite.

**Docker** packages and runs the application consistently across development and production.

## Content Flow

```text
Wagtail Admin
      ↓
   Django
      ↓
 PostgreSQL
      ↓
Django Templates
      ↓
  Portfolio
```

## Contact Flow

```text
Visitor
   ↓
Contact Form
   ↓
Django Form
   ↓
ContactInquiry
   ↓
Email Backend
   ↓
Portfolio Email
```

## CI/CD Flow

```text
GitHub
   ↓
Push / Pull Request
   ↓
GitHub Actions
   ↓
Docker Build
   ↓
main
   ↓
SSH Deployment
   ↓
Production Server
   ↓
Docker Compose
```

The production deployment is automated through GitHub Actions and uses Docker Compose to build and restart the application on the server.

## Frontend

`base.html` owns metadata, the main landmark, navigation, and footer. Page templates load their own CSS alongside shared styles. Lora and Inter remain the typography foundation; colors and fonts are defined in `_global.css`.

`components/project_card.html` and `components/cards.css` provide one card implementation for the homepage and project index. Images use responsive Wagtail renditions. Project details show the narrative before the gallery.

Homepage sections use CSS scroll snapping with `proximity`, disabled on mobile and for reduced-motion preferences. A small deferred `navigation.js` updates the sticky navigation palette and current-section indication. It does not intercept scrolling; content and links work without JavaScript.

## Search and sharing

`templatetags/portfolio_tags.py` resolves the site’s project index and builds presentation metadata from existing Wagtail SEO fields. It outputs canonical URLs, social preview data, and safely escaped JSON-LD. No new content fields are needed.

`seo.py` provides robots.txt and the contact sitemap entry. Wagtail’s sitemap implementation supplies live, public CMS pages. Crawl routes precede Wagtail’s catch-all route in `config/urls.py`.

Filtered and searched index URLs use `noindex, follow` and the unfiltered page canonical. Navigation follows the published Projects Index Page URL instead of assuming its slug is `projects`.
