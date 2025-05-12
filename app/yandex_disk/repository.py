import aiohttp
import logging
from typing import BinaryIO
from app.settings import Settings

logger = logging.getLogger(__name__)


class YandexDiskRepository:
    def __init__(self):
        settings = Settings()
        self.token = settings.YANDEX_DISK_TOKEN
        self.base_path = settings.YANDEX_DISK_BASE_PATH
        self.headers = {
            "Authorization": f"OAuth {self.token}",
            "Accept": "application/json",
        }
        self.api_url = settings.YANDEX_DISK_API_URL
        self.upload_url = settings.YANDEX_DISK_UPLOAD_URL
        self.publish_url = settings.YANDEX_DISK_PUBLISH_URL
        self.info_url = settings.YANDEX_DISK_INFO_URL

    async def get_upload_url(self, filename: str) -> str:
        """Получает URL для загрузки файла"""
        params = {"path": f"{self.base_path}/{filename}", "overwrite": "true"}

        async with aiohttp.ClientSession() as session:
            async with session.get(
                self.upload_url, headers=self.headers, params=params
            ) as response:
                if response.status != 200:
                    error_text = await response.text()
                    logger.error(f"Failed to get upload URL: {error_text}")
                    raise Exception(f"Failed to get upload URL: {error_text}")

                data = await response.json()
                return data["href"]

    async def upload_file_content(
        self, upload_url: str, file_content: BinaryIO
    ) -> None:
        """Загружает содержимое файла"""
        async with aiohttp.ClientSession() as session:
            async with session.put(upload_url, data=file_content) as response:
                if response.status != 201:
                    error_text = await response.text()
                    logger.error(f"Failed to upload file: {error_text}")
                    raise Exception(f"Failed to upload file: {error_text}")

    async def publish_file(self, filename: str) -> None:
        """Делает файл публичным"""
        params = {"path": f"{self.base_path}/{filename}"}

        async with aiohttp.ClientSession() as session:
            async with session.put(
                self.publish_url, headers=self.headers, params=params
            ) as response:
                if response.status != 200:
                    error_text = await response.text()
                    logger.error(f"Failed to publish file: {error_text}")
                    raise Exception(f"Failed to publish file: {error_text}")

    async def get_public_url(self, filename: str) -> str:
        """Получает публичную ссылку на файл"""
        params = {"path": f"{self.base_path}/{filename}"}

        async with aiohttp.ClientSession() as session:
            async with session.get(
                self.info_url, headers=self.headers, params=params
            ) as response:
                if response.status != 200:
                    error_text = await response.text()
                    logger.error(f"Failed to get public URL: {error_text}")
                    raise Exception(f"Failed to get public URL: {error_text}")

                data = await response.json()
                return data["public_url"]
