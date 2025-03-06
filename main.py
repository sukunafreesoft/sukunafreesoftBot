import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import psycopg2
import os
from keep_alive import keep_alive

keep_alive()

# === НАСТРОЙКИ ===
TOKEN = "7191146491:AAFqpXRbyKKac6sw_wKfeP-c0n_CYU9gScM"  # Замени на свой токен
CHANNELS = ["@perexodniksukuna", "@sukunasoft"]  # Каналы для подписки

# Вместо ссылок храним file_id (полученные ранее)
FILES = {
    "✅ - [PC] NerestPC Free 0.32.3 💻":
    "BQACAgQAAxkBAANOZ8cHg-2x0Hay-aR7vG-ZlZZcy_wAAnwZAAJbzThSj9620FDQfx82BA",
    "✅ - [Android ROOT] Excellent Crack 0.32.3 📱":
    "BQACAgQAAxkBAANYZ8cJYbq9pZHthzNuH6e9KRFAOkEAAogZAAJbzThSqxGG5Zaw0uU2BA"
}

bot = telebot.TeleBot(TOKEN)


# === ФУНКЦИЯ ПРОВЕРКИ ПОДПИСКИ ===
def is_subscribed(user_id):
    for channel in CHANNELS:
        try:
            status = bot.get_chat_member(channel, user_id).status
            if status not in ["member", "administrator", "creator"]:
                return False
        except Exception:
            return False
    return True


# === ГЛАВНОЕ МЕНЮ ===
@bot.message_handler(commands=["start"])
def send_welcome(message):
    user_id = str(message.chat.id)  # Используем строку для хранения в базе данных PostgreSQL

    markup = InlineKeyboardMarkup()
    for app_name in FILES.keys():
        markup.add(InlineKeyboardButton(app_name, callback_data=app_name))
    bot.send_message(message.chat.id, "*Выберите файл для скачивания:*"
                     "\n"
                     "\n"
                     ">Но сначала подпишитесь на проекты создателя"
                     "\n"
                     ">@perexodniksukuna"
                     "\n"
                     ">@sukunasoft",
                     reply_markup=markup,
                     parse_mode="MarkdownV2")


# === ОТПРАВКА КНОПКИ START НОВЫМ ПОЛЬЗОВАТЕЛЯМ ===
@bot.message_handler(content_types=["new_chat_members"])
def welcome_new_member(message):
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("🚀 Начать", callback_data="start_cmd"))
    bot.send_message(message.chat.id,
                     f"Привет, {message.new_chat_members[0].first_name}! 👋\n"
                     "Нажмите кнопку ниже, чтобы начать.",
                     reply_markup=markup)


# === ОБРАБОТКА НАЖАТИЯ КНОПКИ "START" ===
@bot.callback_query_handler(func=lambda call: call.data == "start_cmd")
def start_button_pressed(call):
    send_welcome(call.message)


# === ОБРАБОТКА ВЫБОРА ПРИЛОЖЕНИЯ ===
@bot.callback_query_handler(func=lambda call: call.data in FILES)
def send_file(call):
    user_id = call.from_user.id
    if is_subscribed(user_id):
        bot.send_document(user_id, FILES[call.data])  # Отправляет файл
    else:
        markup = InlineKeyboardMarkup()
        for channel in CHANNELS:
            markup.add(
                InlineKeyboardButton(f"Подписаться на {channel}",
                                     url=f"https://t.me/{channel[1:]}"))
        markup.add(
            InlineKeyboardButton("🔄 Проверить подписку",
                                 callback_data="check_sub"))
        bot.send_message(
            user_id,
            "❌ Вы не подписаны на все каналы! Подпишитесь и попробуйте снова.",
            reply_markup=markup)


# === ПРОВЕРКА ПОДПИСКИ ===
@bot.callback_query_handler(func=lambda call: call.data == "check_sub")
def check_subscription(call):
    user_id = call.from_user.id
    if is_subscribed(user_id):
        bot.send_message(
            user_id,
            "✅ Подписка подтверждена! Теперь выберите файл для скачивания снова."
        )
    else:
        bot.send_message(
            user_id,
            "❌ Вы всё ещё не подписаны на все каналы. Подпишитесь и попробуйте ещё раз."
        )

# === ЗАПУСК БОТА ===
bot.polling(none_stop=True)
