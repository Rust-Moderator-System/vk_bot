from typing import Any, TypeVar, Union, get_origin

import aiohttp
from pydantic import parse_obj_as

from utils.http.client import HTTPClient

RT = TypeVar('RT')


class APIClient:
    def __init__(self, base_url: str | None = None, authorization_token: str | None = None) -> None:
        self.http_client = HTTPClient(base_url=base_url, authorization_token=authorization_token)

    async def get(
        self,
        url: str,
        query: dict | None = None,
        response_model: type[RT] | None = None,
    ) -> RT:
        response = await self.http_client.request_get(url, query=query)
        return await self._parse_response(response, response_model)

    async def post(
        self,
        url: str,
        query: str | None = None,
        payload: dict | None = None,
        body: str | None = None,
        response_model: RT | None = None,
        **kwargs: Any,
    ) -> RT:
        response = await self.http_client.request_post(url, query=query, payload=payload, body=body, **kwargs)
        return await self._parse_response(response, response_model)

    async def put(
        self,
        url: str,
        query: dict | None = None,
        payload: dict | None = None,
        body: str | None = None,
        response_model: RT | None = None,
    ) -> RT:
        response = await self.http_client.requets_put(url, query=query, payload=payload, body=body)
        return await self._parse_response(response, response_model)

    async def delete(
        self,
        url: str,
        query: dict | None = None,
        response_model: RT | None = None,
    ) -> RT:
        response = await self.http_client.request_delete(url, query=query)
        return await self._parse_response(response, response_model)

    async def _parse_response(
        self,
        response: aiohttp.ClientResponse,
        response_model: RT | None = None,
    ) -> Union[RT, list[RT], None]:
        if response_model is None:
            return
        elif response_model is dict:
            return await response.json()

        response_json = await response.json()
        if response_json:
            return parse_obj_as(response_model, response_json)

        if issubclass(get_origin(response_model), list):
            return []
        return None
