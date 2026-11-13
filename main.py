import os
import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

TOKEN = os.getenv("BOT_TOKEN")

logging.basicConfig(
format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
level=logging.INFO
)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
await update.message.reply_text(
"سلام! ربات دستیار معامله‌گر فعال است."
)

async def gold(update: Update, context: ContextTypes.DEFAULT_TYPE):
await update.message.reply_text("در حال بررسی طلا هستم.")

async def bitcoin(update: Update, context: ContextTypes.DEFAULT_TYPE):
await update.message.reply_text("در حال بررسی بیت‌کوین هستم.")

def main():
if not TOKEN:
raise ValueError("BOT_TOKEN تنظیم نشده است.")

app = Application.builder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("gold", gold))
app.add_handler(CommandHandler("bitcoin", bitcoin))

print("ربات فعال شد.")
app.run_polling()

if name == "main":
main()
