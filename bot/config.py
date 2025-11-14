import os
from dataclasses import dataclass

from dotenv import load_dotenv

load_dotenv()


@dataclass
class Settings:
    bot_token: str


settings = Settings(
    bot_token=os.getenv("BOT_TOKEN", "").strip(),
)

if not settings.bot_token:
    raise RuntimeError("Не задан BOT_TOKEN в .env")
