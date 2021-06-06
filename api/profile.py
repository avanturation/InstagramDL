import asyncio
import random
from typing import Dict, Optional

from .request import DEFAULT_COOKIE, DEFAULT_HEADER, ROOT, BaseReq

QUERY_HASH = "02e14f6a7812a876f7d133c9555b1151"
PROFILE_HASH = "d4d88dc1500312af6f937f7b804c68c3"


class Profile(BaseReq):
    def __init__(self, auth_data: Optional[Dict], user_id: str) -> None:
        self.headers = DEFAULT_HEADER
        self.cookies = auth_data
        self.profile = user_id
        super().__init__()

    async def metadata(self) -> Dict:
        params = {"__a": 1}

        metadata = await self.get(
            f"{ROOT}/{self.profile}",
            params=params,
            headers=self.headers,
            cookies=self.cookies,
        )

        data = await metadata.json(encoding="utf-8")

        self.headers["Referer"] = f"https://www.instagram.com/{self.profile}/"
        self.metadata = data["graphql"]["user"]

        return self.metadata

    async def stories(self):
        if not self.metadata["has_clips"]:
            self.logger.error(
                f"User {self.metadata['full_name']} ({self.metadata['username']}) does not have any stories uploaded. Aborting"
            )
            exit()

        params = {"reel_ids": self.metadata["id"]}

        stories = await self.get(
            url=f"https://i.instagram.com/api/v1/feed/reels_media",
            params=params,
            headers=self.headers,
            cookies=self.cookies,
        )

        data = await stories.json(encoding="utf-8")

        story_videoes = [
            items["video_versions"][0]["url"]
            for items in data["reels"][str(self.metadata["id"])]["items"]
        ]

        return story_videoes

    async def grab_posts(self):

        await asyncio.sleep(min(random.expovariate(0.6), 15.0))

    async def download(self, stories: bool):
        try:
            await self.metadata()

            if stories:
                return await self.stories()

        finally:
            await self.session.close()
