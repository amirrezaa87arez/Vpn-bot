import telebot
from telebot import types

# 🔥 توکن جدید!
TOKEN = "7386747475:AAGzwWqBEBZApZSm-lPR0JJhX2FGvBEY6Sc"
bot = telebot.TeleBot(TOKEN)

# 🔥 لیست آیدی ادمین‌ها
ADMINS = [7935344235, 5993860770]

# شروع
@bot.message_handler(commands=["start"])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("💎 خرید اشتراک")
    btn2 = types.KeyboardButton("🛠 پشتیبانی")
    markup.add(btn1, btn2)
    bot.send_message(message.chat.id, "سلام! به ربات خوش اومدی. دکمه مورد نظر رو انتخاب کن:", reply_markup=markup)

# خرید اشتراک
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

# پشتیبانی
@bot.message_handler(func=lambda m: m.text == "🛠 پشتیبانی")
def support(message):
    support_text = "برای پشتیبانی با آیدی زیر در تماس باش:\n\n@Psycho_remix1"
    bot.send_message(message.chat.id, support_text)

# کال‌بک پلن‌ها
@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    bot.answer_callback_query(call.id, "✅ برای خرید با آیدی پشتیبانی تماس بگیر: @Psycho_remix1")
    bot.send_message(call.message.chat.id, f"🔹 شما پلن {call.data} رو انتخاب کردی.\n\n🔸 برای خرید، به پشتیبانی پیام بده:\n@Psycho_remix1")

# اجرای بات
if __name__ == "__main__":
    print("ربات در حال اجراست...")
    bot.infinity_polling()
