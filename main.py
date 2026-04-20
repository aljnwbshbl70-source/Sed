import telebot, requests, random, string, threading, time, os
from flask import Flask

# --- بيانات يامي الأساسية ---
TOKEN = "8600424985:AAGG-fIEuWBckryg_s8PiHD0UxFSbclQ8hA"
CHAT_ID = "7061804635"
SESSION_ID = "79626092435%3AN1K9h6O8Y7mZlE%3A22%3AAYf5b_rXoJtW8vC-QoP0UuI4_L9A-k"

bot = telebot.TeleBot(TOKEN)
app = Flask('')

@app.route('/')
def home(): return "YAMI 24/7 IS ACTIVE ✅"

@app.route('/ping')
def ping(): return "OK", 200

running = False
length = 4
total_checked = 0
start_time = time.time()

def check_insta(u):
    # استخدام الـ API الأقوى لضمان عدم الحظر
    url = f"https://www.instagram.com/api/v1/users/web_profile_info/?username={u}"
    headers = {
        "x-ig-app-id": "936619743392459",
        "cookie": f"sessionid={SESSION_ID}",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    }
    try:
        r = requests.get(url, headers=headers, timeout=10)
        if r.status_code == 404: return True
        return False
    except: return None

def hunt():
    global running, total_checked
    while running:
        u = ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(length))
        res = check_insta(u)
        if res is not None:
            total_checked += 1
            if res is True:
                bot.send_message(CHAT_ID, f"🎯 صيدة جديدة بواسطة يامي!\n🔗 اليوزر: @{u}\n⏱ الوقت: {time.strftime('%H:%M:%S')}")
                time.sleep(3)
        
        # يطمنك كل 500 محاولة (عشان ما يزعجك كثير وهو شغال 24 ساعة)
        if total_checked % 500 == 0:
            bot.send_message(CHAT_ID, f"👷‍♂️ يامي يواصل العمل.. تم فحص {total_checked} يوزر بنجاح.")
            
        time.sleep(0.5)

@bot.message_handler(commands=['start'])
def start(m):
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add("🚀 إطلاق يامي", "🛑 إيقاف", "⚙️ الطول")
    bot.send_message(m.chat.id, "🤖 أهلاً يا عمر، أنا يامي.\nسأقوم بالصيد لك 24 ساعة بدون توقف من السيرفر السحابي.", reply_markup=markup)

@bot.message_handler(func=lambda m: True)
def handle(m):
    global running, length
    if m.text == "🚀 إطلاق يامي":
        if not running:
            running = True
            threading.Thread(target=hunt, daemon=True).start()
            bot.reply_to(m, "✅ تم تفعيل وضع الصيد 24 ساعة. يمكنك إغلاق التلجرام الآن!")
    elif m.text == "🛑 إيقاف":
        running = False
        bot.reply_to(m, "🛑 تم إيقاف يامي.")
    elif m.text == "⚙️ الطول":
        msg = bot.reply_to(m, "أرسل الطول الجديد:")
        bot.register_next_step_handler(msg, update_l)

def update_l(m):
    global length
    try:
        length = int(m.text)
        bot.reply_to(m, f"⚙️ تم تحديث الهدف إلى يوزرات طول {length}")
    except: pass

if __name__ == "__main__":
    # تشغيل Flask في ثريد منفصل لضمان عمل UptimeRobot
    port = int(os.environ.get("PORT", 8080))
    threading.Thread(target=lambda: app.run(host='0.0.0.0', port=port, debug=False, use_reloader=False)).start()
    bot.infinity_polling()
    
