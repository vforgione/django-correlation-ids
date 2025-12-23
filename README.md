# Django Correlation IDs

Django Correlation IDs adds Correlation IDs into your log records to enhace their traceability, especially for distributed systems.

Each request is assigned a unique identifier--its Correlation ID. As the request is processed by your project, each Django subsystem and your apps' loggers have the ability to produce log messages that include this identifier:

```
2025-12-01T16:25:34 12345678-1234-1234-1234-123456789abc INFO: handling POST /foo/
2025-12-01T16:25:34 87654321-4321-4321-4321-fed987654321 INFO: handling GET /bar/
2025-12-01T16:25:34 87654321-4321-4321-4321-fed987654321 DEBUG: executing query "SELECT ..." with params (...)
2025-12-01T16:25:35 12345678-1234-1234-1234-123456789abc WARNING: found condition in payload data
2025-12-01T16:25:35 87654321-4321-4321-4321-fed987654321 INFO: responding 200 to GET /bar/
2025-12-01T16:25:36 12345678-1234-1234-1234-123456789abc DEBUG: executing query "SELECT ..." with params (...)
2025-12-01T16:25:36 12345678-1234-1234-1234-123456789abc DEBUG: executing query "INSERT ..." with params (...)
2025-12-01T16:25:36 12345678-1234-1234-1234-123456789abc INFO: reponding 201 to POST /foo/
```

## Installation

Django Correlation IDs can be installed from PyPI:

```shell
uv add django-correlation-ids
```

Then, add the app to the list of installed apps in your project's _settings.py_ file:

```python
INSTALLED_APPS = [
    # ... other apps
    "django_correlation_ids",
]
```

Next, add the appropriate middleware to your project's middleware list in _settings.py_:

```python
MIDDLEWARE = [
    # ... other middleware
    "django_correlation_ids.middleware.CorrelationMiddleware",
    # or if your project is running on ASGI:
    # "django_correlation_ids.middleware.AsyncCorrelationMiddleware"
]
```

## Settings

Django Correlation IDs does not require any additional settings to be used by your project. It does have optional settings that can be configured in your project's _settings.py_ file.

The default settings for Django Correlation IDs are:

```python
DJANGO_CORRELATION_IDS = {
    # Name of the HTTP header for responses. Will also be used as the name of
    # the HTTP header for requests when 'accept_correlation_id' is True.
    "correlation_id_header": "X-Correlation-Id",
    
    # Name of the HTTP header for requests and responses.
    "request_id_header": "X-Request-Id",
    
    # If a request has a Correlation ID header, should that value be used as
    # the Correlation ID by this software? This can be useful if your app is
    # part of a collection of APIs; e.g. a microservice architecture.
    "accept_correlation_id": True,
    
    # If the request has a Request ID header, should that value be used as
    # the Correlation ID by this software?
    "recycle_request_id": False,
    
    # If, for whatever reason, the Correlation ID is empty when returning a
    # response, should an empty header value be allowed to be sent?
    "allow_response_empty_correlation_id": False,
    
    # If the Request ID is empty when returning a response, should an empty
    # header value be allowed to be sent?
    "allow_response_empty_request_id": False,
}
```

## Usage

The main interface of Django Correlation IDs is via logging. This software provides a custom logging filter object that will add the current request's Correlation ID, and optionally the Request ID, to log records.

```python
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
            "format": "{asctime} {correlation_id} {levelname}: {message}",
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
        "your_app": {
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
```

Django Correlation IDs also provides a simple interface to access the current Correlation and Request IDs:

```python
>>> from django_correlation_ids import context
>>> context.get_correlation_id()
"some-correlation-id-string"
>>> context.get_request_id()
"some-request-id-string"
```
