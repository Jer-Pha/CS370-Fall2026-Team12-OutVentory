from decouple import config

from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False
ALLOWED_HOSTS = [s.strip() for s in config("ALLOWED_HOSTS").split(",")]

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "NAME": config("SQL_NAME"),
        "HOST": config("SQL_HOST"),
        "PORT": "3306",
        "USER": config("SQL_USER"),
        "PASSWORD": config("SQL_PASSWORD"),
        "CONN_MAX_AGE": 300,
        "CONN_HEALTH_CHECKS": True,
        "OPTIONS": {
            "init_command": "SET sql_mode='STRICT_TRANS_TABLES'",
            "charset": "utf8mb4",
        },
    },
}

ADMINS = []
MANAGERS = []
