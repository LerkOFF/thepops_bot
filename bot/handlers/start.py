from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery

from bot.db import has_consent, set_consent
from bot.keyboards.common import consent_keyboard, main_menu_keyboard

router = Router()


@router.message(CommandStart())
async def cmd_start(message: Message):
    user_id = message.from_user.id

    if await has_consent(user_id):
        await message.answer(
            "Вы уже дали согласие. Главное меню:",
            reply_markup=main_menu_keyboard()
        )
        return

    await message.answer(
        "Привет! 👋\n\nДля продолжения требуется согласие "
        "на обработку персональных данных.",
        reply_markup=consent_keyboard()
    )


@router.callback_query(F.data == "consent_yes")
async def consent_yes(callback: CallbackQuery):
    await set_consent(callback.from_user.id, True)

    await callback.message.edit_text(
        "Спасибо! Согласие сохранено.\n\nГлавное меню:"
    )
    await callback.message.answer(
        "Выберите раздел:",
        reply_markup=main_menu_keyboard()
    )
    await callback.answer()


@router.callback_query(F.data == "consent_no")
async def consent_no(callback: CallbackQuery):
    await set_consent(callback.from_user.id, False)

    await callback.message.edit_text(
        "Вы отказались от согласия.\n"
        "Чтобы начать заново — /start"
    )
    await callback.answer()
