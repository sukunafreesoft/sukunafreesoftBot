import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import requests

# === НАСТРОЙКИ ===
TOKEN = "7191146491:AAFqpXRbyKKac6sw_wKfeP-c0n_CYU9gScM"  # Замени на свой токен бота
CHANNELS = ["@sukunafreesoft", "@sukunasoft"]  # Список каналов, на которые нужно подписаться
FILES = {
    "Приложение 1": "https://shre.su/A583",
    "Приложение 2": "https://sukunafreesoft.pp.ua"
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
    markup = InlineKeyboardMarkup()
    for app_name in FILES.keys():
        markup.add(InlineKeyboardButton(app_name, callback_data=app_name))
    bot.send_message(message.chat.id, "Выберите приложение для скачивания:", reply_markup=markup)

# === ОБРАБОТКА ВЫБОРА ПРИЛОЖЕНИЯ ===
@bot.callback_query_handler(func=lambda call: call.data in FILES)
def send_file(call):
    user_id = call.from_user.id
    if is_subscribed(user_id):
        bot.send_message(user_id, f"✅ Вот ваша ссылка: {FILES[call.data]}")
    else:
        markup = InlineKeyboardMarkup()
        for channel in CHANNELS:
            markup.add(InlineKeyboardButton(f"Подписаться на {channel}", url=f"https://t.me/{channel[1:]}"))
        markup.add(InlineKeyboardButton("🔄 Проверить подписку", callback_data="check_sub"))
        bot.send_message(user_id, "❌ Вы не подписаны на все каналы! Подпишитесь и попробуйте снова.", reply_markup=markup)

# === ПРОВЕРКА ПОДПИСКИ ===
@bot.callback_query_handler(func=lambda call: call.data == "check_sub")
def check_subscription(call):
    user_id = call.from_user.id
    if is_subscribed(user_id):
        bot.send_message(user_id, "✅ Подписка подтверждена! Теперь выберите приложение снова.")
    else:
        bot.send_message(user_id, "❌ Вы всё ещё не подписаны на все каналы. Подпишитесь и попробуйте ещё раз.")

# === ЗАПУСК БОТА ===
bot.polling(none_stop=True)
