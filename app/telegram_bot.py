import logging
import os
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters
from dotenv import load_dotenv

from app.services.DataService import DataService

load_dotenv(dotenv_path='.env.dev')
TOKEN = os.environ.get('TELEGRAM_BOT_TOKEN')

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

class TelegramBot:
    def __init__(self, token: str, data_service):
        """Initializes the bot with its token and dependencies."""
        self.token = token
        self.data_service = data_service
        self.application = ApplicationBuilder().token(self.token).build()
        self._add_handlers()

    async def _general_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Echoes any non-command text message."""
        logging.info(f"Received message from chat {update.effective_chat.id}: {update.message.text}")
        await context.bot.send_message(chat_id=update.effective_chat.id, text=update.message.text)

    async def _caps(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Converts command arguments to uppercase."""
        text_caps = ' '.join(context.args).upper()
        logging.info(f"Processed /caps command. Result: {text_caps}")
        await context.bot.send_message(chat_id=update.effective_chat.id, text=text_caps)

    async def _list_data(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Retrieves and sends data using the injected DataService."""
        data_list = self.data_service.list_top_10_crypto_currencies()
        response_text = "📚 **Top 10 Cryptocurrencies:**\n\n"
        for index, coin in enumerate(data_list, start=1):
            price_formatted = f"${coin.current_price:,.2f}"
            response_text += (
                f"**{index}. {coin.name}** (`{coin.symbol}`)\n"
                f"   💰 Price: {price_formatted}\n"
            )
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=response_text,
            parse_mode='Markdown'
        )

    def _add_handlers(self):
        """Registers all command and message handlers with the Application."""
        self.application.add_handler(
            MessageHandler(filters.TEXT & (~filters.COMMAND), self._general_message)
        )
        self.application.add_handler(
            CommandHandler('caps', self._caps)
        )
        # Use the bound method for the handler
        self.application.add_handler(
            CommandHandler('list', self._list_data)
        )

    def run(self):
        """Starts the bot using long polling."""
        logging.info("Starting Telegram Bot.")
        # self.application.run_polling(stop_signals=[])
        self.application.run_webhook()

# run the bot directly from this file (for testing)
if __name__ == '__main__':
    if not TOKEN:
        logging.error("TELEGRAM_BOT_TOKEN not found in environment variables.")
    else:
        service = DataService()
        bot = TelegramBot(token=TOKEN, data_service=service)
        bot.run()