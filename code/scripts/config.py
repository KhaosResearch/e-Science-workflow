import platform
import tempfile
from pathlib import Path

from pydantic import BaseSettings

from scripts.logger import logger


class _Settings(BaseSettings):
    # DFS
    MINIO_HOST: str = None
    MINIO_BUCKET: str = None
    MINIO_ACCESS_KEY: str = "minio"
    MINIO_SECRET_KEY: str = "minio"

    MONGO_HOST: str = None
    MONGO_USERNAME: str = None
    MONGO_ACCESS_KEY: str = None
    MONGO_DATABASE: str = None
    MONGO_COLLECTION: str = None

    DATA_DIR: str = str(
        Path("/tmp" if platform.system() == "Darwin" else tempfile.gettempdir())
    )

    class Config:
        env_file = ".env"
        file_path = Path(env_file)
        if not file_path.is_file():
            logger.warning("⚠️ `.env` not found in current directory")
            logger.info("⚙️ Loading settings from environment")
        else:
            logger.info(f"⚙️ Loading settings from dotenv @ {file_path.absolute()}")


settings = _Settings()
