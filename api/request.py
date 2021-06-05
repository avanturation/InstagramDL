import aiohttp

from datetime import datetime
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


class Requester:
    def __init__(self) -> None:
        self.header = DEFAULT_HEADER
        self.cookie = DEFAULT_COOKIE
        self.logger = Logger.generate("Request")

    async def login(self, user: str, passwd: str):
        async with aiohttp.ClientSession(headers=self.header) as trick_session:
            self.logger.debug("Tricking IG in order to get fake CSRF token.")
            async with trick_session.get(ROOT + "/accounts/login/") as response:
                self.header["X-CSRFToken"] = response.cookies["csrftoken"].value
                self.header["Referer"] = "https://www.instagram.com/accounts/login/"
                self.logger.debug(
                    "Got CSRF Token: " + response.cookies["csrftoken"].value
                )
                await trick_session.close()

        async with aiohttp.ClientSession(headers=self.header) as login:
            self.logger.info("Logging into Instagram..")
            self.logger.debug(f"ID: {user}, PASSWORD: {passwd}")
            async with login.request(
                method="POST",
                url="https://www.instagram.com/accounts/login/ajax/",
                data={
                    "username": user,
                    "enc_password": f"#PWD_INSTAGRAM_BROWSER:0:{int(datetime.now().timestamp())}:{passwd}",
                    "queryParams": "{}",
                    "optIntoOneTap": "false",
                },
                allow_redirects=True,
            ) as response:
                if response.status == 200:
                    self.logger.debug("/accounts/login/ajax returned status 200.")
                    data = await response.json(encoding="utf-8")

                    if "two_factor_required" in data:
                        self.logger.error(
                            "Two-Factor authentication requireed. Aborting"
                        )
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
                    return response.cookies

                else:
                    self.logger.debug(
                        f"/account/login/ajax returned status {response.status}."
                    )
                    self.logger.error("Unexpected Error. Aborting")
                    exit()
