import asyncio
import os
import logging
import discord
from discord.ext import commands
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import ContextTypes, MessageHandler, filters, CommandHandler, ApplicationBuilder

load_dotenv(dotenv_path='.env.dev')
DISCORD_TOKEN = os.environ.get('DISCORD_BOT_TOKEN')
TELEGRAM_TOKEN = os.environ.get('TELEGRAM_BOT_TOKEN')
DISCORD_GUILD_ID = int(os.environ.get('DISCORD_GUILD_ID'))

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(threadName)s - %(levelname)s - %(message)s')

async def telegram_list_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /help is issued."""
    await update.message.reply_text("List!")

class Tracker(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None

    @commands.command(name='echo')
    async def _echo(self, ctx: commands.Context, *, arg: str):
        await ctx.channel.send(f"You said: {arg}")

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if message.author == self.bot.user:
            return
        if message.content.startswith(self.bot.command_prefix):
            return
        await message.channel.send(f"I heard you say: {message.content}")

telegram_bot = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
telegram_bot.add_handler(CommandHandler("list", telegram_list_command, block=False))

intents = discord.Intents.default()
intents.message_content = True
discord_bot = commands.Bot(command_prefix='/', intents=intents)

async def run_telegram_bot():
    await telegram_bot.initialize()
    await telegram_bot.start()
    await telegram_bot.updater.start_polling(
        poll_interval=0.0,
        timeout=60,
        allowed_updates=["message", "callback_query"],
        drop_pending_updates=True
    )

async def run_discord_bot():
    await discord_bot.add_cog(Tracker(discord_bot))
    await discord_bot.start(DISCORD_TOKEN)

async def stop_telegram_bot():
    await telegram_bot.updater.stop()
    await telegram_bot.stop()
    await telegram_bot.shutdown()

async def stop_discord_bot():
    await discord_bot.close()

async def run_bots_asynchronously():
    await run_telegram_bot()
    await run_discord_bot()
    try:
        await asyncio.Future() # wait indefinitely until future is resolved/canceled (in pending state)
    except asyncio.CancelledError: # when future is explicitly canceled, the previous "await" raises this exception
        pass # continue program flow
    await stop_telegram_bot()
    await stop_discord_bot()

if __name__ == '__main__':
    asyncio.run(run_bots_asynchronously())
