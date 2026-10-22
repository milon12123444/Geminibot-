import os
import sys
from google import genai
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, filters

# রেন্ডার সার্ভার থেকে সিক্রেট কি রিড করবে
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")

if not GEMINI_API_KEY or not TELEGRAM_BOT_TOKEN:
    print("Error: API Key or Bot Token missing!")
    sys.exit(1)

client = genai.Client(api_key=GEMINI_API_KEY)

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text
    if not user_message:
        return
    
    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=user_message,
        )
        reply_text = response.text
    except Exception as e:
        reply_text = "দুঃখিত, এই মুহূর্তে উত্তর দিতে সমস্যা হচ্ছে, Dude।"

    await update.message.reply_text(reply_text)

if __name__ == '__main__':
    app = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))
    print("বট ক্লাউডে সফলভাবে চালু হয়েছে...")
    app.run_polling()
  
