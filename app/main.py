import asyncio
import os
import logging
from dotenv import load_dotenv
from app.bots.DiscordBot import DiscordBot
from app.bots.TelegramBot import TelegramBot

load_dotenv(dotenv_path='.env.dev')
DISCORD_TOKEN = os.environ.get('DISCORD_BOT_TOKEN')
TELEGRAM_TOKEN = os.environ.get('TELEGRAM_BOT_TOKEN')
DISCORD_GUILD_ID = int(os.environ.get('DISCORD_GUILD_ID'))

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(threadName)s - %(levelname)s - %(message)s')


async def run_bots_asynchronously():
    discord_bot = DiscordBot(DISCORD_TOKEN)
    telegram_bot = TelegramBot(TELEGRAM_TOKEN)
    await asyncio.gather(
        discord_bot.start(),
        telegram_bot.start()
    )
    try:
        await asyncio.Future() 
    except asyncio.CancelledError:  
        pass  
    
    await discord_bot.stop()
    await telegram_bot.stop()


if __name__ == '__main__':
    asyncio.run(run_bots_asynchronously())
