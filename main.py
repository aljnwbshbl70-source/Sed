import telebot, requests, random, string, threading, time, os
from flask import Flask

# --- البيانات ---
TOKEN = "8600424985:AAGG-fIEuWBckryg_s8PiHD0UxFSbclQ8hA"
CHAT_ID = "7061804635"

bot = telebot.TeleBot(TOKEN)
app = Flask('')

@app.route('/')
def home(): return "YAMI IS ALIVE 24/7 🔥"

@app.route('/ping')
def ping(): return "OK", 200

running = False
length = 4

def check_insta(u):
    # فحص عن طريق ثغرة الـ "Query" - أسرع وأضمن
    url = f"https://www.instagram.com/{u}/?__a=1&__d=1"
    headers = {
        "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Mobile/15E148 Safari/604.1",
        "X-IG-App-ID": "936619743392459"
    }
    try:
        r = requests.get(url, headers=headers, timeout=8)
        # إذا رجع 404 أو صفحة فاضية يعني متاح
        if r.status_code == 404:
            return True
        return False
    except:
        return False

def hunt():
    global running
    # رسالة تأكيد أول ما يضغط زر البدء
    bot.send_message(CHAT_ID, "🚀 بدأ يامي في الجلد.. سأرسل لك فوراً عند وجود صيدة.")
    while running:
        u = ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(length))
        if check_insta(u):
            bot.send_message(CHAT_ID, f"🎯 يامي جاب صيدة!\n🔗: @{u}")
            time.sleep(10) # ننتظر شوي عشان ما ننحظر
        time.sleep(0.4)

@bot.message_handler(commands=['start'])
def start(m):
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add("🚀 إطلاق يامي", "🛑 إيقاف", "⚙️ الطول")
    bot.send_message(m.chat.id, "🤖 يامي في وضع القوة القصوى!\nالسيرفر شغال 24 ساعة.", reply_markup=markup)

@bot.message_handler(func=lambda m: True)
def handle(m):
    global running, length
    if m.text == "🚀 إطلاق يامي":
        if not running:
            running = True
            threading.Thread(target=hunt, daemon=True).start()
            bot.reply_to(m, "انطلق يامي! ⚡")
    elif m.text == "🛑 إيقاف":
        running = False
        bot.reply_to(m, "توقفنا 🛑")
    elif m.text == "⚙️ الطول":
        msg = bot.send_message(m.chat.id, "أرسل الطول الجديد (مثلاً 5):")
        bot.register_next_step_handler(msg, update_l)

def update_l(m):
    global length
    try:
        length = int(m.text)
        bot.reply_to(m, f"تم تغيير الطول لـ {length}")
    except: pass

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    threading.Thread(target=lambda: app.run(host='0.0.0.0', port=port)).start()
    bot.infinity_polling()
    
