from .base import *

DEBUG = True

# Exercise Turnstile form handling without contacting Cloudflare.
TURNSTILE_ENABLED = True
TURNSTILE_TESTING = True
TURNSTILE_SITE_KEY = "test-site-key"
TURNSTILE_SECRET_KEY = "test-secret-key"

SECRET_KEY = "test-secret-key"

ALLOWED_HOSTS = ["*"]
WAGTAILADMIN_BASE_URL = "http://testserver"


DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "test.sqlite3",
    }
}


EMAIL_BACKEND = "django.core.mail.backends.locmem.EmailBackend"


STORAGES = {
    "default": {
        "BACKEND": "django.core.files.storage.FileSystemStorage",
    },
    "staticfiles": {
        "BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage",
    },
}


STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
