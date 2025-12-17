import logging
from telegram import Update
from telegram.ext import ContextTypes, CommandHandler, ApplicationBuilder

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(threadName)s - %(levelname)s - %(message)s')


async def telegram_list_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /list is issued."""
    await update.message.reply_text("List!")


class TelegramBot:
    def __init__(self, token: str):
        self.token = token
        self.app = ApplicationBuilder().token(token).build()
        self.app.add_handler(CommandHandler("list", telegram_list_command, block=False))

    async def start(self):
        """Start the Telegram bot."""
        await self.app.initialize()
        await self.app.start()
        await self.app.updater.start_polling(
            poll_interval=0.0,
            timeout=60,
            allowed_updates=["message", "callback_query"],
            drop_pending_updates=True
        )
        logging.info("TelegramBot has started!")

    async def stop(self):
        """Stop the Telegram bot."""
        await self.app.updater.stop()
        await self.app.stop()
        await self.app.shutdown()
