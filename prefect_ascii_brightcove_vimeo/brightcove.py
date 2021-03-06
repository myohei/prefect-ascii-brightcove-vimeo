import base64
from typing import Optional, List

import aiohttp
from prefect import task, get_run_logger
from dataclasses import dataclass
from .data import Video, VideoSource

_limit = 2


class BrightcoveService:
    _base_url: str
    _auth_str: str
    _access_token: Optional[str] = None

    def __init__(self, auth_str: str, account_id: str):
        self.ses = aiohttp.ClientSession()
        self._auth_str = auth_str
        self.base_url = f'https://cms.api.brightcove.com/v1/accounts/{account_id}'

    async def _login(self):
        async with self.ses.post('https://oauth.brightcove.com/v4/access_token',
                                 headers={'Authorization': 'Basic ' + self._auth_str,
                                          'Content-Type': 'application/x-www-form-urlencoded'},
                                 data={'grant_type': 'client_credentials'}) as resp:
            if not resp.ok:
                raise Exception('response was not ok')
            j = await resp.json()
            self._access_token = j['access_token']

    async def get_all_videos(self) -> List[Video]:
        if self._access_token is None:
            await self._login()
        videos: List[Video] = []
        limit = _limit
        size = limit
        offset = 0
        while size is limit:
            v = await self._get_video(offset=offset, limit=size)
            size = len(v)
            videos += v
            # TODO(mae): REMOVE THIS break
            break
        return videos

    async def _get_video(self, offset: int, limit: int) -> List[Video]:
        async with self.ses.get(self._url('/videos'),
                                params={'limit': limit, 'offset': offset},
                                headers={'Authorization': f'Bearer {self._access_token}'}) as resp:
            if not resp.ok:
                raise Exception('video get error')
            json = await resp.json()
            get_run_logger().info(json)
            videos = Video.schema().load(json, many=True)
            return videos

    def _url(self, path: str):
        return f'{self.base_url}{path}'

    async def get_video_source(self, video_id: str) -> List[VideoSource]:
        if self._access_token is None:
            await self._login()
        async with self.ses.get(self._url(f'/videos/{video_id}/sources'),
                                headers={'Authorization': f'Bearer {self._access_token}'}) as resp:
            if not resp.ok:
                raise Exception(f'video source get error: response {resp.status}')
            json = await resp.json()
            get_run_logger().info(json)
            video_sources = VideoSource.schema().load(json, many=True)
            return video_sources


@dataclass
class BrightcoveCredentials:
    account_id: str
    client_id: str
    client_secret: str

    def create_service(self) -> BrightcoveService:
        plain_auth_str = f'{self.client_id}:{self.client_secret}'
        auth_str = base64.b64encode(plain_auth_str.encode()).decode()
        return BrightcoveService(auth_str=auth_str, account_id=self.account_id)


@task
async def fetch_brightcove_data(credentials: BrightcoveCredentials) -> List[Video]:
    service = credentials.create_service()
    result = await service.get_all_videos()
    await service.ses.close()
    return result


@task
async def fetch_video_source(credentials: BrightcoveCredentials, video_id: str):
    service = credentials.create_service()
    sources = await service.get_video_source(video_id=video_id)
    await service.ses.close()
    print(sources)
    return sources
