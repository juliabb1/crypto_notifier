import os
import logging
import json
import asyncio
import httpx
import discord
from discord.ext import commands
from app.services.DataService import DataService

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(threadName)s - %(levelname)s - %(message)s')


class Crypto_Notifier(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None

    @commands.command(name='echo')
    async def _echo(self, ctx: commands.Context, *, arg: str):
        await ctx.channel.send(f"You said: {arg}")

    @commands.command(name='index')
    async def _index(self, ctx: commands.Context, *, arg: str):
        if not arg:
            await ctx.channel.send("Please provide a cryptocurrency name. Usage: /index btc")
            return
        result = await DataService.get_index(arg)
        if result is None:
            await ctx.channel.send(f"Could not find price for {arg}")
        else:
            await ctx.channel.send(f"{arg.capitalize()}: {result:.2f} €")

    @commands.command(name='list')
    async def _list(self, ctx: commands.Context):
        result = await DataService.list_top_crypto_currencies(amount=10)
        message = "Top 10 Cryptocurrencies by Market Cap:\n\n"
        for coin in result:
            message += f"{coin.market_cap_rank}. {coin.name} ({coin.symbol.upper()})\n"
            message += f"   Price: ${coin.current_price:.2f} €\n"
            message += f"   Market Cap: ${coin.market_cap:,} €\n\n"
        await ctx.channel.send(message)

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if message.author == self.bot.user:
            return
        if message.content.startswith(self.bot.command_prefix):
            return
        await message.channel.send(f"I heard you say: {message.content}")


class DiscordBot:
    def __init__(self, token: str, client_id: int, guild_id: int, channel_id: int):
        self.token = token
        self.client_id = client_id
        self.guild_id = guild_id
        self.channel_id = channel_id
        intents = discord.Intents.default()
        intents.message_content = True
        self.bot = commands.Bot(command_prefix='/', intents=intents)

        @self.bot.event
        async def on_command_error(ctx, error):
            if isinstance(error, commands.CommandNotFound):
                await ctx.send(f"Command not found. Use `/echo`, `/index`, or `/list`")
            else:
                logging.error(f"Command error: {error}")

    async def start(self):
        """Start the Discord bot."""
        await self.bot.add_cog(Crypto_Notifier(self.bot))
        await self.bot.start(self.token)
        logging.info("DiscordBot has started!")

    async def stop(self):
        """Stop the Discord bot."""
        await self.bot.close()
