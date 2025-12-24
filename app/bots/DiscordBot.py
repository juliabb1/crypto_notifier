import os
import logging
import discord
from discord.ext import commands
from discord import app_commands
from app.repository.cryptocurrency_repository import CryptocurrencyRepository
from app.services.crypto_api_service import CryptoApiService
from app.services.data_service import DataService

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(threadName)s - %(levelname)s - %(message)s')
DISCORD_GUILD_ID = int(os.environ.get('DISCORD_GUILD_ID'))


class Crypto_Notifier_Cog(commands.Cog):
    def __init__(
            self, 
            bot, 
            crypto_service: CryptoApiService, 
            cryptocurrency_repository: CryptocurrencyRepository):
        self.bot = bot
        self.crypto_service = crypto_service
        self.cryptocurrency_repository = cryptocurrency_repository
        self._last_member = None

    async def cog_load(self):
        crypto_names = self.cryptocurrency_repository.get_all_cryptocurrency_names()
        choices = [
            app_commands.Choice(name=name, value=name)
            for name in crypto_names[:25]  # Discord limit is 25 choices
        ]
        # TODO: Doesnt work, fix it
        self._index.choices = choices
        return await super().cog_load()

    @commands.command(name='echo')
    async def _echo(self, ctx: commands.Context, *, arg: str):
        await ctx.channel.send(f"You said: {arg}")

    @app_commands.command(name="index", description="Get price/index of a cryptocurrency")
    @app_commands.describe(currency="The type of cryptocurrency")
    @app_commands.guilds(discord.Object(id=DISCORD_GUILD_ID))
    async def _index(self, interaction: discord.Interaction, currency: str):
        result = await self.crypto_service.get_index(currency)
        if result is None:
            await interaction.response.send_message(f"Could not find price for {currency}")
        else:
            await interaction.response.send_message(f"{currency.capitalize()}: {result:.2f} €")


    @commands.command(name='list')
    async def _list(self, ctx: commands.Context):
        result = await self.crypto_service.list_top_crypto_currencies(amount=10)
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
    def __init__(
            self, 
            token: str, 
            client_id: int, 
            guild_id: int, 
            channel_id: int,
            crypto_api_service: CryptoApiService,
            data_service: DataService,
            cryptocurrency_repository: CryptocurrencyRepository):
        
        self.token = token
        self.client_id = client_id
        self.guild_id = guild_id # guild = server
        self.channel_id = channel_id
        self.crypto_api_service = crypto_api_service
        self.data_service = data_service
        self.cryptocurrency_repository = cryptocurrency_repository

        intents = discord.Intents.default()
        intents.message_content = True
        self.bot = commands.Bot(command_prefix='/', intents=intents)

        @self.bot.event
        async def on_ready():
            logging.info(f"Bot logged in as {self.bot.user}")
            
            # Sync app_commands to guild (no global commands)
            try:
                # First copy global commands to the guild
                # self.bot.tree.copy_global_to(guild=discord.Object(id=self.guild_id))
                # Then sync to the guild
                synced = await self.bot.tree.sync(guild=discord.Object(id=self.guild_id))
                logging.info(f"Synced {len(synced)} app_commands to guild")
            except Exception as e:
                logging.error(f"Failed to sync app_commands: {e}")

        @self.bot.event
        async def on_command_error(ctx, error):
            if isinstance(error, commands.CommandNotFound):
                await ctx.send(f"Command not found.")
            else:
                logging.error(f"Command error: {error}")

    async def start(self):        
        cog = Crypto_Notifier_Cog(self.bot, self.crypto_api_service, self.cryptocurrency_repository)
        await self.bot.add_cog(cog)
        await self.bot.start(self.token)
        logging.info("DiscordBot has started!")

    async def stop(self):
        """Stop the Discord bot."""
        await self.bot.close()
