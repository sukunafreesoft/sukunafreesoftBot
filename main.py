import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from referral import handle_referral, get_user_referrals

TOKEN = "7191146491:AAFqpXRbyKKac6sw_wKfeP-c0n_CYU9gScM"
CHANNELS = ["@sukunasoft", "@perexodniksukuna"]

FILES_PC = {
    "💻 [PC] NerestPC Free 0.32.3": "BQACAgQAAxkBAAMeZ8mX5HupwDAyqWU82kRZFIY3iO4AAnwZAAJbzThSdA6U8VArn002BA",
    "💻 [PC] Nerest External Crack 0.32.3": "BQACAgIAAyEFAASKyTTrAAMLZ9J9SFLVzWl44CH5PknMVaUJSusAAoJmAAKQ_IlKCAIQK2EpC3k2BA"
}

FILES_ANDROID = {
    "📱 [Android ROOT] Excellent Crack 0.32.3": "BQACAgIAAyEFAASKyTTrAAMKZ9J6MGXLPM4NLUNAiUDWwwrZz3oAAqpsAAKQ_JFKwTitg3eN_k42BA"
}

TEXTS = {
    "💻 [PC] NerestPC Free 0.32.3": "ℹ️[Туториала пока нет](https://t.me/sukunasoft)",
    "💻 [PC] Nerest External Crack 0.32.3": "ℹ️[Туториал в архиве](https://t.me/sukunasoft)",
    "📱 [Android ROOT] Excellent Crack 0.32.3": "ℹ️[Туториал](https://t.me/sukunasoft/168)"
}

bot = telebot.TeleBot(TOKEN)

def is_subscribed(user_id):
    for channel in CHANNELS:
        try:
            status = bot.get_chat_member(channel, user_id).status
            if status not in ["member", "administrator", "creator"]:
                return False
        except Exception:
            return False
    return True

@bot.message_handler(commands=["start"])
def send_welcome(message):
    user_id = message.chat.id
    handle_referral(user_id, message.text)

    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("👾 Читы", callback_data="download_files"))
    markup.add(InlineKeyboardButton("ℹ Установка ROOT", callback_data="tutor_root"))
    markup.add(InlineKeyboardButton("👤 Мой Профиль", callback_data="profile"))

    bot.send_message(user_id, "🗿 Доброго времени суток, выбирай что хочешь. \n\nНо сначала подпишись на мои проекты: \n Канал: @sukunasoft \n\nПереходник: @perexodniksukuna", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data == "download_files")
def send_download_menu(call):
    user_id = call.from_user.id
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("📱 Android", callback_data="android_files"))
    markup.add(InlineKeyboardButton("💻 ПК", callback_data="pc_files"))
    markup.add(InlineKeyboardButton("🔙 Назад", callback_data="back_main"))

    bot.send_message(user_id, "🔽 Выберите категорию:", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data == "android_files")
def send_android_files(call):
    user_id = call.from_user.id
    markup = InlineKeyboardMarkup()
    for app_name in FILES_ANDROID.keys():
        markup.add(InlineKeyboardButton(app_name, callback_data=app_name))

    markup.add(InlineKeyboardButton("🔙 Назад", callback_data="download_files"))
    bot.send_message(user_id, "📱 Выберите Android-приложение:", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data == "pc_files")
def send_pc_files(call):
    user_id = call.from_user.id
    markup = InlineKeyboardMarkup()
    for app_name in FILES_PC.keys():
        markup.add(InlineKeyboardButton(app_name, callback_data=app_name))

    markup.add(InlineKeyboardButton("🔙 Назад", callback_data="download_files"))
    bot.send_message(user_id, "💻 Выберите программу для ПК:", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data in FILES_PC or call.data in FILES_ANDROID)
def send_file(call):
    user_id = call.from_user.id
    if is_subscribed(user_id):
        file_id = FILES_PC.get(call.data) or FILES_ANDROID.get(call.data)
        caption = TEXTS.get(call.data, "ℹ Инструкции пока нет.")
        bot.send_document(user_id, file_id, caption=caption, parse_mode="Markdown")
    else:
        send_subscription_request(user_id)

@bot.callback_query_handler(func=lambda call: call.data == "profile")
def send_profile(call):
    user_id = call.from_user.id
    referrals = get_user_referrals(user_id)

    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("📩 Пригласить друга", callback_data="send_invite_link"))
    markup.add(InlineKeyboardButton("🔙 Назад", callback_data="back_main"))

    bot.send_message(user_id, f"👤 Ваш профиль:\n👥 Приглашено пользователей: {referrals}", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data == "send_invite_link")
def send_invite_link(call):
    user_id = call.from_user.id
    invite_link = f"https://t.me/sukunafreesoftBot?start={user_id}"
    bot.send_message(user_id, f"📩 Ваша реферальная ссылка:\n{invite_link}")

def send_subscription_request(user_id):
    markup = InlineKeyboardMarkup()
    for channel in CHANNELS:
        markup.add(InlineKeyboardButton(f"Подписаться на {channel}", url=f"https://t.me/{channel[1:]}"))
    markup.add(InlineKeyboardButton("🔄 Проверить подписку", callback_data="check_sub"))

    bot.send_message(user_id, "❌ Вы не подписаны на все каналы! Подпишитесь и попробуйте снова.", reply_markup=markup, parse_mode="Markdown")

@bot.callback_query_handler(func=lambda call: call.data == "check_sub")
def check_subscription(call):
    user_id = call.from_user.id
    if is_subscribed(user_id):
        bot.send_message(user_id, "✅ Подписка обнаружена! Теперь выберите файл для скачивания.")
    else:
        send_subscription_request(user_id)

@bot.message_handler(content_types=["document", "video", "audio", "photo"])
def get_file_id(message):
    if message.document:
        file_id = message.document.file_id
    elif message.video:
        file_id = message.video.file_id
    elif message.audio:
        file_id = message.audio.file_id
    elif message.photo:
        file_id = message.photo[-1].file_id

    bot.send_message(message.chat.id, f"📎 File ID: `{file_id}`", parse_mode="Markdown")

@bot.callback_query_handler(func=lambda call: call.data == "back_main")
def back_to_main(call):
    send_welcome(call.message)

@bot.callback_query_handler(func=lambda call: call.data == "download_files")
def back_to_download(call):
    send_download_menu(call)

# Новый обработчик для кнопки Root
@bot.callback_query_handler(func=lambda call: call.data == "tutor_root")
def send_root_tutorial(call):
    user_id = call.from_user.id
    tutorial_text = """
    🚀 Установка Root, на разные девайсы.

Установка рут прав на Xiaomi - 
https://youtu.be/JT8Vyr8drpY?si=IgCTKJ7NFIgWSC2d

Установка рут прав на Samsung -
https://youtu.be/nL0nCvRnCtM?si=4d4OJffUsrbuB6UW

Установка рут прав на infinix -
https://youtu.be/3qZ-lG34_RE?si=awY0y83IhFVQkrbN

Установка рут прав на Realme - 
https://youtu.be/SV0JjAaxx68?si=ImwrfZuSc_luU1uS

Через тврп - 
https://youtu.be/sEvy6r5unpY?si=UgmcovIkIb--BYVM

❗Если вашего устройства нет в списке, то устанавливайте TWRP и ставьте рут через него

❗Если нужна помощь можете обратиться в [наш чат](https://t.me/+iAkSMGQw7J8yNzQ8)
    """
    bot.send_message(user_id, tutorial_text, parse_mode="Markdown")

bot.polling(none_stop=True)
