from typing import Literal


class Config:
    credentials_database_host: str = "127.0.0.1"
    environment: Literal["dev", "stg", "prd"] = "dev"
    password_length: int = 16
