from .settings import *
from decouple import config

DEBUG = False

if not SECRET_KEY or SECRET_KEY.startswith("django-insecure-") or len(SECRET_KEY) < 50:
    raise ValueError("A long, random SECRET_KEY must be set in production")

if not FIELD_ENCRYPTION_KEY:
    raise ValueError("FIELD_ENCRYPTION_KEY must be set in production")

ALLOWED_HOSTS = config("ALLOWED_HOSTS", default="").split(",")
if not ALLOWED_HOSTS or ALLOWED_HOSTS == [""]:
    raise ValueError("ALLOWED_HOSTS must be set in production")

# Configure a production database (e.g., PostgreSQL)
_db_password = config("DB_PASSWORD", default="")
if not _db_password:
    raise ValueError(
        "DB_PASSWORD environment variable must be set in production. "
        "Using default passwords is insecure and not allowed."
    )
DATABASES = {
    "default": {
        "ENGINE": config("DB_ENGINE", default="django.db.backends.postgresql"),
        "NAME": config("DB_NAME", default="remedium_hms"),
        "USER": config("DB_USER", default="remedium_user"),
        "PASSWORD": _db_password,
        "HOST": config("DB_HOST", default="localhost"),
        "PORT": config("DB_PORT", default="5432"),
    }
}

# Security settings
X_FRAME_OPTIONS = "DENY"
SECURE_HSTS_SECONDS = config(
    "SECURE_HSTS_SECONDS", default=300, cast=int
)  # Start with 5 min, increase gradually
SECURE_HSTS_INCLUDE_SUBDOMAINS = config(
    "SECURE_HSTS_INCLUDE_SUBDOMAINS", default=True, cast=bool
)
SECURE_HSTS_PRELOAD = config("SECURE_HSTS_PRELOAD", default=True, cast=bool)
SECURE_SSL_REDIRECT = config("SECURE_SSL_REDIRECT", default=True, cast=bool)
SESSION_COOKIE_SECURE = config("SESSION_COOKIE_SECURE", default=True, cast=bool)
CSRF_COOKIE_SECURE = config("CSRF_COOKIE_SECURE", default=True, cast=bool)
SECURE_CONTENT_TYPE_NOSNIFF = True
REFERRER_POLICY = "same-origin"
SESSION_COOKIE_HTTPONLY = True
CSRF_COOKIE_HTTPONLY = True
SESSION_COOKIE_SAMESITE = "Lax"
CSRF_COOKIE_SAMESITE = "Lax"
# Note: SECURE_BROWSER_XSS_FILTER and SECURE_CONTENT_TYPE_NOSNIFF are deprecated in Django 4.0+

# Proxy SSL header - required when behind nginx/Cloudflare/reverse proxy
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

# Static files (collectstatic)
STATIC_ROOT = BASE_DIR / "staticfiles"

# Logging
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "file": {
            "class": "logging.handlers.RotatingFileHandler",
            "filename": BASE_DIR / "logs" / "production.log",
            "maxBytes": 1024 * 1024 * 5,  # 5 MB
            "backupCount": 5,
            "formatter": "verbose",
        },
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "simple",
        },
    },
    "formatters": {
        "verbose": {
            "format": "{levelname} {asctime} {module} {process:d} {thread:d} {message}",
            "style": "{",
        },
        "simple": {
            "format": "{levelname} {message}",
            "style": "{",
        },
    },
    "root": {
        "handlers": ["file", "console"],
        "level": "INFO",
    },
    "loggers": {
        "django": {
            "handlers": ["file", "console"],
            "level": "INFO",
            "propagate": False,
        },
    },
}

# Email settings (example for SendGrid)
# EMAIL_BACKEND = 'sendgrig_backend.SendgridBackend'
# SENDGRID_API_KEY = os.environ.get('SENDGRID_API_KEY')
# DEFAULT_FROM_EMAIL = 'your_email@example.com'

# Production Cache (Redis) - Uses REDIS_URL environment variable
CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": config("REDIS_URL", default="redis://localhost:6379/1"),
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        },
    }
}

# Session backend with Redis
SESSION_ENGINE = "django.contrib.sessions.backends.cached_db"
