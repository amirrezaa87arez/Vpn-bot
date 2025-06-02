import telebot
from telebot import types
import os

# مقداردهی اولیه ربات از محیط (Render)
BOT_TOKEN = os.getenv("BOT_TOKEN")
bot = telebot.TeleBot(BOT_TOKEN)

# آیدی مدیران اصلی
MAIN_ADMINS = [7935344235, 5993860770]

# آیدی ادمین‌های اضافه‌شده
def load_admins():
    if os.path.exists("admins.txt"):
        with open("admins.txt", "r") as f:
            return [int(line.strip()) for line in f]
    else:
        return []

def save_admin(admin_id):
    with open("admins.txt", "a") as f:
        f.write(f"{admin_id}\n")

# چک کردن دسترسی
def is_admin(user_id):
    return user_id in MAIN_ADMINS or user_id in load_admins()

# منوی اصلی کاربر
def user_menu():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add("🛒 خرید اشتراک", "🎓 آموزش اتصال", "🆘 پشتیبانی")
    return markup

# منوی مدیریت
def admin_menu(user_id):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add("📤 ارسال کانفیگ", "💲 ویرایش پلن‌ها")
    markup.add("💳 ویرایش شماره کارت")
    if user_id in MAIN_ADMINS:
        markup.add("➕ اضافه کردن ادمین")
    markup.add("🔙 بازگشت")
    return markup

# شروع ربات
@bot.message_handler(commands=["start"])
def start_bot(message):
    user_id = message.from_user.id
    if is_admin(user_id):
        bot.send_message(user_id, "🔐 به پنل مدیریت خوش اومدی!", reply_markup=admin_menu(user_id))
    else:
        bot.send_message(user_id, "👋 به ربات خوش اومدی!\n\nیکی از گزینه‌ها رو انتخاب کن:", reply_markup=user_menu())

# هندل کلیدهای عمومی کاربر
@bot.message_handler(func=lambda m: m.text in ["🛒 خرید اشتراک", "🎓 آموزش اتصال", "🆘 پشتیبانی"])
def handle_user_buttons(message):
    if message.text == "🛒 خرید اشتراک":
        with open("plans.txt", "r", encoding="utf-8") as f:
            plans = f.read()
        msg = f"💰 پلن‌های موجود:\n\n{plans}\n\n🔴 لطفاً مبلغ را به شماره کارت زیر واریز کنید:\n6277601368776066 به نام رضوانی\n\n📸 سپس فیش واریزی را ارسال کنید تا ادمین بررسی و کانفیگ را ارسال کند.\n\n⚠️ توجه: مبلغ را دقیق واریز کنید."
        bot.send_message(message.chat.id, msg)
    elif message.text == "🎓 آموزش اتصال":
        bot.send_message(message.chat.id, "📢 آموزش اتصال در این کانال:\nhttps://t.me/amuzesh_dragonvpn")
    elif message.text == "🆘 پشتیبانی":
        bot.send_message(message.chat.id, "🆘 ارتباط با پشتیبانی:\n@Psycho_remix1")

# مدیریت برگشت به منو
@bot.message_handler(func=lambda m: m.text == "🔙 بازگشت")
def back_to_menu(message):
    user_id = message.from_user.id
    if is_admin(user_id):
        bot.send_message(user_id, "🔙 بازگشت به پنل مدیریت:", reply_markup=admin_menu(user_id))
    else:
        bot.send_message(user_id, "🔙 بازگشت به منو:", reply_markup=user_menu())

# 📤 ارسال کانفیگ
@bot.message_handler(func=lambda m: m.text == "📤 ارسال کانفیگ")
def send_config(message):
    user_id = message.from_user.id
    if is_admin(user_id):
        msg = bot.send_message(user_id, "🔍 آیدی عددی کاربر رو وارد کن:")
        bot.register_next_step_handler(msg, get_user_id_for_config)

def get_user_id_for_config(message):
    user_id_to_send = int(message.text)
    msg = bot.send_message(message.chat.id, "📦 حالا متن یا کانفیگ رو بفرست:")
    bot.register_next_step_handler(msg, lambda m: send_config_to_user(m, user_id_to_send))

def send_config_to_user(message, user_id_to_send):
    try:
        bot.send_message(user_id_to_send, f"📦 کانفیگ دریافتی:\n\n{message.text}")
        bot.send_message(message.chat.id, "✅ کانفیگ با موفقیت ارسال شد.")
    except Exception as e:
        bot.send_message(message.chat.id, f"❌ خطا: {e}")

# 💲 ویرایش پلن‌ها
@bot.message_handler(func=lambda m: m.text == "💲 ویرایش پلن‌ها")
def edit_plans(message):
    if is_admin(message.from_user.id):
        msg = bot.send_message(message.chat.id, "📝 پلن‌های جدید رو وارد کن:")
        bot.register_next_step_handler(msg, save_plans)

def save_plans(message):
    with open("plans.txt", "w", encoding="utf-8") as f:
        f.write(message.text)
    bot.send_message(message.chat.id, "✅ پلن‌ها به‌روزرسانی شدند.")

# 💳 ویرایش شماره کارت
@bot.message_handler(func=lambda m: m.text == "💳 ویرایش شماره کارت")
def edit_card(message):
    if is_admin(message.from_user.id):
        msg = bot.send_message(message.chat.id, "💳 شماره کارت جدید رو وارد کن:")
        bot.register_next_step_handler(msg, save_card)

def save_card(message):
    with open("card.txt", "w", encoding="utf-8") as f:
        f.write(message.text)
    bot.send_message(message.chat.id, "✅ شماره کارت به‌روزرسانی شد.")

# ➕ اضافه کردن ادمین (فقط مدیران اصلی)
@bot.message_handler(func=lambda m: m.text == "➕ اضافه کردن ادمین")
def add_admin(message):
    if message.from_user.id in MAIN_ADMINS:
        msg = bot.send_message(message.chat.id, "🆕 آیدی عددی ادمین جدید رو وارد کن:")
        bot.register_next_step_handler(msg, save_new_admin)

def save_new_admin(message):
    new_admin_id = int(message.text)
    save_admin(new_admin_id)
    bot.send_message(message.chat.id, f"✅ ادمین جدید {new_admin_id} اضافه شد.")

# راه‌اندازی ربات
bot.infinity_polling()
