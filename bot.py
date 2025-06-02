import telebot
from telebot import types
import threading
import time

# 🟡 توکن ربات
TOKEN = "توکن خودت"

# 🟡 آیدی مدیر
ADMIN_ID = 123456789  # جایگزین کن!

bot = telebot.TeleBot(TOKEN)

# ▶️ تابع شروع ربات
def start_bot():
    bot.infinity_polling()

# ▶️ منوی اصلی
def send_main_menu(message):
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add(types.KeyboardButton("💳 خرید اشتراک 💳"))
    kb.add(types.KeyboardButton("💡 راهنما"), types.KeyboardButton("🛠 پشتیبانی"))
    bot.send_message(message.chat.id, "🔷 به منوی اصلی خوش اومدی! یکی از گزینه‌ها رو انتخاب کن:", reply_markup=kb)

# ▶️ استارت
@bot.message_handler(commands=['start'])
def handle_start(message):
    send_main_menu(message)

# ▶️ دکمه خرید اشتراک با پلن‌های دکمه‌ای
@bot.message_handler(func=lambda m: m.text == "💳 خرید اشتراک 💳")
def handle_buy(message):
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    
    kb.add(types.KeyboardButton("1️⃣ پلن تک کاربره نامحدود ۱ ماهه - 85T"))
    kb.add(types.KeyboardButton("2️⃣ پلن دو کاربره نامحدود ۱ ماهه - 115T"))
    kb.add(types.KeyboardButton("3️⃣ پلن سه کاربره نامحدود ۱ ماهه - 169T"))

    kb.add(types.KeyboardButton("4️⃣ پلن تک کاربره نامحدود ۲ ماهه - 140T"))
    kb.add(types.KeyboardButton("5️⃣ پلن دو کاربره نامحدود ۲ ماهه - 165T"))
    kb.add(types.KeyboardButton("6️⃣ پلن سه کاربره نامحدود ۲ ماهه - 185T"))

    kb.add(types.KeyboardButton("7️⃣ پلن تک کاربره نامحدود ۳ ماهه - 174T"))
    kb.add(types.KeyboardButton("8️⃣ پلن دو کاربره نامحدود ۳ ماهه - 234T"))
    kb.add(types.KeyboardButton("9️⃣ پلن سه کاربره نامحدود ۳ ماهه - 335T"))

    kb.add(types.KeyboardButton("🔙 بازگشت به منو"))

    bot.send_message(message.chat.id, "💳 یکی از پلن‌های زیر رو انتخاب کن:", reply_markup=kb)

# ▶️ دکمه راهنما
@bot.message_handler(func=lambda m: m.text == "💡 راهنما")
def handle_help(message):
    help_text = "📌 راهنمای استفاده:\n" \
                "1️⃣ یکی از پلن‌ها رو انتخاب کن.\n" \
                "2️⃣ مبلغ رو پرداخت کن.\n" \
                "3️⃣ رسید رو به پشتیبانی بفرست!"
    bot.send_message(message.chat.id, help_text)

# ▶️ دکمه پشتیبانی
@bot.message_handler(func=lambda m: m.text == "🛠 پشتیبانی")
def handle_support(message):
    support_text = "🛠 برای پشتیبانی به آیدی زیر پیام بده:\n" \
                   f"👉 @username (یا لینک دلخواهت)"
    bot.send_message(message.chat.id, support_text)

# ▶️ دکمه بازگشت به منو
@bot.message_handler(func=lambda m: m.text == "🔙 بازگشت به منو")
def handle_back(message):
    send_main_menu(message)

# ▶️ گرفتن هر متنی که جزو دکمه‌ها نیست
@bot.message_handler(func=lambda m: True)
def handle_other(message):
    bot.send_message(message.chat.id, "❌ این گزینه موجود نیست. از منو استفاده کن!")

# ▶️ اجرای ربات در ترد جداگانه
if __name__ == "__main__":
    t = threading.Thread(target=start_bot)
    t.start()
