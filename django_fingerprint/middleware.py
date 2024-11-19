from __future__ import annotations

import json
from collections.abc import Awaitable
from typing import Any
from typing import Callable
from urllib.parse import unquote
from urllib.parse import urlsplit
from urllib.parse import urlunsplit

from asgiref.sync import iscoroutinefunction
from asgiref.sync import markcoroutinefunction
from django.http import HttpRequest
from django.http.response import HttpResponseBase
from django.utils.functional import cached_property


class FingerprintMiddleware:
    sync_capable = True
    async_capable = True

    def __init__(
        self,
        get_response: (
            Callable[[HttpRequest], HttpResponseBase]
            | Callable[[HttpRequest], Awaitable[HttpResponseBase]]
        ),
    ) -> None:
        self.get_response = get_response
        self.async_mode = iscoroutinefunction(self.get_response)

        if self.async_mode:
            # Mark the class as async-capable, but do the actual switch
            # inside __call__ to avoid swapping out dunder methods
            markcoroutinefunction(self)

    def __call__(
        self, request: HttpRequest
    ) -> HttpResponseBase | Awaitable[HttpResponseBase]:
        if self.async_mode:
            return self.__acall__(request)
        fpid = request.GET.get("fpid")
        # print(request.headers)
        # print(request.META)
        print(fpid)
        request.fpid = fpid
        request.session["fpid"] = fpid
        # request.fpid = fpid  # type: ignore [attr-defined]
        return self.get_response(request)

    async def __acall__(self, request: HttpRequest) -> HttpResponseBase:
        request.htmx = HtmxDetails(request)  # type: ignore [attr-defined]
        return await self.get_response(request)  # type: ignore [no-any-return, misc]
