import discord
from discord.ext import commands

from utils.channel_create import create_mod_channels
from utils.logging import get_logger, setup_logger

setup_logger("logs", "mod_events.log")
logger = get_logger("mod_events.log")


class CreateChannels(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def setup(self):
        pass

    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        # Create channels
        await create_mod_channels(guild)
        # Log channels
        logger.info(
            f"Moderation channel msg_edit created in {guild.name} (id: {guild.id})"
        )
        logger.info(f"Moderation channel mute created in {guild.name} (id: {guild.id})")
        logger.info(f"Moderation channel warn created in {guild.name} (id: {guild.id})")
        logger.info(f"Moderation channel ban created in {guild.name} (id: {guild.id})")
        logger.info(f"Moderation channel kick created in {guild.name} (id: {guild.id})")
        logger.info(
            f"Moderation channel unban created in {guild.name} (id: {guild.id})"
        )
        logger.info(
            f"Moderation channel unmute created in {guild.name} (id: {guild.id})"
        )
        logger.info(
            f"Moderation channel user_join created in {guild.name} (id: {guild.id})"
        )
        logger.info(
            f"Moderation channel user_leave created in {guild.name} (id: {guild.id})"
        )
        logger.info(
            f"Moderation channel message_delete created in {guild.name} (id: {guild.id})"
        )
        logger.info(
            f"Moderation channel message_edit created in {guild.name} (id: {guild.id})"
        )
        logger.info(
            f"Moderation channel role_change created in {guild.name} (id: {guild.id})"
        )
        logger.info(
            f"Moderation channel nickname_change created in {guild.name} (id: {guild.id})"
        )
        logger.info(
            f"Moderation channel automod created in {guild.name} (id: {guild.id})"
        )
        logger.info(
            f"Moderation channel spam_detection created in {guild.name} (id: {guild.id})"
        )
