import telebot
from telebot import types
import os

# مقداردهی اولیه ربات از محیط (Render)
BOT_TOKEN = os.getenv("BOT_TOKEN")
bot = telebot.TeleBot(BOT_TOKEN)

# آیدی مدیران اصلی
MAIN_ADMINS = [7935344235, 5993860770]

# مسیر فایل‌ها
PLANS_FILE = "plans.txt"
CARD_FILE = "card.txt"
ADMINS_FILE = "admins.txt"

# بررسی و ایجاد فایل‌های ضروری
def check_and_create_files():
    if not os.path.exists(PLANS_FILE):
        with open(PLANS_FILE, "w", encoding="utf-8") as f:
            f.write("1️⃣ پلن تک کاربره نامحدود یک ماهه - 85 تومن\n2️⃣ پلن دو کاربره نامحدود یک ماهه - 115 تومن\n3️⃣ پلن سه کاربره نامحدود یک ماهه - 169 تومن\n\n🔴 برای تغییر پلن‌ها از پنل مدیریت استفاده کنید.")
    if not os.path.exists(CARD_FILE):
        with open(CARD_FILE, "w", encoding="utf-8") as f:
            f.write("6277601368776066 به نام رضوانی")
    if not os.path.exists(ADMINS_FILE):
        with open(ADMINS_FILE, "w", encoding="utf-8") as f:
            pass

check_and_create_files()

# آیدی ادمین‌های اضافه‌شده
def load_admins():
    with open(ADMINS_FILE, "r") as f:
        return [int(line.strip()) for line in f if line.strip()]

def save_admin(admin_id):
    with open(ADMINS_FILE, "a") as f:
        f.write(f"{admin_id}\n")

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

# شروع
@bot.message_handler(commands=["start"])
def start_bot(message):
    user_id = message.from_user.id
    if is_admin(user_id):
        bot.send_message(user_id, "🔐 به پنل مدیریت خوش اومدی!", reply_markup=admin_menu(user_id))
    else:
        bot.send_message(user_id, "👋 به ربات خوش اومدی!\n\nیکی از گزینه‌ها رو انتخاب کن:", reply_markup=user_menu())

# خرید اشتراک
@bot.message_handler(func=lambda m: m.text == "🛒 خرید اشتراک")
def buy_subscription(message):
    with open(PLANS_FILE, "r", encoding="utf-8") as f:
        plans = f.read()
    with open(CARD_FILE, "r", encoding="utf-8") as f:
        card = f.read()
    msg = f"💰 پلن‌های موجود:\n\n{plans}\n\n🔴 لطفاً مبلغ را به شماره کارت زیر واریز کنید:\n{card}\n\n📸 سپس فیش واریزی را ارسال کنید تا ادمین بررسی و کانفیگ را ارسال کند.\n\n⚠️ توجه: مبلغ را دقیق واریز کنید."
    bot.send_message(message.chat.id, msg)

# بقیه بخش‌ها مثل قبل...
@bot.message_handler(func=lambda m: m.text == "🎓 آموزش اتصال")
def show_guide(message):
    bot.send_message(message.chat.id, "📢 آموزش اتصال در این کانال:\nhttps://t.me/amuzesh_dragonvpn")

@bot.message_handler(func=lambda m: m.text == "🆘 پشتیبانی")
def support(message):
    bot.send_message(message.chat.id, "🆘 ارتباط با پشتیبانی:\n@Psycho_remix1")

@bot.message_handler(func=lambda m: m.text == "🔙 بازگشت")
def back(message):
    user_id = message.from_user.id
    if is_admin(user_id):
        bot.send_message(user_id, "🔙 بازگشت به پنل مدیریت:", reply_markup=admin_menu(user_id))
    else:
        bot.send_message(user_id, "🔙 بازگشت به منو:", reply_markup=user_menu())

@bot.message_handler(func=lambda m: m.text == "📤 ارسال کانفیگ")
def send_config(message):
    if is_admin(message.from_user.id):
        msg = bot.send_message(message.chat.id, "🔍 آیدی عددی کاربر رو وارد کن:")
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

@bot.message_handler(func=lambda m: m.text == "💲 ویرایش پلن‌ها")
def edit_plans(message):
    if is_admin(message.from_user.id):
        msg = bot.send_message(message.chat.id, "📝 پلن‌های جدید رو وارد کن:")
        bot.register_next_step_handler(msg, save_plans)

def save_plans(message):
    with open(PLANS_FILE, "w", encoding="utf-8") as f:
        f.write(message.text)
    bot.send_message(message.chat.id, "✅ پلن‌ها به‌روزرسانی شدند.")

@bot.message_handler(func=lambda m: m.text == "💳 ویرایش شماره کارت")
def edit_card(message):
    if is_admin(message.from_user.id):
        msg = bot.send_message(message.chat.id, "💳 شماره کارت جدید رو وارد کن:")
        bot.register_next_step_handler(msg, save_card)

def save_card(message):
    with open(CARD_FILE, "w", encoding="utf-8") as f:
        f.write(message.text)
    bot.send_message(message.chat.id, "✅ شماره کارت به‌روزرسانی شد.")

@bot.message_handler(func=lambda m: m.text == "➕ اضافه کردن ادمین")
def add_admin(message):
    if message.from_user.id in MAIN_ADMINS:
        msg = bot.send_message(message.chat.id, "🆕 آیدی عددی ادمین جدید رو وارد کن:")
        bot.register_next_step_handler(msg, save_new_admin)

def save_new_admin(message):
    new_admin_id = int(message.text)
    save_admin(new_admin_id)
    bot.send_message(message.chat.id, f"✅ ادمین جدید {new_admin_id} اضافه شد.")

bot.infinity_polling()
