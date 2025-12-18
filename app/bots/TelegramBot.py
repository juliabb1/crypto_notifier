import logging
from telegram import Update
from telegram.ext import ContextTypes, CommandHandler, ApplicationBuilder
from app.services.DataService import DataService
from app.services.DatabaseService import AccountService, CryptocurrencyService, FavoriteService
from app.models import PlatformType

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(threadName)s - %(levelname)s - %(message)s')

class TelegramBot:
    def __init__(self, token: str):
        self.token = token
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
        result = await DataService.get_index(index=index)
        if result is None:
            await update.message.reply_text(f"Could not find price for {index}")
        else:
            await update.message.reply_text(f"{index.capitalize()}: {result:.2f} €")

    async def list_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        result = await DataService.list_top_crypto_currencies(amount=10)
        message = "Top 10 Cryptocurrencies by Market Cap:\n\n"
        for coin in result:
            message += f"{coin.market_cap_rank}. {coin.name} ({coin.symbol.upper()})\n"
            message += f"   Price: {coin.current_price:.2f} €\n"
            message += f"   Market Cap: {coin.market_cap:,} €\n\n"
        await update.message.reply_text(message)

    async def save_fav_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        logging.info(f" save_fav_command")

        user_id = update.effective_user.id
        if not context.args:
            await update.message.reply_text("Usage: /favorite bitcoin")
            return
        
        crypto_symbol = context.args[0].lower()
        
        if (not CryptocurrencyService.crypto_exists(crypto_symbol)):
            available = "❌ *{crypto_symbol}* not found.\n\n📋 **Available cryptocurrencies:**\n\n"
            for symbol, name in sorted(SYMBOL_TO_ID.items()):
                available += f"`{symbol}` - {name}\n"
            await update.message.reply_text(available, parse_mode="Markdown")
            return
        
        # Get or create user account
        user = AccountService.get_or_create_account(
                platform=PlatformType.Telegram,
                platform_id=user_id
            )
        
        logging.info(f"ADD_FAVORITE")
        # Add to favorites
        success = FavoriteService.add_favorite(
            platform=PlatformType.Telegram,
            platform_id=user_id,
            symbol=crypto_symbol
        )
        
        if success:
            await update.message.reply_text(f"✅ Saved {crypto_symbol} as your favorite cryptocurrency!")
        else:
            await update.message.reply_text(f"⚠️ Error saving {crypto_symbol} to your favorites.")
