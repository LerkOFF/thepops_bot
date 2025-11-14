from aiogram.types import (
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    ReplyKeyboardMarkup,
)
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder


def consent_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text="Согласен", callback_data="consent_yes")
    builder.button(text="Не согласен", callback_data="consent_no")
    builder.adjust(2)
    return builder.as_markup()


def main_menu_keyboard() -> ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder()
    builder.button(text="Бонусная система")
    builder.button(text="Наши соцсети")
    builder.button(text="Сделать возврат")
    builder.button(text="Предложить идею для развития")
    builder.button(text="Другое")
    builder.adjust(2, 2, 1)
    return builder.as_markup(resize_keyboard=True)


def back_to_main_inline() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(
        text="Вернуться в главное меню",
        callback_data="main_menu"
    )
    return builder.as_markup()


def socials_inline() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    # Заглушки – заменишь реальными ссылками
    builder.button(text="Наш Telegram", url="https://t.me/thepops")
    builder.button(text="Instagram", url="https://example.com/inst")
    builder.button(text="Наш сайт", url="https://example.com")

    builder.adjust(1)

    # Кнопка назад
    builder.row(
        InlineKeyboardButton(
            text="Вернуться в главное меню",
            callback_data="main_menu",
        )
    )

    return builder.as_markup()
