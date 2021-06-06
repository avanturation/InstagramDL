from typing import Any, Optional

from aiohttp.client import ClientSession
from utils import Logger

DEFAULT_HEADER = {
    "Accept-Language": "en-US",
    "Accept-Encoding": "gzip, deflate, br",
    "Host": "www.instagram.com",
    "Origin": "https://www.instagram.com",
    "Referer": "https://www.instagram.com/",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1 Safari/605.1.15",
    "Connection": "keep-alive",
    "X-Requested-With": "XMLHttpRequest",
}

DEFAULT_COOKIE = {
    "sessionid": "",
    "mid": "",
    "ig_pr": "1",
    "ig_vw": "1920",
    "csrftoken": "",
    "s_network": "",
    "ds_user_id": "",
}

ROOT = "https://www.instagram.com"


class BaseReq:
    def __init__(self) -> None:
        self.session: Optional[ClientSession] = None
        self.logger = Logger.generate("Request")

    async def request(
        self,
        url: str,
        method: str,
        **kwargs: Any,
    ):
        if not self.session or self.session.closed:
            self.session = ClientSession()
            self.logger.debug("aiohttp.ClientSession() created.")

        resp = await self.session.request(method, url, **kwargs)

        if resp.status == 200:
            return resp

        else:
            self.logger.debug(f"{url} returned status {resp.status}.")
            self.logger.error("Unexpected Error. Aborting")
            exit()

    async def post(self, url: str, **kwargs: Any):
        if not self.session or self.session.closed:
            self.session = ClientSession()
            self.logger.debug("aiohttp.ClientSession() created.")

        return await self.request(url, "POST", **kwargs)

    async def get(self, url: str, **kwargs: Any):
        if not self.session or self.session.closed:
            self.session = ClientSession()
            self.logger.debug("aiohttp.ClientSession() created.")

        return await self.request(url, "GET", **kwargs)
