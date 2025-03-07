import json
import os

DATA_FILE = "referrals.json"

# Функция загрузки данных
def load_data():
    if not os.path.exists(DATA_FILE):
        return {}
    with open(DATA_FILE, "r", encoding="utf-8") as file:
        try:
            return json.load(file)
        except json.JSONDecodeError:
            return {}  # Если файл пустой или битый, вернуть пустой словарь

# Функция сохранения данных
def save_data(data):
    with open(DATA_FILE, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4, ensure_ascii=False)

# Функция обработки реферала
def handle_referral(user_id, command_text):
    data = load_data()
    
    user_id = str(user_id)  # Приводим к строке для JSON

    if user_id not in data or not isinstance(data[user_id], dict):
        data[user_id] = {"referrer": None, "referrals": 0}

    if command_text.startswith("/start "):
        referrer_id = command_text.split()[1]

        # Проверяем, что ID валидный и не равен самому пользователю
        if referrer_id.isdigit() and referrer_id != user_id:
            referrer_id = str(referrer_id)  

            # Если у пользователя ещё нет реферера, назначаем его
            if data[user_id]["referrer"] is None:
                data[user_id]["referrer"] = referrer_id

                # Добавляем реферала к рефереру
                if referrer_id in data and isinstance(data[referrer_id], dict):
                    data[referrer_id]["referrals"] += 1
                else:
                    data[referrer_id] = {"referrer": None, "referrals": 1}

    save_data(data)
    return data[user_id].get("referrer")  # Безопасный доступ к полю

# Функция получения количества приглашённых
def get_user_referrals(user_id):
    data = load_data()
    return data.get(str(user_id), {}).get("referrals", 0)

