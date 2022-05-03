from datetime import timedelta

from ffmpeg_streaming import S3, CloudManager, input, Formats


def monitor(ffmpeg, duration, time_, time_left, process):
    per = round(time_ / duration * 100)
    print("Transcoding...(%s%%) %s left [%s%s]" %
          (per, timedelta(seconds=int(time_left)), '#' * per, '-' * (100 - per)))


class Converter:
    _bucket: str
    _credentials: "AwsS3Credentials"

    def __init__(self, bucket: str, credentials: "AwsS3Credentials"):
        self._credentials = credentials
        self._bucket = bucket

    async def download_and_upload(self, src_url: str, dest_path: str):
        s3 = S3(aws_access_key_id=self._credentials.aws_access_key_id,
                aws_secret_access_key=self._credentials.aws_secret_access_key,
                region_name=self._credentials.region_name)
        save_to_s3 = CloudManager().add(s3, bucket_name=self._bucket, )
        video = input(src_url)
        stream = video.stream2file(Formats.h264())
        stream.output(dest_path, clouds=save_to_s3, run_command=False)
        await stream.async_run(ffmpeg_bin='ffmpeg', monitor=monitor)
