import logging
from typing import BinaryIO
from app.yandex_disk.repository import YandexDiskRepository

logger = logging.getLogger(__name__)


class YandexDiskService:
    def __init__(self):
        self.storage = YandexDiskRepository()

    async def upload_file(self, file_content: BinaryIO, filename: str) -> str:
        """
        Uploads file to Yandex.Disk and return public url.
        """
        try:
            # get upload url
            upload_url = await self.storage.get_upload_url(filename)
            logger.info(f"Got upload URL for {filename}")

            # download file
            await self.storage.upload_file_content(upload_url, file_content)
            logger.info(f"Uploaded file {filename}")

            # make file public
            await self.storage.publish_file(filename)
            logger.info(f"Published file {filename}")

            # get public url
            public_url = await self.storage.get_public_url(filename)
            logger.info(f"Got public URL for {filename}: {public_url}")

            return public_url
        except Exception as e:
            logger.error(f"Error uploading file {filename}: {str(e)}")
            raise
