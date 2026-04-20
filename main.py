import telebot, requests, random, string, threading, time, os
from flask import Flask

TOKEN = "8600424985:AAGG-fIEuWBckryg_s8PiHD0UxFSbclQ8hA"
CHAT_ID = "7061804635"

bot = telebot.TeleBot(TOKEN)
app = Flask('')

@app.route('/')
def home(): return "YAMI EMERGENCY MODE: ON ✅"

@app.route('/ping')
def ping(): return "OK", 200

running = False
length = 4

def check_insta(u):
    # طريقة فحص عبر رابط الصور (سريعة جداً ولا تحتاج سشن)
    url = f"https://www.instagram.com/{u}/"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
    }
    try:
        r = requests.get(url, headers=headers, timeout=5)
        # إذا الصفحة مو موجودة (404) يعني اليوزر متاح
        if r.status_code == 404:
            return True
        return False
    except:
        return None

def hunt():
    global running
    while running:
        u = ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(length))
        if check_insta(u):
            bot.send_message(CHAT_ID, f"🎯 صيدة جديدة من يامي!\n🔗 اليوزر: @{u}")
            time.sleep(5)
        
        # رسالة تأكيد كل 30 ثانية إن البوت مازال "يتنفس"
        # لو ما جتك هذي الرسالة، يعني السيرفر طفى
        time.sleep(0.8)

@bot.message_handler(commands=['start'])
def start(m):
    bot.send_message(m.chat.id, "يامي (وضع الطوارئ) جاهز 🚀\nاكتب (إطلاق) عشان أبدأ فوراً.")

@bot.message_handler(func=lambda m: True)
def handle(m):
    global running, length
    if "إطلاق" in m.text:
        running = True
        threading.Thread(target=hunt, daemon=True).start()
        bot.reply_to(m, "🚀 المحركات بدأت تدور.. راقب الصيدات!")
    elif "إيقاف" in m.text:
        running = False
        bot.reply_to(m, "🛑 توقفنا.")
    elif m.text.isdigit():
        length = int(m.text)
        bot.reply_to(m, f"⚙️ تم تغيير الطول لـ {length}")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    threading.Thread(target=lambda: app.run(host='0.0.0.0', port=port)).start()
    bot.infinity_polling()
    
