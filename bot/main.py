import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from bot.config import settings
from bot.db import init_db
from bot.handlers import start, menu


def setup_logging() -> None:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    )


async def main() -> None:
    setup_logging()
    logger = logging.getLogger(__name__)
    logger.info("Запуск бота The Pops...")

    await init_db()
    logger.info("База данных инициализирована.")

    bot = Bot(
        token=settings.bot_token,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML),
    )

    dp = Dispatcher()

    dp.include_router(start.router)
    dp.include_router(menu.router)

    logger.info("Старт long polling...")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
