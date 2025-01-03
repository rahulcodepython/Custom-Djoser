from .settings import *
import os

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ["*"]

# Database
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

# CORS Configuration
CORS_ALLOWED_ORIGINS = []
CORS_ALLOW_ALL_ORIGINS = True

SEND_LOGIN_CONFIRMATION_EMAIL = not DEBUG

OTP_VERIFICATION_LOGIN = not DEBUG
