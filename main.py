import os
from html import escape

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.constants import ParseMode
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes,
)

BOT_TOKEN = "8758136921:AAFQjy7NC5vNkfs8km45mGR4sELGgXNPpxw"
EVENTS = [
    {

        "type": "Действие пользователя",
        "title": "Пользователь запустил бота",
        "description": "Бот получил команду /start и показал приветствие.",
        "reaction": "Отправлено главное меню.",
    },
    {

        "type": "Действие пользователя",
        "title": "Открыт раздел «События»",
        "description": "Пользователь нажал кнопку «События» в главном меню.",
        "reaction": "Показан список доступных событий.",
    },
    {

        "type": "Действие пользователя",
        "title": "Открыт раздел «О боте»",
        "description": "Пользователь запросил информацию о назначении бота.",
        "reaction": "Показано описание проекта и разработчика.",
    },
    {

        "type": "Системное изменение",
        "title": "Обновление данных",
        "description": "Система обновила внутренний список событий.",
        "reaction": "Бот использует актуальный статичный массив.",
    }
]


def get_main_menu() -> InlineKeyboardMarkup:
    keyboard = [
        [InlineKeyboardButton("📅 События", callback_data="events")],
        [InlineKeyboardButton("ℹ️ О боте", callback_data="about")],
    ]

    return InlineKeyboardMarkup(keyboard)


def get_back_menu() -> InlineKeyboardMarkup:
    keyboard = [
        [InlineKeyboardButton("⬅️ В главное меню", callback_data="main_menu")]
    ]

    return InlineKeyboardMarkup(keyboard)


def format_events() -> str:
    text = "📅 <b>События бота</b>\n\n"
    text += "Ниже показаны события, на которые бот может реагировать:\n\n"

    for number, event in enumerate(EVENTS, start=1):
        event_type = escape(event["type"])
        title = escape(event["title"])
        description = escape(event["description"])
        reaction = escape(event["reaction"])

        text += (
            f" <b>{number}. {title}</b>\n"
            f" <b>Тип:</b> {event_type}\n"
            f" <b>Описание:</b> {description}\n"
            f" <b>Реакция бота:</b> {reaction}\n\n"
        )

    return text


def format_about() -> str:
    return (
        "ℹ️ <b>О боте</b>\n\n"
        "Этот бот реагирует на заданные события\n"
        "<b>Разработчик:</b> @katarseus"
    )


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    text = (
        "👋 <b>Привет!</b>\n\n"
        "Выбери нужный раздел в главном меню:\n"
    )

    await update.message.reply_text(
        text=text,
        reply_markup=get_main_menu(),
        parse_mode=ParseMode.HTML,
    )


async def handle_buttons(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query

    await query.answer()

    if query.data == "events":
        await query.edit_message_text(
            text=format_events(),
            reply_markup=get_back_menu(),
            parse_mode=ParseMode.HTML,
        )

    elif query.data == "about":
        await query.edit_message_text(
            text=format_about(),
            reply_markup=get_back_menu(),
            parse_mode=ParseMode.HTML,
        )

    elif query.data == "main_menu":
        await query.edit_message_text(
            text=(
                "Выбери нужный раздел:\n\n"
            ),
            reply_markup=get_main_menu(),
            parse_mode=ParseMode.HTML,
        )


def main() -> None:
    if not BOT_TOKEN:
        raise RuntimeError("Не найдена переменная окружения BOT_TOKEN")

    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(handle_buttons))

    print("Бот запущен. Нажми Ctrl+C для остановки.")

    app.run_polling(drop_pending_updates=True)


if __name__ == "__main__":
    main()