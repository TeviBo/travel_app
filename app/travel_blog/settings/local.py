from .base import * # noqa

DEBUG = True

ALLOWED_HOSTS = []

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql_psycopg2", # noqa
        "NAME": os.environ.get("DB_NAME"), # noqa
        "USER": os.environ.get("DB_USER"), # noqa
        "PASSWORD": os.environ.get("DB_PASS"), # noqa
        "HOST": os.environ.get("DB_HOST"), # noqa
        "PORT": os.environ.get("DB_PORT"), # noqa
    }
}


STATIC_URL = "static/"


MEDIA_URL = "media/"
MEDIA_ROOT = BASE_DIR.child("media") # noqa
