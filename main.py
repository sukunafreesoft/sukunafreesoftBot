import telebot
import time
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from keep_alive import keep_alive

keep_alive()

# === НАСТРОЙКИ ===
TOKEN = "7588669661:AAHm2L9C3LfMAYmuodztMjqssFePX_eAyds"  # Замени на свой токен
CHANNELS = ["@perexodniksukuna", "@sukunasoft"]  # Каналы для подписки

# Вместо ссылок храним file_id (полученные ранее)
FILES = {
    "✅ - [PC] NerestPC Free 0.32.3 💻": "BQACAgQAAxkBAAMeZ8mX5HupwDAyqWU82kRZFIY3iO4AAnwZAAJbzThSdA6U8VArn002BA",
    "✅ - [Android ROOT] Excellent Crack 0.32.3 📱": "BQACAgQAAxkBAAMfZ8mX5LJ3TPKEAfjakG2psV1W35wAAogZAAJbzThSN_kk0FblCfI2BA"
}

# Тексты, которые будут отправляться вместе с файлами
TEXTS = {
    "✅ - [PC] NerestPC Free 0.32.3 💻": "⁉️[Туториал](https://t.me/sukunasoft/168)",
    "✅ - [Android ROOT] Excellent Crack 0.32.3 📱": "⁉️[Туториала пока нет](https://t.me/sukunasoft)"
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
    bot.send_message(
        message.chat.id,
        "🔽 *Выберите файл для скачивания:* 🔽\n\n"
        "‼️*Но сначала подпишитесь на проекты создателя:*‼️ \n"
        "👉 [@perexodniksukuna](https://t.me/perexodniksukuna)\n"
        "👉 [@sukunasoft](https://t.me/sukunasoft)",
        reply_markup=markup,
        parse_mode="Markdown"
    )

# === ОБРАБОТКА ВЫБОРА ПРИЛОЖЕНИЯ ===
@bot.callback_query_handler(func=lambda call: call.data in FILES)
def send_file(call):
    user_id = call.from_user.id
    if is_subscribed(user_id):
        file_id = FILES.get(call.data)
        caption = TEXTS.get(call.data, "ℹ Туториала пока нет!")
        
        try:
            # Отправляем файл с подписью
            bot.send_document(user_id, file_id, caption=caption, parse_mode="Markdown")
        except Exception as e:
            bot.send_message(user_id, f"❌ Ошибка при отправке файла: {str(e)}")
    else:
        markup = InlineKeyboardMarkup()
        for channel in CHANNELS:
            markup.add(InlineKeyboardButton(f"Подписаться на {channel}", url=f"https://t.me/{channel[1:]}"))
        markup.add(InlineKeyboardButton("🔄 Проверить подписку", callback_data="check_sub"))
        bot.send_message(
            user_id,
            "❌ *Вы не подписаны на все каналы!*\n\nПодпишитесь и попробуйте снова.",
            reply_markup=markup,
            parse_mode="Markdown"
        )

# === ПРОВЕРКА ПОДПИСКИ ===
@bot.callback_query_handler(func=lambda call: call.data == "check_sub")
def check_subscription(call):
    user_id = call.from_user.id
    if is_subscribed(user_id):
        bot.send_message(user_id, "✅ Подписка подтверждена! Теперь выберите файл для скачивания снова.")
    else:
        bot.send_message(user_id, "❌ Вы всё ещё не подписаны на все каналы. Подпишитесь и попробуйте ещё раз.")

# === ЗАПУСК БОТА ===
bot.polling(none_stop=True)
