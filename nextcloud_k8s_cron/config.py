from typing import List
from pydantic_settings import BaseSettings, SettingsConfigDict


class Config(BaseSettings):
    namespace: str = "nextcloud"
    pod_label: str = "nextcloud"
    command: List[str] = [
        "su",
        "-s",
        "/bin/sh",
        "www-data",
        "-c",
        "'php -f /var/www/html/cron.php'",
    ]
    model_config = SettingsConfigDict()
