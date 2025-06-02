import telebot
from telebot import types
import json
import os

BOT_TOKEN = os.environ.get("BOT_TOKEN")
bot = telebot.TeleBot(BOT_TOKEN)

ADMIN_IDS = ["7935344235", "5993860770"]

USERS_FILE = "users.json"

def load_users():
    if not os.path.exists(USERS_FILE):
        return {}
    with open(USERS_FILE, "r") as f:
        return json.load(f)

def save_users(users):
    with open(USERS_FILE, "w") as f:
        json.dump(users, f)

def add_user(user_id):
    users = load_users()
    if str(user_id) not in users.values():
        new_id = str(max([int(k) for k in users.keys()], default=1000) + 1)
        users[new_id] = user_id
        save_users(users)

def main_menu(is_admin=False):
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
    kb.row("خرید اشتراک 💳", "آموزش اتصال 📘")
    if is_admin:
        kb.row("📤 ارسال کانفیگ")
    kb.row("🆘 پشتیبانی")  # دکمه جدید پشتیبانی
    return kb

@bot.message_handler(commands=["start"])
def start(message):
    user_id = message.from_user.id
    add_user(user_id)
    is_admin = str(user_id) in ADMIN_IDS
    bot.send_message(
        message.chat.id,
        "سلام! به ربات خوش اومدی 😊\n\nاز منو استفاده کن 👇",
        reply_markup=main_menu(is_admin)
    )

@bot.message_handler(func=lambda m: m.text == "🆘 پشتیبانی")
def handle_support(message):
    bot.send_message(
        message.chat.id,
        "💬 برای پشتیبانی با ادمین تماس بگیرید:\n@korosh_dev"
    )

@bot.message_handler(func=lambda m: m.text == "خرید اشتراک 💳")
def handle_buy(message):
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
    kb.row("پلن ۱️⃣ (۱ ماهه - 85T)", "پلن ۲️⃣ (۲ ماهه - 140T)")
    kb.row("پلن ۳️⃣ (۳ ماهه - 174T)")
    kb.row("🔙 بازگشت به منو")
    bot.send_message(message.chat.id, "💳 یکی از پلن‌های زیر رو انتخاب کن:", reply_markup=kb)

@bot.message_handler(func=lambda m: m.text.startswith("پلن"))
def handle_plan_choice(message):
    bot.send_message(
        message.chat.id,
        f"✅ انتخاب شما: {message.text}\n\n💳 لطفاً مبلغ رو به کارت زیر واریز کنید:\n\n💳 کارت: 6037997512345678\n💬 بعد از واریز، فیش رو بفرستید."
    )

@bot.message_handler(func=lambda m: m.text == "🔙 بازگشت به منو")
def back_to_menu(message):
    is_admin = str(message.from_user.id) in ADMIN_IDS
    bot.send_message(message.chat.id, "🔙 بازگشت به منو", reply_markup=main_menu(is_admin))

@bot.message_handler(func=lambda m: m.text == "آموزش اتصال 📘")
def send_instructions(message):
    bot.send_message(
        message.chat.id,
        "📘 آموزش اتصال:\n1️⃣ دانلود اپلیکیشن\n2️⃣ وارد کردن کانفیگ\n3️⃣ اتصال به سرور\n\n👀 مشکلی داشتی، به پشتیبانی پیام بده."
    )

@bot.message_handler(func=lambda m: m.text == "📤 ارسال کانفیگ")
def send_config(message):
    if str(message.from_user.id) not in ADMIN_IDS:
        bot.send_message(message.chat.id, "❌ فقط ادمین به این بخش دسترسی داره!")
        return

    msg = bot.send_message(message.chat.id, "🔗 کانفیگ رو بفرست:")
    bot.register_next_step_handler(msg, handle_config)

def handle_config(message):
    config_text = message.text
    users = load_users()
    for uid in users.values():
        bot.send_message(uid, f"🔗 کانفیگ جدید:\n\n{config_text}")
    bot.send_message(message.chat.id, "✅ کانفیگ برای همه کاربرها ارسال شد!")

def main():
    bot.infinity_polling()

if __name__ == "__main__":
    main()
