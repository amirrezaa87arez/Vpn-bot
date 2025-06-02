import telebot
from telebot import types

TOKEN = "7386747475:AAGzwWqBEBZApZSm-lPR0JJhX2FGvBEY6Sc"
bot = telebot.TeleBot(TOKEN)

ADMINS = [7935344235, 5993860770]

# متغیر برای ذخیره مرحله ارسال کانفیگ
admin_states = {}

@bot.message_handler(commands=["start"])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("💎 خرید اشتراک")
    btn2 = types.KeyboardButton("📚 آموزش اتصال")
    btn3 = types.KeyboardButton("🛠 پشتیبانی")
    markup.add(btn1, btn2, btn3)
    bot.send_message(message.chat.id, "سلام! به ربات خوش اومدی. از منو یکی رو انتخاب کن:", reply_markup=markup)

@bot.message_handler(func=lambda m: m.text == "💎 خرید اشتراک")
def buy_plan(message):
    markup = types.InlineKeyboardMarkup(row_width=1)
    plans = [
        ("1️⃣ پلن تک کاربره یک ماهه - 85 تومن", "plan1"),
        ("2️⃣ پلن دو کاربره یک ماهه - 115 تومن", "plan2"),
        ("3️⃣ پلن سه کاربره یک ماهه - 169 تومن", "plan3"),
        ("4️⃣ پلن تک کاربره دو ماهه - 140 تومن", "plan4"),
        ("5️⃣ پلن دو کاربره دو ماهه - 165 تومن", "plan5"),
        ("6️⃣ پلن سه کاربره دو ماهه - 185 تومن", "plan6"),
        ("7️⃣ پلن تک کاربره سه ماهه - 174 تومن", "plan7"),
        ("8️⃣ پلن دو کاربره سه ماهه - 234 تومن", "plan8"),
        ("9️⃣ پلن سه کاربره سه ماهه - 335 تومن", "plan9"),
    ]
    for plan_text, plan_data in plans:
        markup.add(types.InlineKeyboardButton(plan_text, callback_data=plan_data))
    bot.send_message(message.chat.id, "💎 لطفا یکی از پلن‌ها رو انتخاب کن:", reply_markup=markup)

@bot.message_handler(func=lambda m: m.text == "🛠 پشتیبانی")
def support(message):
    bot.send_message(message.chat.id, "🔹 برای پشتیبانی با آیدی زیر تماس بگیر:\n\n@Psycho_remix1")

@bot.message_handler(func=lambda m: m.text == "📚 آموزش اتصال")
def learn(message):
    bot.send_message(message.chat.id, "🌐 برای آموزش اتصال، به کانال زیر برو:\n\nhttps://t.me/amuzesh_dragonvpn")

@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    payment_text = (
        "💳 لطفاً مبلغ صورتحساب رو به شماره کارت زیر واریز کن:\n\n"
        "🔸 6277601368776066 بنام رضوانی\n\n"
        "✅ بعد از واریز، فیش واریزی رو ارسال کن تا ادمین بررسی کنه و کانفیگ رو بهت بده.\n\n"
        "🔴 لطفاً توجه داشته باش مبلغ صورتحساب رو به طور دقیق واریز کنی!"
    )
    bot.answer_callback_query(call.id, "✅ اطلاعات پرداخت رو ببین 👇")
    bot.send_message(call.message.chat.id, payment_text)

# وقتی کاربر فیش واریزی رو ارسال کرد
@bot.message_handler(content_types=["photo", "document"])
def handle_payment(message):
    bot.send_message(message.chat.id, "✅ فیش شما دریافت شد.\n🔎 لطفاً منتظر باشید تا ادمین بررسی کند.")

# پنل مدیریت
@bot.message_handler(commands=["admin"])
def admin_panel(message):
    if message.from_user.id in ADMINS:
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add(types.KeyboardButton("📤 ارسال کانفیگ"))
        bot.send_message(message.chat.id, "🔐 پنل مدیریت:", reply_markup=markup)
    else:
        bot.send_message(message.chat.id, "❌ شما ادمین نیستید.")

# مدیریت ارسال کانفیگ
@bot.message_handler(func=lambda m: m.text == "📤 ارسال کانفیگ" and m.from_user.id in ADMINS)
def send_config_step1(message):
    bot.send_message(message.chat.id, "🔹 لطفاً آیدی عددی کاربر رو بفرست:")
    admin_states[message.from_user.id] = "waiting_user_id"

@bot.message_handler(func=lambda m: admin_states.get(m.from_user.id) == "waiting_user_id")
def send_config_step2(message):
    try:
        user_id = int(message.text.strip())
        admin_states[message.from_user.id] = ("waiting_config", user_id)
        bot.send_message(message.chat.id, "📝 حالا متن یا کانفیگ رو بفرست تا برای کاربر ارسال بشه.")
    except ValueError:
        bot.send_message(message.chat.id, "❌ آیدی عددی معتبر نیست. دوباره تلاش کن.")

@bot.message_handler(func=lambda m: isinstance(admin_states.get(m.from_user.id), tuple) and admin_states.get(m.from_user.id)[0] == "waiting_config")
def send_config_step3(message):
    _, user_id = admin_states.pop(message.from_user.id)
    bot.send_message(user_id, f"📥 پیام یا کانفیگ جدید:\n\n{message.text}")
    bot.send_message(message.chat.id, "✅ کانفیگ با موفقیت برای کاربر ارسال شد.")

if __name__ == "__main__":
    print("💥 ربات با موفقیت اجرا شد!")
    bot.infinity_polling()
