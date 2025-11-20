import asyncio
import os
import threading
import logging
from dotenv import load_dotenv
from app.services.DataService import DataService
from app.telegram_bot import TelegramBot
from app.discord_bot import DiscordBot

load_dotenv(dotenv_path='.env.dev')
DISCORD_TOKEN = os.environ.get('DISCORD_BOT_TOKEN')
TELEGRAM_TOKEN = os.environ.get('TELEGRAM_BOT_TOKEN')
DISCORD_GUILD_ID = os.environ.get('DISCORD_GUILD_ID')

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(threadName)s - %(levelname)s - %(message)s')

def main():
    """The main entry point of your multi-bot application."""
    logging.info("--- Starting Multi-Bot Application ---")

    # Both bots will use same instance to fetch data
    shared_data_service = DataService()
    logging.info("Shared DataService instantiated.")

    # --- Discord Bot Setup ---
    if DISCORD_TOKEN and DISCORD_GUILD_ID:
        discord_bot_instance = DiscordBot(
            token=DISCORD_TOKEN,
            guild_id=DISCORD_GUILD_ID,
            data_service=shared_data_service
        )
        # Start Discord Bot in a separate, daemonized thread
        discord_thread = threading.Thread(
            target=discord_bot_instance.run,
            name="DiscordBotThread",
            daemon=True
        )
        discord_thread.start()
        logging.info("Discord Bot started in a background thread.")
    else:
        logging.warning("Discord Bot skipped: Token or Guild ID is missing.")

    # --- Telegram Bot Setup ---
    if TELEGRAM_TOKEN:
        telegram_bot_instance = TelegramBot(
            token=TELEGRAM_TOKEN,
            data_service=shared_data_service
        )
        # Start Telegram Bot in a separate, daemonized thread
        telegram_thread = threading.Thread(
            target=telegram_bot_instance.run,
            name="TelegramBotThread",
            daemon=True
        )
        telegram_thread.start()
        logging.info("Telegram Bot started in a background thread.")
    else:
        logging.warning("Telegram Bot skipped: Token is missing.")

    try:
        logging.info("Main application (mathdo) is running. Press Ctrl+C to exit.")
        while True:
            # Keep main thread alive so the daemon threads (bots) can run
            threading.Event().wait(3)
    except KeyboardInterrupt:
        logging.info("Main application interrupted. Shutting down all services.")

def main_synchronous():
    shared_data_service = DataService()
    discord_bot = DiscordBot(DISCORD_TOKEN, DISCORD_GUILD_ID, shared_data_service)
    telegram_bot = TelegramBot(TELEGRAM_TOKEN, shared_data_service)

    loop = asyncio.get_event_loop()
    loop.create_task(discord_bot.run())
    threading.Thread(target=loop.run_forever).start()
    # discordBot.run()
    logging.info("!!!Discord Bot started.!!!")
    telegram_bot.run()
    logging.info("Telegram Bot started.")

if __name__ == '__main__':
    # main()
    main_synchronous()