import discord
from discord.ext import commands

from utils.channel_utils import create_mod_channels
from utils.logging import get_logger, setup_logger

setup_logger("/home/central-turn/discord_services/turnbot/logs", "mod_events.log")
logger = get_logger("mod_events.log")


class CreateChannels(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        super().__init__()

    @commands.Cog.listener()
    async def setup(self):
        pass

    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        """
        A listener method that is called whenever the bot joins a new guild.
        This method creates mod channels for the guild.

        Parameters:
            - guild (discord.Guild): The guild the bot has joined.
        """
        # Create channels
        await create_mod_channels(guild)
