
import telebot
from telebot import types
import json
import os

TOKEN = os.environ.get("BOT_TOKEN")
ADMIN_IDS = os.environ.get("ADMIN_IDS", "").split(",")

bot = telebot.TeleBot(TOKEN)
USERS_FILE = 'users.json'
pending_configs = {}

def load_users():
    if not os.path.exists(USERS_FILE):
        with open(USERS_FILE, 'w') as f:
            json.dump({}, f)
    with open(USERS_FILE, 'r') as f:
        return json.load(f)

def save_users(users):
    with open(USERS_FILE, 'w') as f:
        json.dump(users, f)

def get_or_create_user_id(telegram_id):
    users = load_users()
    for uid, tid in users.items():
        if tid == telegram_id:
            return uid
    new_id = str(1000 + len(users) + 1)
    users[new_id] = telegram_id
    save_users(users)
    return new_id

def main_menu(is_admin=False):
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
    kb.row("خرید اشتراک 💳", "آموزش اتصال 📘")
    if is_admin:
        kb.row("📤 ارسال کانفیگ")
    return kb

plans_text = """💳 لیست پلن‌ها:

1️⃣ پلن تک کاربره نامحدود یک ماهه - 85 تومن
2️⃣ پلن دو کاربره نامحدود یک ماهه - 115 تومن
3️⃣ پلن سه کاربره نامحدود یک ماهه - 169 تومن

4️⃣ پلن تک کاربره نامحدود دو ماهه - 140 تومن
5️⃣ پلن دو کاربره نامحدود دو ماهه - 165 تومن
6️⃣ پلن سه کاربره نامحدود دو ماهه - 185 تومن

7️⃣ پلن تک کاربره نامحدود سه ماهه - 174 تومن
8️⃣ پلن دو کاربره نامحدود سه ماهه - 234 تومن
9️⃣ پلن سه کاربره نامحدود سه ماهه - 335 تومن"""

@bot.message_handler(commands=['start'])
def handle_start(message):
    user_id = get_or_create_user_id(message.from_user.id)
    is_admin = str(message.from_user.id) in ADMIN_IDS
    bot.send_message(
        message.chat.id,
        f"🌟 خوش آمدید! آیدی عددی شما: {user_id}",
        reply_markup=main_menu(is_admin)
    )

@bot.message_handler(func=lambda m: m.text == "آموزش اتصال 📘")
def handle_amoozesh(message):
    bot.send_message(message.chat.id, "📘 آموزش اتصال: https://t.me/amuzesh_dragonvpn")

@bot.message_handler(func=lambda m: m.text == "خرید اشتراک 💳")
def handle_buy(message):
    bot.send_message(message.chat.id, plans_text)

@bot.message_handler(func=lambda m: m.text == "📤 ارسال کانفیگ")
def start_send_config(message):
    if str(message.from_user.id) not in ADMIN_IDS:
        bot.send_message(message.chat.id, "⛔️ شما دسترسی ندارید.")
        return
    bot.send_message(message.chat.id, "🆔 آیدی عددی کاربر را وارد کنید:")
    bot.register_next_step_handler(message, get_config_text)

def get_config_text(message):
    target_id = message.text.strip()
    users = load_users()
    if target_id not in users:
        bot.send_message(message.chat.id, "❌ آیدی عددی نامعتبر است.")
        return
    pending_configs[message.chat.id] = target_id
    bot.send_message(message.chat.id, "✉️ پیام یا کانفیگ موردنظر را ارسال کنید:")
    bot.register_next_step_handler(message, send_config_to_user)

def send_config_to_user(message):
    target_numeric = pending_configs.get(message.chat.id)
    users = load_users()
    if not target_numeric or target_numeric not in users:
        bot.send_message(message.chat.id, "❌ مشکلی پیش آمده.")
        return
    telegram_id = users[target_numeric]
    bot.send_message(telegram_id, f"🔑 کانفیگ شما: {message.text}")
    bot.send_message(message.chat.id, "✅ پیام با موفقیت ارسال شد.")

@bot.message_handler(content_types=['photo', 'document'])
def handle_receipt(message):
    user_id = get_or_create_user_id(message.from_user.id)
    bot.reply_to(message, "🕐 فیش شما دریافت شد. لطفاً چند لحظه صبر کنید تا بررسی و تایید شود.")
    caption = f"🧾 کاربر با آیدی عددی {user_id} یک فیش ارسال کرد."
    for admin_id in ADMIN_IDS:
        if message.content_type == 'photo':
            bot.send_photo(admin_id, message.photo[-1].file_id, caption=caption)
        elif message.content_type == 'document':
            bot.send_document(admin_id, message.document.file_id, caption=caption)

bot.remove_webhook()
bot.infinity_polling()
