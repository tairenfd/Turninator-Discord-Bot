import discord
from discord.ext import commands

from utils.channel_create import create_mod_channels

# from utils.database.create import
from utils.database.read import (
    get_last_row_from_all_tables,
    get_last_row_from_user_id_and_server_id,
    get_rows_from_user_id_and_server_id,
)
from utils.logging import get_logger
from utils.tools import create_embed, format_rows, get_timestamp

logger = get_logger("commands.log")


class ModCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        super().__init__()

    # Delete the bot created moderation channels
    @commands.hybrid_command(name="delete_mod_channels")
    @commands.has_permissions(manage_channels=True)
    async def delete_turninator_channels(self, ctx):
        guild = ctx.guild
        channels_to_delete = [
            channel
            for channel in guild.channels
            if channel.name.startswith("turninator-")
        ]
        if not channels_to_delete:
            await ctx.send("No channels found with the name prefix 'turninator-'.")
            return
        for channel in channels_to_delete:
            await channel.delete()
        await ctx.author.send(f"Deleted {len(channels_to_delete)} channels.")

    # Create the moderation channels associated with bot
    @commands.hybrid_command(name="create_mod_channels")
    @commands.has_permissions(manage_channels=True)
    async def create_turninator_channels(self, ctx):
        await create_mod_channels(ctx.guild)

    # sync commands to guild
    @commands.hybrid_command(name="sync")
    @commands.is_owner()
    async def sync_commands(self, ctx):
        self.bot.tree.copy_global_to(guild=ctx.guild)
        await self.bot.tree.sync(guild=ctx.guild)
        logger.info(f"Tree synced for {ctx.guild.name}")
        print(f"Tree synced for {ctx.guild.name}")
        logger.info(f"Commands synced for {ctx.me} in {ctx.guild.name}")
        print(f"Commands synced for {ctx.me} in {ctx.guild.name}")

    @commands.command()
    async def history(self, ctx, user: discord.Member = None, table: str = None):
        """Fetch the history of a user from the database"""
        if user is None:
            await ctx.send("Please mention a user to fetch the history for")
            return

        if table not in [
            "automod_history",
            "kick_history",
            "warning_history",
            "ban_history",
            "unban_history",
            "notes_history",
        ]:
            await ctx.send("Please provide a valid table name")
            return

        rows = get_rows_from_user_id_and_server_id(user.id, ctx.guild.id, table)
        if len(rows) == 0:
            await ctx.send(f"No history found for {user.name} in {table}")
            return

        title = f"History for {user.name} in {table.replace('_', ' ')}:\n"
        message = format_rows(rows=rows, table=table)

        embed = create_embed(
            title=title,
            description=message,
            colour=0x00FF00,
            author=f"{user.name}'s History",
            thumbnail=user.avatar.url,
        )
        await ctx.send(embed=embed)

    @commands.command()
    async def last_history(self, ctx, user: discord.Member = None, table: str = None):
        """Fetch the last entry in the history of a user from the database"""
        if user is None:
            await ctx.send("Please mention a user to fetch the last history entry for")
            return

        if table not in [
            "automod_history",
            "kick_history",
            "warning_history",
            "ban_history",
            "unban_history",
            "notes_history",
        ]:
            await ctx.send("Please provide a valid table name")
            return

        row = get_last_row_from_user_id_and_server_id(user.id, ctx.guild.id, table)
        if row is None:
            await ctx.send(f"No history found for {user.name} in {table}")
            return

        embed = create_embed(
            title="Last Entry",
            description=f"Last entry for {user.name} in {table.replace('_history', '')}: {format_rows(rows=row)}",
            colour=0x00FF00,
            author=f"{user.name}'s Last Entry",
            thumbnail=user.avatar.url,
        )
        await ctx.send(embed=embed)

    @commands.command()
    async def last_entry(self, ctx):
        """Fetch the last entry in any table in the database"""
        row = get_last_row_from_all_tables()
        if row is None:
            await ctx.send("No history found in any table")
            return

        embed = create_embed(
            title="Last Entry",
            description=f"Last entry in any table: {format_rows(rows=row)}",
            colour=0x00FF00,
        )
        await ctx.send(embed=embed)
