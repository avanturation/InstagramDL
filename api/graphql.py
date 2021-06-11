from typing import Dict, Optional

from .request import DEFAULT_HEADER, ROOT, BaseReq


class GraphQL(BaseReq):
    def __init__(self, auth_data: Optional[Dict], user_id: str) -> None:
        self.headers = DEFAULT_HEADER
        self.cookies = auth_data
        self.profile = user_id
        super().__init__()

    async def query(self, hash: str, variables: dict):
        params = {"query_hash": hash, "variables": variables}

        result = await self.get(
            url=f"{ROOT}/graphql/query/",
            params=params,
            headers=self.headers,
            cookies=self.cookies,
        )

        data = await result.json(encoding="utf-8")
        return data
