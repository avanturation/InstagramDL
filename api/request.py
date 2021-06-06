import asyncio
import random
from datetime import datetime
from http.cookies import SimpleCookie
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
        if not self.session:
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
        if not self.session:
            self.session = ClientSession()
            self.logger.debug("aiohttp.ClientSession() created.")

        return await self.request(url, "POST", **kwargs)

    async def get(self, url: str, **kwargs: Any):
        if not self.session:
            self.session = ClientSession()
            self.logger.debug("aiohttp.ClientSession() created.")

        return await self.request(url, "GET", **kwargs)


class Authenticator(BaseReq):
    def __init__(self) -> None:
        self.headers = DEFAULT_HEADER
        self.cookies = DEFAULT_COOKIE
        super().__init__()

    async def get_csfr(self):
        self.logger.debug("Tricking IG in order to get fake CSRF token.")
        login_resp = await self.get(ROOT + "/accounts/login/", headers=self.headers)

        self.headers["X-CSRFToken"] = login_resp.cookies["csrftoken"].value
        self.headers["Referer"] = "https://www.instagram.com/accounts/login/"

        self.logger.debug("Got CSRF Token: " + login_resp.cookies["csrftoken"].value)

        return login_resp.cookies["csrftoken"].value

    async def ajax(self, user: str, passwd: str):
        self.logger.info("Logging into Instagram..")
        self.logger.debug(f"ID: {user}, PASSWORD: {passwd}")

        payload = {
            "username": user,
            "enc_password": f"#PWD_INSTAGRAM_BROWSER:0:{int(datetime.now().timestamp())}:{passwd}",
            "queryParams": "{}",
            "optIntoOneTap": "false",
        }

        ajax_resp = await self.post(
            ROOT + "/accounts/login/ajax/",
            data=payload,
            allow_redirects=True,
            headers=self.headers,
        )

        self.logger.debug("/accounts/login/ajax returned status 200.")
        data = await ajax_resp.json(encoding="utf-8")

        if "two_factor_required" in data:
            self.logger.error("Two-Factor authentication requireed. Aborting")
            exit()

        if "checkpoint_url" in data:
            self.logger.error("Instagram needs your confirmation. Aborting")
            exit()

        if data["status"] != "ok" or "authenticated" not in data:
            self.logger.error("Unexpected Error. Aborting")
            exit()

        if not data["authenticated"]:
            self.logger.error("Wrong password or id. Aborting")
            exit()

        self.logger.info("Authentication Successful!")
        return ajax_resp.cookies

    def convert_dict(self, cookie: SimpleCookie):
        _cookies = DEFAULT_COOKIE

        for key, morsel in cookie.items():
            _cookies[key] = morsel.value

        return _cookies

    async def login(self, user: str, passwd: str):
        try:
            csrf_token = await self.get_csfr()

            self.logger.info(
                "Sleeping for a few seconds to avoid Instagram from blocking your IP."
            )
            await asyncio.sleep(min(random.expovariate(0.6), 15.0))
            final_cookies = await self.ajax(user, passwd)

            return self.convert_dict(final_cookies)

        finally:
            await self.session.close()


class GraphQL(BaseReq):
    def __init__(self, cookies) -> None:
        self.headers = DEFAULT_HEADER
        self.cookies = cookies
        super().__init__()
