from typing import Optional

from api import Authenticator
from utils import Logger


class IGDL:
    def __init__(
        self,
        post: Optional[str],
        target: Optional[str],
        story: bool,
        login: Optional[str],
        passwd: Optional[str],
    ) -> None:
        self.post = post
        self.target = target
        self.story = story
        self.login = login
        self.passwd = passwd
        self.cookies = {}
        self.request = Authenticator()
        self.logger = Logger.generate("Downloader")

    async def authenticate(self):
        cookies = await self.request.login(user=self.login, passwd=self.passwd)
        return cookies

    async def download_post(self):
        auth = await self.authenticate()

    async def download_user(self):
        auth = await self.authenticate()

    async def start(self):
        if self.post:
            return await self.download_post()

        if self.target:
            return await self.download_user()
