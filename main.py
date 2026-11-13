import logging
import os

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CallbackQueryHandler,
    CommandHandler,
    ContextTypes,
)

TOKEN = os.getenv("BOT_TOKEN")

logging.basicConfig(
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    keyboard = [
        [InlineKeyboardButton("طلا", callback_data="gold")],
        [InlineKeyboardButton("یورو/دلار", callback_data="eurusd")],
        [InlineKeyboardButton("بیت‌کوین", callback_data="bitcoin")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.effective_message.reply_text(
        "سلام! ربات دستیار معامله‌گر روشن است.\n\n"
        "از دکمه‌های زیر یک بازار را انتخاب کن.\n"
        "توجه: در این مرحله فقط پاسخ‌گویی تلگرام آزمایش می‌شود؛ هنوز قیمت زنده، تحلیل هوشمند یا اتصال به متاتریدر فعال نیست.",
        reply_markup=reply_markup,
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.effective_message.reply_text(
        "دستورهای ربات:\n"
        "/start  نمایش منوی اصلی\n"
        "/gold  انتخاب طلا\n"
        "/eurusd  انتخاب یورو/دلار\n"
        "/bitcoin  انتخاب بیت‌کوین\n"
        "/help  راهنما"
    )


async def show_market(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    message = update.effective_message
    command_text = message.text.split()[0] if message and message.text else ""
    market = command_text.split("@")[0].lstrip("/").lower()
    await send_market_message(update, market)


async def market_button(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    if query is None:
        return
    await query.answer()
    await send_market_message(update, query.data, edit=True)


async def send_market_message(
    update: Update,
    market: str,
    edit: bool = False,
) -> None:
    labels = {
        "gold": "طلا",
        "eurusd": "جفت‌ارز یورو/دلار",
        "bitcoin": "بیت‌کوین",
    }
    label = labels.get(market)
    if label is None:
        message = "این گزینه را نمی‌شناسم. برای دیدن منو /start را بفرست."
    else:
        message = (
            f"{label} انتخاب شد.\n\n"
            "اتصال داده‌های زنده و تحلیل این بازار هنوز در این نسخه نصب نشده است. "
            "فعلاً هیچ سیگنال خرید یا فروشی صادر نمی‌شود و هیچ معامله‌ای انجام نمی‌شود."
        )

    if edit and update.callback_query is not None:
        await update.callback_query.edit_message_text(message)
    elif update.effective_message is not None:
        await update.effective_message.reply_text(message)


def main() -> None:
    if not TOKEN:
        raise RuntimeError(
            "متغیر BOT_TOKEN تنظیم نشده است. توکن را در همان ترمینال تنظیم کن و دوباره اجرا کن."
        )

    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("gold", show_market))
    app.add_handler(CommandHandler("eurusd", show_market))
    app.add_handler(CommandHandler("bitcoin", show_market))
    app.add_handler(CallbackQueryHandler(market_button))

    logger.info("ربات روشن شد و آماده دریافت پیام است.")
    # حلقه رویداد را خود کتابخانه مدیریت می‌کند؛ نیازی به asyncio.get_event_loop نیست.
    app.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()

