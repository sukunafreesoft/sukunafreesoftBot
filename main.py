import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

# === НАСТРОЙКИ ===
TOKEN = "7191146491:AAFqpXRbyKKac6sw_wKfeP-c0n_CYU9gScM"  # Замени на свой токен
CHANNELS = ["@sukunasoft", "@perexodniksukuna"]  # Каналы для подписки

# Вместо ссылок храним file_id (полученные ранее)
FILES = {
    "💻[PC] NerestPC Free 0.32.3": "BQACAgQAAxkBAAMeZ8mX5HupwDAyqWU82kRZFIY3iO4AAnwZAAJbzThSdA6U8VArn002BA",
    "📱[Android ROOT] Excellent Crack 0.32.3": "BQACAgQAAxkBAAMfZ8mX5LJ3TPKEAfjakG2psV1W35wAAogZAAJbzThSN_kk0FblCfI2BA"
}

TEXTS = {
    "💻[PC] NerestPC Free 0.32.3": "ℹ️[Туториала пока нет](https://t.me/sukunasoft)",
    "📱[Android ROOT] Excellent Crack 0.32.3": "ℹ️[Туториал](https://t.me/sukunasoft/168)"
}

bot = telebot.TeleBot(TOKEN)

# Словарь для хранения ID последнего отправленного сообщения (не меню)
last_response = {}

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
    user_id = message.chat.id

    markup = InlineKeyboardMarkup()
    for app_name in FILES.keys():
        markup.add(InlineKeyboardButton(app_name, callback_data=app_name))
    
    bot.send_message(
        user_id,
        "🔽 *Выберите файл для скачивания:* 🔽\n\n"
        "☣️ *Но сначала подпишитесь на проекты создателя:* ☣️\n"
        "🔗 [@sukunasoft](https://t.me/sukunasoft)\n"
        "🔗 [@perexodniksukuna](https://t.me/perexodniksukuna)",
        reply_markup=markup,
        parse_mode="Markdown"
    )

# === ФУНКЦИЯ УДАЛЕНИЯ ПРЕДЫДУЩЕГО СООБЩЕНИЯ (КРОМЕ МЕНЮ) ===
def delete_last_response(user_id):
    if user_id in last_response:
        try:
            bot.delete_message(user_id, last_response[user_id])
        except Exception:
            pass  # Если сообщение уже удалено, просто игнорируем

# === ОБРАБОТКА ВЫБОРА ФАЙЛА ===
@bot.callback_query_handler(func=lambda call: call.data in FILES)
def send_file(call):
    user_id = call.from_user.id
    delete_last_response(user_id)  # Удаляем старое сообщение (не меню!)

    if is_subscribed(user_id):
        file_id = FILES.get(call.data)
        caption = TEXTS.get(call.data, "ℹ Инструкции пока нет.")

        try:
            sent_message = bot.send_document(user_id, file_id, caption=caption, parse_mode="Markdown")
            last_response[user_id] = sent_message.message_id  # Запоминаем ID нового сообщения
        except Exception as e:
            error_message = bot.send_message(user_id, f"❌ Ошибка при отправке файла: {str(e)}")
            last_response[user_id] = error_message.message_id
    else:
        send_subscription_request(user_id)

# === ПРОСЬБА ПОДПИСАТЬСЯ ===
def send_subscription_request(user_id):
    markup = InlineKeyboardMarkup()
    for channel in CHANNELS:
        markup.add(InlineKeyboardButton(f"Подписаться на {channel}", url=f"https://t.me/{channel[1:]}"))
    markup.add(InlineKeyboardButton("🔄 Проверить подписку", callback_data="check_sub"))

    sent_message = bot.send_message(
        user_id,
        "❌ *Ты не подписан на все проекты!*\n\nПодпишись и попробуй ещё.",
        reply_markup=markup,
        parse_mode="Markdown"
    )
    last_response[user_id] = sent_message.message_id  # Сохраняем ID нового сообщения

# === ПРОВЕРКА ПОДПИСКИ ===
@bot.callback_query_handler(func=lambda call: call.data == "check_sub")
def check_subscription(call):
    user_id = call.from_user.id
    delete_last_response(user_id)  # Удаляем предыдущее сообщение

    if is_subscribed(user_id):
        sent_message = bot.send_message(user_id, "✅ Подписка обнаружена! Теперь выбери файл для скачивания.")
    else:
        sent_message = bot.send_message(user_id, "❌ Ты всё ещё не подписан на все проекты. Подпишись и попробуй ещё раз.")

    last_response[user_id] = sent_message.message_id  # Сохраняем ID нового сообщения

# === ОБРАБОТКА ФАЙЛОВ ДЛЯ ПОЛУЧЕНИЯ FILE_ID ===
@bot.message_handler(content_types=["document", "video", "audio", "photo"])
def get_file_id(message):
    if message.document:
        file_id = message.document.file_id
    elif message.video:
        file_id = message.video.file_id
    elif message.audio:
        file_id = message.audio.file_id
    elif message.photo:
        file_id = message.photo[-1].file_id  # Берем самое большое фото
    
    bot.send_message(message.chat.id, f"📎 File ID: `{file_id}`", parse_mode="Markdown")

# === ЗАПУСК БОТА ===
bot.polling(none_stop=True)
