import logging

from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery

from bot.db import has_consent, set_consent
from bot.keyboards.common import consent_keyboard, main_menu_keyboard

router = Router()
logger = logging.getLogger(__name__)


@router.message(CommandStart())
async def cmd_start(message: Message) -> None:
    user_id = message.from_user.id
    logger.info("Пользователь %s вызвал /start", user_id)

    if await has_consent(user_id):
        await message.answer(
            "Снова привет! Вы уже дали согласие на обработку персональных данных.\n\n"
            "Выберите раздел в главном меню ниже.",
            reply_markup=main_menu_keyboard(),
        )
        return

    await message.answer(
        "Привет! 👋\n\n"
        "Перед началом работы, пожалуйста, подтвердите согласие "
        "на обработку персональных данных.\n\n"
        "Продолжение возможно только в случае согласия.",
        reply_markup=consent_keyboard(),
    )


@router.callback_query(F.data == "consent_yes")
async def consent_yes(callback: CallbackQuery) -> None:
    user_id = callback.from_user.id
    logger.info("Пользователь %s дал согласие", user_id)

    await set_consent(user_id, True)

    await callback.message.edit_text(
        "Спасибо! ✅\n\n"
        "Ваше согласие на обработку персональных данных сохранено.\n\n"
        "Добро пожаловать в бот The Pops.\n"
        "Выберите раздел в главном меню ниже."
    )
    await callback.message.answer(
        "Главное меню:",
        reply_markup=main_menu_keyboard(),
    )
    await callback.answer()


@router.callback_query(F.data == "consent_no")
async def consent_no(callback: CallbackQuery) -> None:
    user_id = callback.from_user.id
    logger.info("Пользователь %s НЕ дал согласие", user_id)

    await set_consent(user_id, False)

    await callback.message.edit_text(
        "Без согласия на обработку персональных данных мы не можем продолжить работу.\n\n"
        "Если передумаете, просто снова отправьте команду /start."
    )
    await callback.answer()
