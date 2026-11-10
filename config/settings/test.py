import os

from .base import *

DEBUG = True

# Let reCAPTCHA fields validate with the value "PASSED" during tests.
os.environ["RECAPTCHA_TESTING"] = "True"

SECRET_KEY = "test-secret-key"

ALLOWED_HOSTS = ["*"]


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
