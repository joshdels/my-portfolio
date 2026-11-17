import os

from botocore.config import Config

from .base import *

B2_ENDPOINT_URL = os.environ["B2_ENDPOINT_URL"].rstrip("/")
B2_BUCKET_NAME = os.environ["B2_BUCKET_NAME"]
B2_CUSTOM_DOMAIN = (
    f"{B2_ENDPOINT_URL.removeprefix('https://').removeprefix('http://')}"
    f"/{B2_BUCKET_NAME}"
)

SECRET_KEY = os.environ["SECRET_KEY"]

DEBUG = False

ALLOWED_HOSTS = [
    host.strip() for host in os.environ["ALLOWED_HOSTS"].split(",") if host.strip()
]

CSRF_TRUSTED_ORIGINS = [
    origin.strip()
    for origin in os.environ.get("CSRF_TRUSTED_ORIGINS", "").split(",")
    if origin.strip()
]


CSRF_COOKIE_SECURE = True

SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

SECURE_SSL_REDIRECT = True

SESSION_COOKIE_SECURE = True
SESSION_COOKIE_HTTPONLY = True

SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True

USE_X_FORWARDED_HOST = True


DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.environ["POSTGRES_DB"],
        "USER": os.environ["POSTGRES_USER"],
        "PASSWORD": os.environ["POSTGRES_PASSWORD"],
        "HOST": os.environ["POSTGRES_HOST"],
        "PORT": os.environ.get("POSTGRES_PORT", "5432"),
        "CONN_MAX_AGE": int(os.environ.get("POSTGRES_CONN_MAX_AGE", "60")),
        "CONN_HEALTH_CHECKS": True,
        "OPTIONS": {
            "connect_timeout": int(os.environ.get("POSTGRES_CONNECT_TIMEOUT", "5")),
        },
    }
}


CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
        "LOCATION": "joshdels-public-pages",
        "TIMEOUT": 300,
        "OPTIONS": {"MAX_ENTRIES": 500},
    }
}

# Public Wagtail pages are cached per worker. This short TTL bounds stale
# rendered HTML after publishing without adding another infrastructure service.
PUBLIC_PAGE_CACHE_SECONDS = int(os.environ.get("PUBLIC_PAGE_CACHE_SECONDS", "300"))


STORAGES = {
    "default": {
        "BACKEND": "storages.backends.s3.S3Storage",
        "OPTIONS": {
            "access_key": os.environ["B2_APPLICATION_KEY_ID"],
            "secret_key": os.environ["B2_APPLICATION_KEY"],
            "bucket_name": B2_BUCKET_NAME,
            "endpoint_url": B2_ENDPOINT_URL,
            "region_name": os.environ["B2_REGION"],
            "addressing_style": "path",
            # Avoid initializing boto3 merely to render a public media URL.
            "custom_domain": B2_CUSTOM_DOMAIN,
            "url_protocol": "https:",
            "default_acl": None,
            "querystring_auth": False,
            "location": "media",
            "client_config": Config(
                connect_timeout=3,
                read_timeout=10,
                retries={"max_attempts": 2, "mode": "standard"},
                max_pool_connections=20,
            ),
        },
    },
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
}


STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"

MEDIA_URL = f"https://{B2_CUSTOM_DOMAIN}/media/"

EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"

EMAIL_HOST = os.environ["BREVO_HOST"]
EMAIL_PORT = int(os.environ.get("BREVO_PORT", "587"))

EMAIL_USE_TLS = True
EMAIL_TIMEOUT = int(os.environ.get("EMAIL_TIMEOUT", "10"))

EMAIL_HOST_USER = os.environ["BREVO_SMTP_LOGIN"]
EMAIL_HOST_PASSWORD = os.environ["BREVO_SMTP_PASSWORD"]

DEFAULT_FROM_EMAIL = os.environ["WEBSITE_EMAIL"]
SERVER_EMAIL = os.environ["WEBSITE_EMAIL"]

WAGTAILADMIN_BASE_URL = os.environ["WAGTAILADMIN_BASE_URL"]

# Do not let an unavailable CAPTCHA provider occupy a web worker for long.
RECAPTCHA_VERIFY_REQUEST_TIMEOUT = int(
    os.environ.get("RECAPTCHA_VERIFY_REQUEST_TIMEOUT", "5")
)
