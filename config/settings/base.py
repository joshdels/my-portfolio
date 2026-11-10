import os
from pathlib import Path

from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent.parent

load_dotenv(BASE_DIR / ".env")

SECRET_KEY = "change-this"

DEBUG = False

ALLOWED_HOSTS = []


INSTALLED_APPS = [
    "apps.porfolio.apps.PorfolioConfig",
    "apps.services.apps.ServicesConfig",
    # Wagtail
    "wagtail",
    "wagtail.admin",
    "wagtail.documents",
    "wagtail.images",
    "wagtail.snippets",
    "wagtail.sites",
    "wagtail.users",
    "wagtail.contrib.forms",
    "wagtail.contrib.redirects",
    # Wagtail dependencies
    "modelcluster",
    "taggit",
    "modelsearch",
    # Django
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.sitemaps",
    "django.contrib.postgres",
    # Third-party
    "storages",
    "django_recaptcha",
]


MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "wagtail.contrib.redirects.middleware.RedirectMiddleware",
]


ROOT_URLCONF = "config.urls"


TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]


WSGI_APPLICATION = "config.wsgi.application"


AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True


STATIC_URL = "static/"
STATIC_ROOT = BASE_DIR / "staticfiles"

MEDIA_URL = "media/"


EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"


WAGTAIL_SITE_NAME = "Joshdels — Geospatial Developer & GIS"


# Google reCAPTCHA v2 ("I'm not a robot" checkbox) on the contact form.
# Set real keys in .env for production; the Google test keys below let local
# development pass without a configured domain.
RECAPTCHA_PUBLIC_KEY = os.environ.get(
    "RECAPTCHA_PUBLIC_KEY", "6LeIxAcTAAAAAJcZVRqyHh71UMIEGNQ_MXjiZKhI"
)
RECAPTCHA_PRIVATE_KEY = os.environ.get(
    "RECAPTCHA_PRIVATE_KEY", "6LeIxAcTAAAAAGG-vFI1TnRWxMZNFuojJ4WifJWe"
)
# Silence the "test keys" warning only while the public (test) key is in use.
if RECAPTCHA_PUBLIC_KEY == "6LeIxAcTAAAAAJcZVRqyHh71UMIEGNQ_MXjiZKhI":
    SILENCED_SYSTEM_CHECKS = ["django_recaptcha.recaptcha_test_key_error"]
