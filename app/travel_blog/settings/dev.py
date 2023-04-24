# flake8: noqa

from .base import *

DEBUG = bool(int(os.environ.get("DEBUG", 0)))

ALLOWED_HOSTS = []

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        "NAME": os.environ.get("DB_NAME"),
        "USER": os.environ.get("DB_USER"),
        "PASSWORD": os.environ.get("DB_PASS"),
        "HOST": os.environ.get("DB_HOST"),
        "PORT": os.environ.get("DB_PORT"),
    }
}


STATIC_URL = "static/"


MEDIA_URL = "media/"
MEDIA_ROOT = BASE_DIR.child("media")

EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"

EMAIL_HOST = "smtp-relay.sendinblue.com"

EMAIL_PORT = 587

EMAIL_USE_TLS = True

EMAIL_HOST_USER = "e.bobbiesi@gmail.com"

EMAIL_HOST_PASSWORD = "xsmtpsib-3a77f7de60ea089068d526a1082954277b73418498ffb1690a4c0e8b369db95b-3SfcVALvr5jFqk4d"
