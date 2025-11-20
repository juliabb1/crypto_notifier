import discord
from discord.ext import commands
import logging

from app.services.DataService import DataService

logging.basicConfig(level=logging.INFO)

class DiscordBot:
    def __init__(self, token: str, guild_id: int, data_service: DataService):
        """Initializes the bot with token, guild ID, and dependencies."""
        self.token = token
        self.guild_id = guild_id
        self.data_service = data_service
        self.MY_GUILD = discord.Object(id=self.guild_id)
        self.intents = discord.Intents.default()
        self.intents.message_content = True
        self.bot = commands.Bot(command_prefix='/', intents=self.intents)
        # self._add_events_and_commands()

    def _add_events_and_commands(self):
        """Registers all events and commands."""
        @self.bot.event
        async def on_ready():
            if self.bot.guilds:
                target_guild = self.bot.get_guild(self.guild_id)
                if target_guild:
                    self.bot.tree.copy_global_to(guild=target_guild)
                    await self.bot.tree.sync(guild=target_guild)
            logging.info(f'We have logged in as {self.bot.user} and commands synced.')

        @self.bot.command(name='echo')
        async def _echo(ctx: commands.Context, *, arg: str):
            """A command that echoes the provided argument."""
            await ctx.channel.send(f"You said: {arg}")

        @self.bot.command(name='list')
        async def _list_data(ctx: commands.Context):
            """Retrieves and sends data using the injected DataService."""
            logging.info(f'IN LIST CMDDDD')

            data_list = self.data_service.list_top_10_crypto_currencies()

            response_text = "**Top 10 Cryptocurrencies:**\n"
            for index, coin in enumerate(data_list, start=1):
                price_formatted = f"${coin.current_price:,.2f}"
                response_text += (
                    f"**{index}. {coin.name}** (`{coin.symbol}`)\n"
                    f"   💰 Price: {price_formatted}\n"
                )
            await ctx.channel.send(response_text)

    def run(self):
        """Starts the Discord bot."""
        logging.info("Starting Discord Bot...")
        # This call is blocking, so it must be run in a separate thread.
        try:
            self.bot.run(self.token)
        except discord.LoginFailure:
            logging.error("Discord token is invalid or missing.")
        except Exception as e:
            logging.error(f"An error occurred while running the Discord bot: {e}")