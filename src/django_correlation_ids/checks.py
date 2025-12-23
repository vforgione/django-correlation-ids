"""
Django system checks for django_correlation_ids.

Ensures that the correlation middleware is installed in the Django settings.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from django.conf import settings
from django.core.checks import Error, register

if TYPE_CHECKING:
    from typing import Iterator

    from django.core.checks import CheckMessage


@register
def check_middleware(*_, **__) -> Iterator[CheckMessage]:
    syncmw = "django_correlation_ids.middleware.CorrelationMiddleware"
    asyncmw = "django_correlation_ids.middleware.AsyncCorrelationMiddleware"

    if syncmw not in settings.MIDDLEWARE and asyncmw not in settings.MIDDLEWARE:
        yield Error(
            msg="Correlation middleware is not installed",
            hint=f'Add either "{syncmw}" or "{asyncmw}" to MIDDLEWARE in settings.py',
            code="django_correlation_ids.E0001",
        )
