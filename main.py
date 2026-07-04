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


BOT_TOKEN = os.getenv("BOT_TOKEN")

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
    },
]


def get_main_menu():
    keyboard = [
        [InlineKeyboardButton("События", callback_data="events")],
        [InlineKeyboardButton("О боте", callback_data="about")],
    ]

    return InlineKeyboardMarkup(keyboard)


def get_back_menu():
    keyboard = [
        [InlineKeyboardButton("В главное меню", callback_data="main_menu")]
    ]

    return InlineKeyboardMarkup(keyboard)


def get_event_menu(index):
    keyboard = []

    navigation_buttons = []

    if index > 0:
        navigation_buttons.append(
            InlineKeyboardButton("Назад", callback_data=f"event_{index - 1}")
        )

    if index < len(EVENTS) - 1:
        navigation_buttons.append(
            InlineKeyboardButton("Вперёд", callback_data=f"event_{index + 1}")
        )

    if navigation_buttons:
        keyboard.append(navigation_buttons)

    keyboard.append(
        [InlineKeyboardButton("В главное меню", callback_data="main_menu")]
    )

    return InlineKeyboardMarkup(keyboard)


def format_event(index):
    event = EVENTS[index]

    event_type = escape(event["type"])
    title = escape(event["title"])
    description = escape(event["description"])
    reaction = escape(event["reaction"])

    total_events = len(EVENTS)
    current_number = index + 1

    text = (
        f"<b>Событие {current_number} из {total_events}</b>\n\n"
        f"<b>{title}</b>\n\n"
        f"<b>Тип:</b> {event_type}\n"
        f"<b>Описание:</b> {description}\n"
        f"<b>Реакция бота:</b> {reaction}\n\n"
    )

    return text


def format_about():
    return (
        "<b>О боте</b>\n\n"
        "Этот бот создан в рамках практики.\n\n"
        "<b>Разработчик:</b> @katarseus"
    )


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = (
        "<b>Привет!</b>\n\n"
        "Выбери нужный раздел в главном меню:"
    )

    await update.message.reply_text(
        text=text,
        reply_markup=get_main_menu(),
        parse_mode=ParseMode.HTML,
    )


async def handle_buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query

    await query.answer()

    if query.data == "events":
        index = 0

        await query.edit_message_text(
            text=format_event(index),
            reply_markup=get_event_menu(index),
            parse_mode=ParseMode.HTML,
        )

    elif query.data.startswith("event_"):
        index = int(query.data.replace("event_", ""))

        await query.edit_message_text(
            text=format_event(index),
            reply_markup=get_event_menu(index),
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
                "<b>Главное меню</b>\n\n"
                "Выбери нужный раздел:"
            ),
            reply_markup=get_main_menu(),
            parse_mode=ParseMode.HTML,
        )


def main() -> None:
    if not BOT_TOKEN:
        raise RuntimeError(
            "Не найден BOT_TOKEN. "
            "Перед запуском укажи токен в переменной окружения BOT_TOKEN."
        )

    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))

    app.add_handler(CallbackQueryHandler(handle_buttons))

    print("Бот запущен. Нажми Ctrl+C для остановки.")

    app.run_polling()


if __name__ == "__main__":
    main()