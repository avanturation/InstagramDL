import asyncio
import random
from datetime import datetime
from http.cookies import SimpleCookie

from .request import DEFAULT_COOKIE, DEFAULT_HEADER, ROOT, BaseReq


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
            self.logger.info("Two-Factor authentication requireed.")
            code = input("Enter your two factor code: ")

            payload = {
                "username": user,
                "verificationCode": f"{code}",
                "identifier": f"{ajax_resp['two_factor_info']['two_factor_identifier']}",
            }

            ajax_resp = await self.post(
                ROOT + "/accounts/login/ajax/two_factor/",
                data=payload,
                allow_redirects=True,
                headers=self.headers,
            )

        if "checkpoint_url" in data:
            self.logger.error(
                "Instagram needs your confirmation. Follow the instructions and try again. Aborting"
            )
            exit()

        if data["status"] != "ok" or "authenticated" not in data:
            self.logger.error("Unexpected Error. Maybe your IP is blocked. Aborting")
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
