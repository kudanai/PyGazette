import asyncio
import httpx
from .commons import AUTH_URL, get_query_url, get_detail_url
from .commons import requires_token, parse_response
from .models import *


class Gazette:

    def __init__(self, token=None):
        self._token: str = token

    @property
    def token(self):
        return self._token

    @property
    def _headers(self):
        return {"Authorization": f"Bearer {self.token}"}

    def authorize(self, client_id: str, client_secret: str, auto_set: bool = False) -> AuthResponse:
        """
        Obtain OAuth authorization token for the api using client credentials
        :param client_id: The client_id
        :param client_secret: The client_secret
        :param auto_set: if the returned token should automatically be set for this class instance
        :return: AuthResponse object
        """
        body = {"grant_type": "client_credentials", "client_id": client_id, "client_secret": client_secret}
        response = httpx.post(AUTH_URL, json=body)
        auth: AuthResponse = parse_response(response, AuthResponse)

        if auto_set:
            self._token = auth.access_token

        return auth

    @requires_token(token)
    def fetch_page(self, iulaan_type: Optional[IulaanType] = None, category: Optional[VazeefaType] = None,
                   page: int = 1, extend_details: bool = False) -> List[Iulaan]:
        """
        Query the api for listings
        :param iulaan_type: The Iulaan category to filter
        :param category: Job category for filtering, Only valid for IulaanType.VAZEEFA
        :param page: optional page number to fetch
        :param extend_details: if true, will enrich the listing with a second api call to each iulaans detail page
        :return: List of Iulaan objects
        """
        url = get_query_url(iulaan_type, category, page)
        response = httpx.get(url, headers=self._headers)

        if response.status_code == httpx.codes.OK:
            pg: Page = parse_response(response, Page)

            if extend_details:
                details = asyncio.run(self._fetch_details_async(pg.data))
                pg.data = details

            return pg.data
        else:
            response.raise_for_status()

    @requires_token(token)
    def iter_pages(self, iulaan_type: Optional[IulaanType] = None, category: Optional[VazeefaType] = None,
                   start_page: int = 1, extend_details: bool = False) -> List[Iulaan]:
        """
        recursively yields from fetch_page, while incrementing page numbers.
        """
        yield self.fetch_page(iulaan_type, category, start_page, extend_details)
        yield from self.iter_pages(iulaan_type, category, start_page+1, extend_details)

    @requires_token(token)
    async def _fetch_details_async(self, page_data: List[Iulaan]) -> Iulaan:
        """
        async fetch iulaan details for a list of iulaan
        """
        async def _get_detail(client, iulaan_id) -> Iulaan:
            response = await client.get(get_detail_url(iulaan_id), headers=self._headers)
            return parse_response(response, Iulaan)

        async with httpx.AsyncClient() as client:
            details = await asyncio.gather(*[_get_detail(client, i.iulaan_id) for i in page_data])

        return details

    @requires_token(token)
    def fetch_details(self, iulaan_id: int) -> Iulaan:
        """
        Fetches an individual iulaan item
        :param iulaan_id: iulaan ID to fetch
        :return: Iulaan body
        """
        response = httpx.get(get_detail_url(iulaan_id), headers=self._headers)
        return parse_response(response, Iulaan)
