"""
Django signal handlers.

These handlers are responsible for managing the context variables that store the Correlation and
Request IDs.
"""

from __future__ import annotations

from django.core.signals import request_finished, setting_changed
from django.dispatch import receiver

from django_correlation_ids import context


@receiver(setting_changed)
def reload_settings(*, setting: str, **_) -> None:
    """
    Reloads django_correlation_ids settings when they are changed.
    """
    if setting == "DJANGO_CORRELATION_IDS":
        from django_correlation_ids.settings import settings

        settings._load()


@receiver(request_finished)
def reset_contextvars(**_) -> None:
    """
    Resets the context variables that store the Correlation and Request IDs.
    """
    context._correlation_id.set("")
    context._request_id.set("")
