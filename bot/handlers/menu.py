import logging
from typing import Dict, Tuple

from aiogram import Router, F, Bot
from aiogram.types import Message, CallbackQuery

from bot.db import has_consent
from bot.keyboards.common import (
    main_menu_keyboard,
    back_to_main_inline,
    socials_inline,
)

router = Router()
logger = logging.getLogger(__name__)

# user_id -> (chat_id, message_id)
section_messages: Dict[int, Tuple[int, int]] = {}


async def _check_consent_or_warn(message: Message) -> bool:
    """Проверка согласия перед любым действием в меню."""
    user_id = message.from_user.id
    if not await has_consent(user_id):
        await message.answer(
            "Чтобы пользоваться ботом, сначала дайте согласие "
            "на обработку персональных данных командой /start."
        )
        return False
    return True


async def _delete_last_card(bot: Bot, user_id: int) -> None:
    """Удаляем последнюю карточку секции для пользователя, если есть."""
    data = section_messages.get(user_id)
    if not data:
        return

    chat_id, msg_id = data
    try:
        await bot.delete_message(chat_id=chat_id, message_id=msg_id)
        logger.debug(
            "Удалена предыдущая карточка: user_id=%s, msg_id=%s",
            user_id,
            msg_id,
        )
    except Exception as e:
        # Не падаем, просто логируем (могут быть ограничения по времени и т.п.)
        logger.warning(
            "Не удалось удалить карточку: user_id=%s, msg_id=%s, ошибка=%s",
            user_id,
            msg_id,
            e,
        )


async def _send_section_card(
    message: Message,
    text: str,
):
    """Универсальная отправка карточки с предварительным удалением предыдущей."""
    user_id = message.from_user.id

    await _delete_last_card(message.bot, user_id)

    sent = await message.answer(text, reply_markup=back_to_main_inline())

    # запоминаем последнюю карточку
    section_messages[user_id] = (sent.chat.id, sent.message_id)
    logger.info(
        "Отправлена новая карточка секции: user_id=%s, msg_id=%s",
        user_id,
        sent.message_id,
    )


@router.callback_query(F.data == "main_menu")
async def on_back_to_main(callback: CallbackQuery) -> None:
    """Инлайн-кнопка «Вернуться в главное меню»."""
    user_id = callback.from_user.id
    await _delete_last_card(callback.bot, user_id)

    await callback.message.answer(
        "Главное меню:",
        reply_markup=main_menu_keyboard(),
    )
    await callback.answer()


# ---------- Разделы главного меню ----------

@router.message(F.text == "Бонусная система")
async def bonus_system(message: Message) -> None:
    if not await _check_consent_or_warn(message):
        return

    text = (
        "Мы начисляем баллы (попсы) за активность:\n"
        "- за каждую покупку — 2 попса\n"
        "- за подписку на все соцсети — 3 попса\n"
        "- за каждого друга, оформившего заказ по вашей персональной ссылке — 3 попса\n\n"
        "За 10 попсов вы получаете промокод на покупку нашего геля за 1 рубль.\n\n"
        "Чтобы получить попсы, отправьте чек о покупке или скриншот "
        "подписки нам в tg: @thepops"
    )

    await _send_section_card(message, text)


@router.message(F.text == "Наши соцсети")
async def socials(message: Message) -> None:
    if not await _check_consent_or_warn(message):
        return

    user_id = message.from_user.id
    await _delete_last_card(message.bot, user_id)

    sent = await message.answer(
        "Наши соц-сети:",
        reply_markup=socials_inline(),
    )

    section_messages[user_id] = (sent.chat.id, sent.message_id)
    logger.info(
        "Отправлена карточка «Наши соцсети»: user_id=%s, msg_id=%s",
        user_id,
        sent.message_id,
    )


@router.message(F.text == "Сделать возврат")
async def make_return(message: Message) -> None:
    if not await _check_consent_or_warn(message):
        return

    text = (
        "Чтобы оформить возврат, напишите нам @thepops\n"
        "Приложите фото чека и кратко опишите причину возврата\n"
        "Деньги возвращаются в течение 24 часов."
    )

    await _send_section_card(message, text)


@router.message(F.text == "Предложить идею для развития")
async def suggest_idea(message: Message) -> None:
    if not await _check_consent_or_warn(message):
        return

    text = (
        "Мы всегда открыты к вашим идеям и предложениям 🩷\n"
        "За лучшие идеи дарим подарки\n"
        "Напишите нам @thepops и опишите вашу идею"
    )

    await _send_section_card(message, text)


@router.message(F.text == "Другое")
async def other(message: Message) -> None:
    if not await _check_consent_or_warn(message):
        return

    text = (
        "Если вы хотите стать инвестором или предложить партнёрство,\n"
        "напишите нам @thepops\n"
        "Мы готовы обсудить ваши условия."
    )

    await _send_section_card(message, text)
