"""
Django middleware for managing Correlation ID and Request ID in HTTP requests and responses.

This module provides middleware classes for both synchronous and asynchronous Django applications.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from django_correlation_ids import context
from django_correlation_ids.settings import settings

try:
    from uuid import uuid7  # pyright: ignore[reportAttributeAccessIssue]
except ImportError:
    from uuid_utils.compat import uuid7

if TYPE_CHECKING:
    from typing import Awaitable, Callable

    from django.http import HttpRequest, HttpResponse

    ReqResFunc = Callable[[HttpRequest], HttpResponse]
    AsyncReqResFunc = Callable[[HttpRequest], Awaitable[HttpResponse]]


def CorrelationMiddleware(get_response: ReqResFunc) -> ReqResFunc:
    """
    A Django middleware factory that handles Correlation ID and Request ID for incoming HTTP
    requests and outgoing HTTP responses.
    """

    def middleware(request: HttpRequest) -> HttpResponse:
        _pre(request)
        response = get_response(request)
        _post(response)
        return response

    return middleware


async def AsyncCorrelationMiddleware(
    get_resopnse: AsyncReqResFunc,
) -> AsyncReqResFunc:  # pragma: no cover
    """
    An async Django middleware factory that handles Correlation ID and Request ID for incoming HTTP
    requests and outgoing HTTP responses.
    """

    async def middleware(request: HttpRequest) -> HttpResponse:
        _pre(request)
        response = await get_resopnse(request)
        _post(response)
        return response

    return middleware


def _pre(request: HttpRequest) -> None:
    cid_is_set = False

    if settings.accept_correlation_id and (
        cid_from_req := request.headers.get(settings.correlation_id_header)
    ):
        context._correlation_id.set(cid_from_req)
        cid_is_set = True

    if rid := request.headers.get(settings.request_id_header):
        context._request_id.set(rid)
        if settings.recycle_request_id and not cid_is_set:
            context._correlation_id.set(rid)
            cid_is_set = True

    if not cid_is_set:
        context._correlation_id.set(str(uuid7()))


def _post(response: HttpResponse) -> None:
    if cid := context.get_correlation_id():
        response[settings.correlation_id_header] = cid
    elif settings.allow_response_empty_correlation_id:  # pragma: no cover
        response[settings.correlation_id_header] = ""

    if rid := context.get_request_id():
        response[settings.request_id_header] = rid
    elif settings.allow_response_empty_request_id:  # pragma: no cover
        response[settings.request_id_header] = ""
