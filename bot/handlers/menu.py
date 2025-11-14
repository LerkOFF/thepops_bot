from aiogram import Router, F
from aiogram.types import Message, CallbackQuery

from bot.db import has_consent
from bot.keyboards.common import (
    main_menu_keyboard,
    back_to_main_inline,
    socials_inline,
)

router = Router()


async def _check_consent(message: Message) -> bool:
    if not await has_consent(message.from_user.id):
        await message.answer("Сначала используйте /start и дайте согласие.")
        return False
    return True


@router.callback_query(F.data == "main_menu")
async def back_to_main(callback: CallbackQuery):
    await callback.message.answer(
        "Главное меню:",
        reply_markup=main_menu_keyboard()
    )
    await callback.answer()


@router.message(F.text == "Бонусная система")
async def bonus(message: Message):
    if not await _check_consent(message):
        return

    text = (
        "Мы начисляем баллы (попсы) за активность:\n"
        "- за каждую покупку — 2 попса\n"
        "- за подписку на все соцсети — 3 попса\n"
        "- за каждого друга по персональной ссылке — 3 попса\n\n"
        "За 10 попсов — промокод на гель за 1 рубль.\n\n"
        "Чтобы получить попсы, отправьте чек или скриншот подписки: @thepops"
    )

    await message.answer(text, reply_markup=back_to_main_inline())


@router.message(F.text == "Наши соцсети")
async def socials(message: Message):
    if not await _check_consent(message):
        return

    await message.answer("Наши соц-сети:", reply_markup=socials_inline())


@router.message(F.text == "Сделать возврат")
async def refund(message: Message):
    if not await _check_consent(message):
        return

    text = (
        "Чтобы оформить возврат, напишите нам @thepops.\n"
        "Приложите фото чека и причину.\n"
        "Деньги возвращаются в течение 24 часов."
    )
    await message.answer(text, reply_markup=back_to_main_inline())


@router.message(F.text == "Предложить идею для развития")
async def ideas(message: Message):
    if not await _check_consent(message):
        return

    text = (
        "Мы всегда открыты к вашим идеям 🩷\n"
        "За лучшие идеи дарим подарки!\n"
        "Напишите нам @thepops и опишите вашу идею."
    )
    await message.answer(text, reply_markup=back_to_main_inline())


@router.message(F.text == "Другое")
async def other(message: Message):
    if not await _check_consent(message):
        return

    text = (
        "Хотите стать инвестором или предложить партнёрство?\n"
        "Напишите нам @thepops — обсудим ваши условия."
    )
    await message.answer(text, reply_markup=back_to_main_inline())
