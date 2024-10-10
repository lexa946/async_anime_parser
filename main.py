import asyncio
import pathlib

from aiohttp import ClientSession

from app.config import settings
from app.parser import Parser


headers = {
        "User-Agent": settings.USER_AGENT
    }

async def main():
    path_save = pathlib.Path(".", settings.PATH_SAVE)

    path_save.mkdir(exist_ok=True)

    async with ClientSession(headers=headers) as client:

        if settings.ONE_TARGET_URL:
            series = [Parser.get_one_seria(settings.ONE_TARGET_URL)]
        else:
            series = await Parser.get_series(client)

        print(f'Найдено {len(series)} эпизодов.')

        tasks = [Parser.download_seria(client, seria, path_save) for seria in series]
        await asyncio.gather(*tasks)


if __name__ == '__main__':
    asyncio.run(main())
