"""
Application configuration for django_correlation_ids.

On ready, it imports checks and signals to ensure they are registered.
"""

from __future__ import annotations

from django.apps import AppConfig


class DjangoCorrelationIdsConfig(AppConfig):
    label = "django_correlation_ids"
    name = "django_correlation_ids"

    def ready(self) -> None:
        import django_correlation_ids.checks  # noqa: F401
        import django_correlation_ids.signals  # noqa: F401
