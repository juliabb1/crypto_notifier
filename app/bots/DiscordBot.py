import os
import logging
import discord
from discord.ext import commands
from app.services.DataService import DataService

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(threadName)s - %(levelname)s - %(message)s')


class Tracker(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None

    @commands.command(name='echo')
    async def _echo(self, ctx: commands.Context, *, arg: str):
        await ctx.channel.send(f"You said: {arg}")

    @commands.command(name='list')
    async def _list(self, ctx: commands.Context, *, arg: str):
        data_service = DataService()
        result = data_service.list_top_10_crypto_currencies()
        await ctx.channel.send(f"You said: {result}")

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if message.author == self.bot.user:
            return
        if message.content.startswith(self.bot.command_prefix):
            return
        await message.channel.send(f"I heard you say: {message.content}")


class DiscordBot:
    def __init__(self, token: str):
        self.token = token
        intents = discord.Intents.default()
        intents.message_content = True
        self.bot = commands.Bot(command_prefix='/', intents=intents)

    async def start(self):
        """Start the Discord bot."""
        await self.bot.add_cog(Tracker(self.bot))
        await self.bot.start(self.token)
        logging.info("DiscordBot has started!")


    async def stop(self):
        """Stop the Discord bot."""
        await self.bot.close()
