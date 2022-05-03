import aiohttp
import boto3
from prefect import task
from smart_open import open
from dataclasses import dataclass

from .converter import Converter


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


@dataclass
class AwsS3Credentials:
    aws_access_key_id: str
    aws_secret_access_key: str
    region_name: str
    bucket: str

    def create_file_management_service(self) -> FileManagementService:
        client = boto3.Session(aws_access_key_id=self.aws_access_key_id,
                               aws_secret_access_key=self.aws_secret_access_key,
                               region_name=self.region_name, )
        return FileManagementService(bucket=self.bucket, s3=client)

    def create_converter(self) -> Converter:
        return Converter(bucket=self.bucket, credentials=self)


@task
async def fetch_video(credentials: AwsS3Credentials):
    service = credentials.create_file_management_service()
    fake_uri = 'https://s3.us-west-2.amazonaws.com/apk.yohei.org/fix_first_interview.mp4?response-content-disposition=inline&X-Amz-Security-Token=IQoJb3JpZ2luX2VjEI7%2F%2F%2F%2F%2F%2F%2F%2F%2F%2FwEaDmFwLW5vcnRoZWFzdC0xIkcwRQIgB02dRmtp6SN4J%2Frr3ZQWsq4Ny%2FomfKOhEJOR3BgXYcMCIQCySfn8DRJU3FoKwQ%2FMYM%2B%2BDxG703D9WutQyOPjOlmCAir7AghXEAAaDDEwNTYzMzU4MjU0MyIMZvBUA0YtNizadplnKtgCX4SW7w4JO4CUhCUosl9lZBas2NBDEinHkyI3NcvCzY9%2B0VrzhHBQgKmgyREl3Mqm95ZLHikCU5Mg7nussnmdtP%2FCwWOurQfQoCV5J%2FOnVcNCYCFjDJtXoyRbo3TSFN6pnn8QqR3%2Fy4dJjX3h%2Bhoq6qlKRE543f7BQb07zFTRZ70xBpCZne9PggUn0A9pwa9m2whLRGv%2F3zqrhtdaSnUyET8LcWB7koPlCVihAi3iEttR5meOMac1JebAnCN37aZ4s72btey4O3FAJvWmOdct%2BaHDks8tnCwiUfuZQsXK4B0RBIR5Z51fYCdD9ze9fku6geV%2Fz3EShLaamqMXNFcvdW1lDKMKShpHviYa2kO1k8XE2fbpYDmkb%2BaUSwgTb%2Ft5cH%2FmePlbC9GCVHz%2F8Ng2ikIPhPytpM3ytgWfYxpLKLBNtTaHCIs5DJeYyM21Qsv1C40vJvJdKtgw%2FY7DkwY6swLRoAud0Itc3r3%2FbUjbayO%2Fu2zXLNaj1a9rnq78Wqhl63LyVN4WXCKEGvrVQ2mKmVV76Fxvb7KgBnSpVUym2VR3C%2BYzPHDPMWjnCtg7OUrcf7UnK21tJDYvgVNKShd5U1w5PgMqOXaFFFNY0bAvLM%2BoevSBgpwUdNQJliHie9EKBIHVXr64agGtijAEs8E2JtL4UxOoP8hyX1e%2F66onHvil1yk5wPje%2FNHK9MwumCvdM10xYxSnRb8uOK9EAOfVp%2BJ7XVl3pI%2FnsLeJ8J%2BYeTevF%2FGSEhgk0ebFBq76TlDPFm9bVNWKMUgPS%2BG52DIfwHuTVqnFoccxyMw6aHKMmWfPfWM7ahYSVl8%2BHFX0j4UImP6OF3GBvgW4xuTDDFARUI1%2Fmq1xUXMP%2FXzqIeG1OSR80cXJ&X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Date=20220503T073250Z&X-Amz-SignedHeaders=host&X-Amz-Expires=43200&X-Amz-Credential=ASIARRGCARXHUNAWPRS5%2F20220503%2Fus-west-2%2Fs3%2Faws4_request&X-Amz-Signature=494e33d572e97fb0692877f1bfb2434ac9274ea139f13eaa3bcb434e2a0bf672'
    await service.download_and_upload(src_url=fake_uri, dest_path='/dest/sample.mp4')


@task
def convert(credentials: AwsS3Credentials, src: str, dest: str):
    c = credentials.create_converter()
    c.download_and_upload(src_url=src, dest_path=dest)
