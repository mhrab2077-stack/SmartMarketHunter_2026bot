import os
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    ContextTypes,
    filters
)

TOKEN = os.getenv("BOT_TOKEN")

logging.basicConfig(level=logging.INFO)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("🥇 تحلیل طلا", callback_data="gold")],
        [InlineKeyboardButton("₿ تحلیل بیت‌کوین", callback_data="bitcoin")],
        [InlineKeyboardButton("💱 تحلیل فارکس", callback_data="forex")],
        [InlineKeyboardButton("📚 راهنما", callback_data="help")]
    ]

    await update.message.reply_text(
        "🤖 به شکارچی هوشمند بازار خوش آمدی!\n\n"
        "یکی از گزینه‌های زیر را انتخاب کن:",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

async def buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    messages = {
        "gold": "🥇 بخش تحلیل طلا انتخاب شد.",
        "bitcoin": "₿ بخش تحلیل بیت‌کوین انتخاب شد.",
        "forex": "💱 بخش تحلیل فارکس انتخاب شد.",
        "help": "📚 برای دریافت تحلیل، درخواستت را ارسال کن."
    }

    await query.message.reply_text(
        messages.get(query.data, "درخواست نامعتبر است.")
    )

async def message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "درخواستت دریافت شد.\n"
        "برای استفاده از امکانات ربات، از منوی اصلی استفاده کن."
    )

def main():
    if not TOKEN:
        raise ValueError("توکن ربات تنظیم نشده است.")

    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(buttons))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, message))

    print("ربات فعال شد.")

    app.run_polling()

if __name__ == "__main__":
    main()
