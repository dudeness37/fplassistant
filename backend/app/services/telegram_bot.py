import asyncio
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from app.core.config import settings

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hello! I'm your FPL assistant bot. Use /register to link your chat.")

async def register(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = str(update.effective_chat.id)
    # call backend API to register
    import httpx
    async with httpx.AsyncClient() as client:
        res = await client.post("http://api:8000/api/telegram/register", json={"telegram_chat_id": chat_id})
        _ = res.json()
    await update.message.reply_text(f"Registered! (chat_id: {chat_id})")

def main():
    token = settings.TELEGRAM_BOT_TOKEN
    if not token:
        raise RuntimeError("TELEGRAM_BOT_TOKEN not provided")
    application = ApplicationBuilder().token(token).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("register", register))

    logger.info("Telegram bot started")
    application.run_polling()

if __name__ == "__main__":
    main()
