import telebot
import pymongo
import os
from flask import Flask
from threading import Thread

# 1. הגדרות ומשתני סביבה (נמשכים מההגדרות ב-Render)
TOKEN = os.environ.get('BOT_TOKEN')
MONGO_URI = os.environ.get('MONGO_URI')
PORT = int(os.environ.get('PORT', 8080))

bot = telebot.TeleBot(TOKEN)
app = Flask('')

# 2. חיבור לבסיס הנתונים MongoDB
try:
    client = pymongo.MongoClient(MONGO_URI)
    db = client['kevin_db']  # שם בסיס הנתונים
    movies_collection = db['movies'] # שם הטבלה
    print("✅ Connected to MongoDB successfully!")
except Exception as e:
    print(f"❌ MongoDB Connection Error: {e}")

# 3. פונקציות הבוט (טלגרם)
@bot.message_handler(commands=['start'])
def send_welcome(message):
    user_name = message.from_user.first_name
    bot.reply_to(message, f"אהלן {user_name}! הבוט שלך באוויר, נקי ומוכן לעבודה. 🚀")

@bot.message_handler(func=lambda message: True)
def echo_all(message):
    bot.reply_to(message, "קיבלתי את ההודעה שלך! הבוט מגיב מצוין.")

# 4. הגדרת שרת Flask (ה-Keep Alive)
@app.route('/')
def home():
    return "Bot is running and healthy!"

def run_flask():
    app.run(host='0.0.0.0', port=PORT)

# 5. הפעלה משולבת: שרת + בוט
if __name__ == "__main__":
    # הרצת Flask בשרשור נפרד (Thread)
    t = Thread(target=run_flask)
    t.start()
    
    print(f"🚀 Server is up on port {PORT}")
    print("🤖 Bot is now polling...")
    
    # הפעלת הבוט (Infinity Polling דואג שהוא יחזור לעבוד גם אם יש תקלה זמנית)
    bot.infinity_polling()
