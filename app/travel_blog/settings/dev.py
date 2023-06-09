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
