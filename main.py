import telebot, requests, random, string, threading, time
from flask import Flask

# --- بياناتك ---
TOKEN = "8600424985:AAGG-fIEuWBckryg_s8PiHD0UxFSbclQ8hA"
CHAT_ID = "7061804635"
bot = telebot.TeleBot(TOKEN)
app = Flask('')

@app.route('/')
def home(): return "SNO SERVER IS ONLINE ✅"

running = False
length = 5

def check_insta(u):
    url = f"https://www.instagram.com/{u}/"
    try:
        r = requests.get(url, headers={"User-Agent": "Mozilla/5.0"}, timeout=3)
        if "Page Not Found" in r.text or r.status_code == 404:
            return True
        return False
    except: return False

def hunt():
    while running:
        u = ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(length))
        if check_insta(u):
            bot.send_message(CHAT_ID, f"🎯 صيدة من السيرفر: @{u}")
            time.sleep(1)
        time.sleep(0.05) # سرعة عالية جداً

@bot.message_handler(commands=['start'])
def start(m):
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add("🚀 بدء الصيد", "🛑 إيقاف", "⚙️ تغيير الطول")
    bot.send_message(m.chat.id, "SNO SERVER V3 🇸🇦\nالبوت شغال الآن من السيرفر السحابي:", reply_markup=markup)

@bot.message_handler(func=lambda m: True)
def handle(m):
    global running, length
    if m.text == "🚀 بدء الصيد":
        if not running:
            running = True
            threading.Thread(target=hunt, daemon=True).start()
            bot.reply_to(m, "انطلق الصاروخ! البوت يصيد الآن 🚀")
    elif m.text == "🛑 إيقاف":
        running = False
        bot.reply_to(m, "تم إيقاف المحركات 🛑")
    elif m.text == "⚙️ تغيير الطول":
        msg = bot.send_message(m.chat.id, "أرسل الطول الجديد:")
        bot.register_next_step_handler(msg, update_l)

def update_l(m):
    global length
    try:
        length = int(m.text)
        bot.reply_to(m, f"تم التغيير لـ {length}")
    except: bot.reply_to(m, "أرسل رقم!")

def run_web():
    app.run(host='0.0.0.0', port=8080)

if __name__ == "__main__":
    threading.Thread(target=run_web).start()
    bot.infinity_polling()
