from sys import argv

from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
ALLOWED_HOSTS = ["localhost"]

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

TESTING = "test" in argv
if not TESTING:
    ALLOWED_HOSTS += ["127.0.0.1"]
    INTERNAL_IPS = ["127.0.0.1"]
    INSTALLED_APPS += ["debug_toolbar"]
    MIDDLEWARE = [
        "debug_toolbar.middleware.DebugToolbarMiddleware"
    ] + MIDDLEWARE
