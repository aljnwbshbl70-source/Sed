import telebot, requests, random, string, threading, time, os
from flask import Flask

# --- بيانات يامي ---
TOKEN = "8600424985:AAGG-fIEuWBckryg_s8PiHD0UxFSbclQ8hA"
CHAT_ID = "7061804635"
SESSION_ID = "79626092435%3AN1K9h6O8Y7mZlE%3A22%3AAYf5b_rXoJtW8vC-QoP0UuI4_L9A-k"

bot = telebot.TeleBot(TOKEN)
app = Flask('')

@app.route('/')
def home(): 
    return "YAMI SERVER IS ALIVE ⚡"

@app.route('/ping')
def ping():
    return "OK", 200

running = False
length = 4

def check_insta(u):
    url = f"https://www.instagram.com/{u}/?__a=1&__d=dis"
    headers = {
        "cookie": f"sessionid={SESSION_ID}",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    }
    try:
        r = requests.get(url, headers=headers, timeout=10)
        if r.status_code == 404:
            return True
        return False
    except: return False

def hunt():
    while running:
        u = ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(length))
        if check_insta(u):
            bot.send_message(CHAT_ID, f"🎯 يامي جاب لك صيدة:\n🔗: @{u}")
            time.sleep(5) # زيادة الوقت شوي عشان ريندر ما يحظرك
        time.sleep(0.5)

@bot.message_handler(commands=['start'])
def start(m):
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add("🚀 إطلاق يامي", "🛑 إيقاف يامي", "⚙️ الطول")
    bot.send_message(m.chat.id, "🤖 أهلاً بك، أنا البوت يامي (Yami)\nشغال الآن على سيرفر Render 🚀", reply_markup=markup)

@bot.message_handler(func=lambda m: True)
def handle(m):
    global running, length
    if m.text == "🚀 إطلاق يامي":
        if not running:
            running = True
            threading.Thread(target=hunt, daemon=True).start()
            bot.reply_to(m, "تم إطلاق يامي في فضاء الإنستجرام.. 🚀")
    elif m.text == "🛑 إيقاف يامي":
        running = False
        bot.reply_to(m, "تم سحب يامي للقاعدة 🛑")
    elif m.text == "⚙️ الطول":
        msg = bot.send_message(m.chat.id, "أرسل الطول الجديد:")
        bot.register_next_step_handler(msg, update_l)

def update_l(m):
    global length
    try:
        length = int(m.text)
        bot.reply_to(m, f"تم التغيير لـ {length} بواسطة يامي ✅")
    except: bot.reply_to(m, "أرسل رقم!")

def run_web():
    # Render يطلب منك استخدام البورت اللي هو يحدده
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)

if __name__ == "__main__":
    threading.Thread(target=run_web).start()
    bot.infinity_polling()
    
