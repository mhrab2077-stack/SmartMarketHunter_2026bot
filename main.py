import os
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

TOKEN = os.getenv("BOT_TOKEN")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "سلام! ربات شکارچی بازار فعال شد.\n"
        "بازارهای فارکس، طلا و بیت‌کوین در برنامه تحلیل قرار دارند."
    )

if not TOKEN:
    raise ValueError("توکن ربات تنظیم نشده است.")

app = Application.builder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))

app.run_polling()
