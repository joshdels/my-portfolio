from .base import *

DEBUG = True

# Let reCAPTCHA fields validate with the value "PASSED" during tests.
RECAPTCHA_TESTING = True
# base.py loads .env, so force the documented Google test keys here instead of
# allowing local production keys to make unit tests contact Google's API.
RECAPTCHA_PUBLIC_KEY = "6LeIxAcTAAAAAJcZVRqyHh71UMIEGNQ_MXjiZKhI"
RECAPTCHA_PRIVATE_KEY = "6LeIxAcTAAAAAGG-vFI1TnRWxMZNFuojJ4WifJWe"

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
