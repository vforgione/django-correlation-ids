from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent


SECRET_KEY = "django-insecure-l#ju)*2%_n=2s3mx_2ehrir-f*o-_k$7e^vwu7u@qd&jicmc8z"

DEBUG = True

INSTALLED_APPS = [
    "django_correlation_ids",
]

MIDDLEWARE = [
    "django_correlation_ids.middleware.CorrelationMiddleware",
]

ROOT_URLCONF = "tests.urls"

WSGI_APPLICATION = "tests.wsgi.application"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

DJANGO_CORRELATION_IDS = {
    "correlation_id_header": "X-Correlation-Id",
    "request_id_header": "X-Request-Id",
    "allow_empty_correlation_id_header": True,
    "allow_empty_request_id_header": True,
    "recycle_request_id_header": True,
    "log_request_id": True,
}

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "filters": {
        "correlation": {
            "()": "django_correlation_ids.logging.CorrelationFilter",
        },
    },
    "formatters": {
        "correlation": {
            "format": "{asctime} {levelname} {name}: {message} ::: correlation_id='{correlation_id}' request_id='{request_id}'",
            "style": "{",
            "datefmt": "%Y-%m-%dT%H:%M:%S%z",
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "filters": ["correlation"],
            "formatter": "correlation",
        },
    },
    "loggers": {
        "tests": {
            "handlers": ["console"],
            "propagate": True,
            "level": "DEBUG",
        },
        "django": {
            "handlers": ["console"],
            "propagate": True,
            "level": "INFO",
        },
    },
}
