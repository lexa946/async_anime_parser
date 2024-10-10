from asyncio import Semaphore
from pathlib import Path

from aiofile import async_open
from aiohttp import ClientSession
from bs4 import BeautifulSoup
from tqdm.asyncio import tqdm_asyncio

from app.config import settings
from app.schemas import SAnimeSeria

sem = Semaphore(settings.COUNT_THREADS)


class Parser:
    semaphore = Semaphore(settings.COUNT_THREADS)
    headers = {
        "User-Agent": settings.USER_AGENT
    }

    @classmethod
    async def get_series(cls) -> list[SAnimeSeria]:
        async with ClientSession(headers=cls.headers) as session:
            async with session.get(settings.TARGET_URL) as resp:
                if resp.status == 200:
                    soup = BeautifulSoup(await resp.text(), 'lxml')
                else:
                    print(f'Страница {settings.TARGET_URL} не доступна')
                    return []

        series_links = soup.select('.short-btn.video.the_hildi')

        result = []

        for series_link in series_links:
            url = series_link.get('href')
            if "episode" not in url: continue

            series_attributes = url.strip("/").split("/")
            if len(series_attributes) == 2:
                name, episode = series_attributes
                season = None
            else:
                name, season, episode = series_attributes
            anime_seria = SAnimeSeria(name=name, url=settings.MAIN_URL + url, episode=episode.strip(".html"),
                                      season=season)
            result.append(anime_seria)
        return result


    @classmethod
    async def __download_video(cls, file_path_save: str, url: str, video_name: str) -> None:
        async with async_open(file_path_save, 'wb') as file:
            async with ClientSession(headers=cls.headers) as session:
                async with session.get(url) as resp:
                    resp.raise_for_status()

                    total = int(resp.headers.get('Content-Length', 0))

                    tqdm_params = {
                        'desc': video_name,
                        'total': total,
                        'miniters': 1,
                        'unit': 'it',
                        'unit_scale': True,
                        'unit_divisor': 1024
                    }
                    with tqdm_asyncio(**tqdm_params) as pbar:
                        async for chunk in resp.content.iter_chunked(settings.CHUNK_SIZE):
                            await file.write(chunk)
                            pbar.update(len(chunk))


    @classmethod
    async def download_seria(cls, seria: SAnimeSeria, path_save: Path) -> None:
        async with cls.semaphore:
            async with ClientSession(headers=cls.headers) as client:
                async with client.get(seria.url) as resp:
                    if resp.status == 200:
                        soup = BeautifulSoup(await resp.text(), 'lxml')
                    else:
                        print(f'Страница {seria.url} не доступна')
                        return

            video_tags = soup.select('video>source')
            if not video_tags:
                print(f"Не удалось найти видео по ссылке {seria.url}")
                return

            need_quality_video_tag = None

            for video_tag in video_tags:
                if video_tag.get('res') == settings.MAX_QUALITY:
                    need_quality_video_tag = video_tag

            if need_quality_video_tag is None:
                need_quality_video_tag = video_tag[0]

            (path_save / seria.name).mkdir(exist_ok=True)
            if seria.season:
                (path_save / seria.name / seria.season).mkdir(exist_ok=True)
                file_path_save = str(path_save / seria.name / seria.season / f"{seria.episode}.mp4")
                video_name = f"{seria.season}/{seria.episode}.mp4"
            else:
                file_path_save = str(path_save / seria.name / f"{seria.episode}.mp4")
                video_name = f"{seria.episode}.mp4"

            await cls.__download_video(file_path_save, need_quality_video_tag.get('src'), video_name)