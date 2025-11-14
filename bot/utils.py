import asyncio
import logging

from aiogram import Bot
from aiogram.exceptions import TelegramBadRequest

logger = logging.getLogger(__name__)


def schedule_delete(
    bot: Bot,
    chat_id: int,
    message_id: int,
    delay: int = 60,
) -> None:
    """
    Планирует удаление сообщения через delay секунд.
    Ничего не ломает, если сообщения уже нет.
    """

    async def _worker():
        await asyncio.sleep(delay)
        try:
            await bot.delete_message(chat_id, message_id)
            logger.debug(
                "Удалено сообщение %s в чате %s",
                message_id,
                chat_id,
            )
        except TelegramBadRequest:
            # Уже удалено или нельзя удалить – не критично
            logger.debug(
                "Не удалось удалить сообщение %s (возможно, уже удалено)",
                message_id,
            )
        except Exception as e:  # на всякий случай
            logger.warning(
                "Ошибка при удалении сообщения %s: %s",
                message_id,
                e,
            )

    asyncio.create_task(_worker())
