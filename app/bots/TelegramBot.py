import logging
from telegram import Update
from telegram.ext import ContextTypes, CommandHandler, ApplicationBuilder
from app.repository.favorite_repository import FavoriteRepository
from app.services.crypto_api_service import CryptoApiService
from app.services.data_service import DataService
from app.models import PlatformType

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(threadName)s - %(levelname)s - %(message)s')

class TelegramBot:

    PLATFORM_TYPE = PlatformType.Telegram

    def __init__(
            self, 
            token: str, 
            crypto_api_service: CryptoApiService,
            data_service: DataService,
            favorite_repository: FavoriteRepository):
        self.token = token
        self.crypto_api_service = crypto_api_service
        self.data_service = data_service
        self.favorite_repository = favorite_repository
        
        self.app = ApplicationBuilder().token(token).build()
        self.app.add_handler(CommandHandler("index", self.index_command, block=False))
        self.app.add_handler(CommandHandler("list", self.list_command, block=False))
        self.app.add_handler(CommandHandler("add_fav", self.save_fav_command, block=False))

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

    async def index_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        if not context.args:
            await update.message.reply_text("Please provide a cryptocurrency name. Usage: /index bitcoin")
            return
        index = context.args[0]
        result = await self.crypto_api_service.get_index(index=index)
        if result is None:
            await update.message.reply_text(f"Could not find price for {index}")
        else:
            await update.message.reply_text(f"{index.capitalize()}: {result:.2f} €")

    async def list_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        result = await self.crypto_api_service.list_top_crypto_currencies(amount=10)
        message = "Top 10 Cryptocurrencies by Market Cap:\n\n"
        for coin in result:
            message += f"{coin.market_cap_rank}. {coin.name} ({coin.symbol.upper()})\n"
            message += f"   Price: {coin.current_price:.2f} €\n"
            message += f"   Market Cap: {coin.market_cap:,} €\n\n"
        await update.message.reply_text(message)

    async def save_fav_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        user_id = update.effective_user.id
        input_crypto = context.args[0].lower()

        correct_input = self.data_service.check_account_and_crypto(
            platform=self.PLATFORM_TYPE,
            platform_id=str(user_id),
            input_crypto=input_crypto
        )

        if not correct_input:
            await update.message.reply_text(f"⚠️ Cryptocurrency '{input_crypto}' not found. Please check the name/symbol and try again.")
            return

        success = self.favorite_repository.add_favorite(
            platform=self.PLATFORM_TYPE,
            platform_id=user_id,
            symbol=input_crypto
        )
        
        if success:
            await update.message.reply_text(f"✅ Saved {input_crypto} as your favorite cryptocurrency!")
        else:
            await update.message.reply_text(f"⚠️ {input_crypto} is already in your favorites.")
