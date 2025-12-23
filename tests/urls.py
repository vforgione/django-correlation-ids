from logging import getLogger

from django.http import JsonResponse
from django.urls import path
from django_correlation_ids import context


logger = getLogger("tests")


def echo_context(_):
    logger.info("Executing 'echo_context' view")
    return JsonResponse(
        {
            "correlation_id": context.get_correlation_id(),
            "request_id": context.get_request_id(),
        }
    )


urlpatterns = [
    path("echo-context/", echo_context, name="echo_context"),
]
