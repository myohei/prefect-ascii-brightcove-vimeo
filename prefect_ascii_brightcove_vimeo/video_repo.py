from typing import List

import aiosqlite
from prefect import task

from .brightcove import Video


class VideoRepo:
    _db: aiosqlite.Connection

    @classmethod
    async def create(cls, filepath: str) -> "VideoRepo":
        conn = await aiosqlite.connect(filepath)
        await conn.execute("create table if not exists videos(id integer primary key, value json)")
        await conn.execute("delete from videos")
        await conn.execute("create table if not exists video_sources(id integer primary key, value json)")
        await conn.execute("delete from video_sources")
        await conn.commit()
        self = VideoRepo(conn)
        return self

    def __init__(self, db: aiosqlite.Connection):
        self._db = db

    async def save(self, video: Video):
        await self._db.execute("insert into videos values(?,?)", (video.id, video.to_json()))
        await self._db.commit()

    async def findall(self) -> List[Video]:
        videos = []
        async with self._db.execute_fetchall("select * from videos") as cursor:
            async for row in cursor:
                videos.append(Video.from_json(row['value']))
        return videos


@task(retries=3)
async def save_data(repo: VideoRepo, video: Video):
    await repo.save(video)
