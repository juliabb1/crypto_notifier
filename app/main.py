import asyncio
from calendar import c
import os
import logging
from re import A
import httpx
from dotenv import load_dotenv
from app.bots.DiscordBot import DiscordBot
from app.bots.TelegramBot import TelegramBot
from app.services.cryptocurrency_service import CryptocurrencyService
from app.services.CryptoApiService import CryptoApiService
from app.

load_dotenv(dotenv_path='.env.dev')
DISCORD_TOKEN = os.environ.get('DISCORD_BOT_TOKEN')
TELEGRAM_TOKEN = os.environ.get('TELEGRAM_BOT_TOKEN')
DISCORD_GUILD_ID = int(os.environ.get('DISCORD_GUILD_ID'))
DISCORD_CLIENT_ID = int(os.environ.get('DISCORD_CLIENT_ID'))
DISCORD_CHANNEL_ID = int(os.environ.get('DISCORD_CHANNEL_ID'))


logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(threadName)s - %(levelname)s - %(message)s')


async def run_bots_asynchronously():
    # crypto_service_db = CryptocurrencyService()
    
    # if not crypto_service_db.cryptocurrencies_exist():
    #     async with httpx.AsyncClient() as client:
    #         crypto_api_service = CryptoApiService(client)
    #         crypto_currencies = await crypto_api_service.list_top_crypto_currencies(amount=50)
    #         crypto_service_db.store_cryptocurrencies(crypto_currencies)

    crypto_api_service = CryptoApiService(httpx.AsyncClient())
    account_service = AccountService()

    discord_bot = DiscordBot(
        DISCORD_TOKEN, 
        DISCORD_CLIENT_ID, 
        DISCORD_GUILD_ID, 
        DISCORD_CHANNEL_ID,
        crypto_api_service
    )
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
