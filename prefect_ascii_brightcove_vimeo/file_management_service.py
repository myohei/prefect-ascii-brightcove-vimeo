import aiohttp
import boto3
from prefect import task
from smart_open import open


class FileManagementService:
    _bucket: str
    _s3: boto3.Session

    def __init__(self, bucket: str, s3: boto3.Session):
        self._s3 = s3
        self._bucket = bucket

    async def download_and_upload(self, src_url: str, dest_path: str):
        async with aiohttp.ClientSession(raise_for_status=True) as client:
            async with client.get(src_url) as resp:
                url = self._s3_uri(dest_path)
                with open(url, 'wb', transport_params={'client': self._s3.client('s3')}) as out:
                    async for c in resp.content:
                        out.write(c)

    def _s3_uri(self, path: str) -> str:
        if not path.startswith('/'):
            path = f'/${path}'
        return f's3://{self._bucket}{path}'


@task
async def fetch_video(service: FileManagementService):
    fake_uri = 'https://s3.us-west-2.amazonaws.com/apk.yohei.org/fix_first_interview.mp4?response-content-disposition=inline&X-Amz-Security-Token=IQoJb3JpZ2luX2VjEGEaDmFwLW5vcnRoZWFzdC0xIkgwRgIhAMgqmeUMlESO7WyyPfyL48TjQBmOvIZCzA64XztQyUHkAiEA1HudxbY%2B8%2BIQMazq9A8u0FW0T%2FcgyN1SkqUpQ5SCsNgqhQMIKhAAGgwxMDU2MzM1ODI1NDMiDB%2BfWEh2FDaCEzua5SriAkHnwrXCwOOwURvYDKsil18y9kcqY%2BCeedmJqY3koc5AXfLESp6QyzJWml6Hd3WRrje0J0shw1E2CJQaZe6uev2mzFk1kYZjcUu2nQJeFJhp%2BSaX0fyHeVFJ3LGttuR1nBInyPtmrCwzIWg7aLK2VExBWE9KmQuCPBvpT%2BLnrWddAegttQcTO%2BVLSIYZptcfO7WNqudAoCJaIph4GWHs57UYTrLtuHSyNrZEx%2Bk9mku0tBRX7f1WAvZLcLqEJ5M9cUAGsJ%2FKkvGmOZ598Ofp39cv8QmzPfFdQgPGdhqDqJEV7rXcvbhBZbfe85ssLQ4AYh8b2vPH7OFVuQHarp5Q4XIH56QZ%2Bu69z2Q4iaVTkwYlSgJywrpaAyerxlF2mdSLMkoH7DSv%2BhOIfo%2BKO0e3uZZ%2FduXdgN%2F7Nq%2FtHhOBKjkwY7ocvIhj%2FrWCG8Wtn1ffLonX%2F03CBHa%2BiVFniR4KEKeFDTDpj7mTBjqyAnDugS7PWrWFHdefPFVM9x6gYn72RZT3yAD9WbGTRtCDn69sEiv7ipRc3AqKNuLp%2FmHseaT1vc3WBkTNc0e2orolYbLeg%2BFCSoA1HgfuHjoY04%2BjEE5A2uPMBrrseNGHfjmzBAixuWm29UrpO8dBaDjXCgnMnfgkPC7hMu5L1455uSloqq98lHbBuUEdKVye7JGSr7%2BSYJH78ub6KH4FGxKIS08z76vfWEspL3Cj86eAUiPX6aWO8TJB6DK%2BPpAecWs1s1wc8aB8C8bQ1XqPqScEPNyw%2FRg8tWxcSGo%2FOzelVFXgiDaY6k4WiC4bZYJtqV9K45ycUvbd0CPexXRptJc1MhLxU6PqQWBCXNCImJaCQDeViSd8lyZmW78uYB%2BN6ekRzHuKOqRz3qR5PvnUnbbBmw%3D%3D&X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Date=20220501T084513Z&X-Amz-SignedHeaders=host&X-Amz-Expires=43200&X-Amz-Credential=ASIARRGCARXH2WQ2FTCV%2F20220501%2Fus-west-2%2Fs3%2Faws4_request&X-Amz-Signature=fd2d5600a48c3dfcfc4c6fe611921a323ececb254548bcbb4fe6f66347961c9e'
    await service.download_and_upload(src_url=fake_uri, dest_path='/dest/sample.mp4')
