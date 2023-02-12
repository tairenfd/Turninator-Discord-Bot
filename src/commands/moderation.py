import asyncio
import discord
from discord.ext import commands
from datetime import datetime
from utils.channel_utils import create_mod_channels, delete_mod_channels
from utils.database.read import (
    get_last_row_from_all_tables,
    get_last_row_from_user_id_and_server_id,
    get_rows_from_user_id_and_server_id,
    get_last_BWK_from_all_tables_by_user,
)
from utils.database.create import insert_row_into_table
from utils.logging import get_logger
from utils.tools import (
    create_embed,
    format_rows,
    get_timestamp,
    set_default_permissions,
    get_permission_fields,
    parse_ban_time,
    format_ban_time,
    bulk_delete,
)

logger = get_logger("commands.log")


class ModCommands(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        super().__init__()

    @commands.hybrid_command(name="ban", with_app_command=True)
    @commands.has_permissions(ban_members=True)
    @commands.bot_has_permissions(ban_members=True)
    async def ban(
        self,
        ctx: commands.Context,
        user: discord.Member,
        time: str,
        *,
        reason: str = "None given",
        clean: int = 1,
    ):
        """
        Ban a member from the server.
        Parameters:
            - user: the member to be banned.
            - time: the duration of the ban in days.
            - reason: the reason for the ban.
            - clean: number of days of user's messages to be deleted.
        Example:
            - !ban @username 7 Offensive language 1
        """
        if user.id == self.bot.owner_id or user == self.bot.user:
            await ctx.send("Can not ban this user.")
            return

        print(time, "|||", reason)

        async def unbann(user, parsed_time):
            """
            Unban a member after the specified duration.
            Parameters:
                - user: the member to be unbanned.
                - parsed_time: the duration of the ban in seconds.
            """
            await asyncio.sleep(parsed_time)  # convert days to seconds
            await ctx.guild.unban(
                user,
                reason=f"Ban time of {format_ban_time(parsed_time)} days has expired.",
            )

        try:
            p_time = parse_ban_time(time)
            print(p_time)
        except ValueError as e:
            ctx.send(e)

        await ctx.send(
            f"User {user.mention} - {user.id} **BANNED** for {reason}.\nCleaned {clean} day(s) of messages by user."
        )
        await user.ban(reason=reason, delete_message_days=clean)
        self.bot.loop.create_task(unbann(user, p_time))
        insert_row_into_table(
            user.id, ctx.author.id, ctx.guild.id, reason, "ban_history"
        )
        print(f"Entry for user [{user.name} - {user.id}] added to ban history")

    @commands.hybrid_command(name="unban", with_app_command=True)
    @commands.has_permissions(ban_members=True)
    @commands.bot_has_permissions(ban_members=True)
    async def unban(
        self, ctx: commands.Context, user: discord.User, *, reason: str = "None given"
    ) -> None:
        """
        Unban a member from the server.
        Parameters:
            - user: the member to be unbanned.
            - reason: the reason for the unban.
        Example:
            - !unban @username he has been banned for 7 days
        """
        await ctx.guild.unban(user=user, reason=reason)
        await ctx.send(f"User <@{user.id}> unbanned by <@{ctx.author.id}>")
        insert_row_into_table(
            user.id, ctx.author.id, ctx.guild.id, reason, "unban_history"
        )
        print(f"Entry for user [{user.name} - {user.id}] added to unban history")

    @commands.hybrid_command(name="kick")
    @commands.has_permissions(ban_members=True)
    async def kick(
        self,
        ctx: commands.Context,
        user: discord.Member,
        *,
        reason: str = "No reason given.",
    ) -> None:
        """
        Kick a member from the server.
        Parameters:
            - user: the member to be kicked.
            - reason: the reason for the kick.
        Example:
            - !kick @username spamming in chat
        """
        if user.id == self.bot.owner_id or user == self.bot.user:
            await ctx.send("Can not kick this user.")
            return

        insert_row_into_table(
            user.id, ctx.author.id, ctx.guild.id, reason, "kick_history"
        )
        await self.send(f"User {user.mention} - {user.id} **KICKED** for {reason}.")
        await user.kick(reason=reason)
        print(f"Entry for user [{user.name} - {user.id}] added to kick history")

    @commands.hybrid_command(name="add_note")
    @commands.has_permissions(ban_members=True)
    async def add_note(self, ctx: commands.Context, user: discord.User, *, note: str) -> None:
        """
        Add a note to a user.

        Parameters:
            - user (discord.User): The user to add the note to.
            - note (str): The note to add.

        Requires:
            - The author must have the "ban members" permission.

        Example:
            !add_note @user This user is new to the server.
        """
        if not ctx.author.guild_permissions.ban_members:
            await ctx.send("You don't have permission to add notes")
            return

        insert_row_into_table(
            user.id, ctx.author.id, ctx.guild.id, note, "notes_history"
        )
        await ctx.send(f"Added note to user {user.mention} : {note}")

    # Delete the bot created moderation channels
    @commands.hybrid_command(name="delete_mod_channels")
    @commands.has_permissions(ban_members=True)
    @commands.has_permissions(manage_channels=True)
    @commands.has_role("turn")
    async def delete_turninator_channels(self, ctx: commands.Context) -> None:
        """
        Delete the bot-created moderation channels.

        Requires:
            - The author must have the "ban members" and "manage channels" permissions.
            - The author must have the "turn" role.

        Example:
            !delete_mod_channels
        """
        await delete_mod_channels(ctx.guild)

    # Create the moderation channels associated with bot
    @commands.hybrid_command(name="create_mod_channels")
    @commands.has_permissions(ban_members=True)
    @commands.has_permissions(manage_channels=True)
    @commands.has_role("turn")
    async def create_turninator_channels(self, ctx: commands.Context) -> None:
        """
        Create the bot-associated moderation channels.

        Requires:
            - The author must have the "ban members" and "manage channels" permissions.
            - The author must have the "turn" role.

        Example:
            !create_mod_channels
        """
        await create_mod_channels(ctx.guild)

    # sync commands to guild
    @commands.hybrid_command(name="sync")
    @commands.has_role("turn")
    async def sync_commands(self, ctx: commands.Context) -> None:
        """
        Synchronize commands with the server.

        Requires:
            - The author must have the "turn" role.

        Example:
            !sync
        """
        self.bot.tree.copy_global_to(guild=ctx.guild)
        await self.bot.tree.sync(guild=ctx.guild)
        logger.info(f"Tree synced for {ctx.guild.name}")
        print(f"Tree synced for {ctx.guild.name}")
        logger.info(f"Commands synced for {ctx.me} in {ctx.guild.name}")
        print(f"Commands synced for {ctx.me} in {ctx.guild.name}")

    @commands.hybrid_command(name="get_perms")
    @commands.has_permissions(ban_members=True)
    async def get_perms(
        self, ctx: commands.Context, user: discord.Member = None
    ) -> None:
        """
        Get the permissions for a user.

        Parameters:
            - user (discord.Member, optional): The user to get the permissions for. Defaults to None (the author).

        Requires:
            - The author must have the "ban members" permission.

        Example:
            !get_perms @user
        """
        if user is None:
            user = ctx.author

        fields = get_permission_fields(user)

        embed = create_embed(
            title=f"Permissions for {user}",
            colour=discord.Color.red(),
            author=f"{user.name}#{user.discriminator} - {user.id}",
            author_icon=user.avatar.url,
            timestamp=datetime.now(),
            thumbnail=user.avatar.url,
            fields=fields,
        )

        await ctx.send(embed=embed)

    @commands.hybrid_command(name="rapsheet")
    async def rapsheet(self, ctx, user: discord.Member = None) -> None:
        """
        Get a user's moderation history in the server.

        Parameters:
            ctx (discord.Context): The context of the message.
            user (discord.Member, optional): The user to get the moderation history for. Defaults to None.

        Example:
            !rapsheet @user
        """
        if user is None or user == ctx.author:
            _user = ctx.author
            automod = get_rows_from_user_id_and_server_id(
                _user.id, ctx.guild.id, "automod_history"
            )
            kicks = get_rows_from_user_id_and_server_id(
                _user.id, ctx.guild.id, "kick_history"
            )
            warnings = get_rows_from_user_id_and_server_id(
                _user.id, ctx.guild.id, "warning_history"
            )
            bans = get_rows_from_user_id_and_server_id(
                _user.id, ctx.guild.id, "ban_history"
            )
            unbans = get_rows_from_user_id_and_server_id(
                _user.id, ctx.guild.id, "unban_history"
            )
            notes = get_rows_from_user_id_and_server_id(
                _user.id, ctx.guild.id, "notes_history"
            )
        elif user and ctx.author.guild_permissions.ban_members:
            _user = user
            automod = get_rows_from_user_id_and_server_id(
                user.id, ctx.guild.id, "automod_history"
            )
            kicks = get_rows_from_user_id_and_server_id(
                user.id, ctx.guild.id, "kick_history"
            )
            warnings = get_rows_from_user_id_and_server_id(
                user.id, ctx.guild.id, "warning_history"
            )
            bans = get_rows_from_user_id_and_server_id(
                user.id, ctx.guild.id, "ban_history"
            )
            unbans = get_rows_from_user_id_and_server_id(
                user.id, ctx.guild.id, "unban_history"
            )
            notes = get_rows_from_user_id_and_server_id(
                user.id, ctx.guild.id, "notes_history"
            )
        else:
            await ctx.send("Permissions not set or no user by that name.")
            return

        fields = []
        last = get_last_BWK_from_all_tables_by_user(_user.id)

        if notes:
            notes_list = format_rows(notes, "notes_history")
            fields.append(("Notes", notes_list, False))

        if bans:
            ban_list = format_rows(bans, "ban_history")
            fields.append(("Bans", ban_list, False))

        if kicks:
            kick_list = format_rows(kicks, "kick_history")
            fields.append(("Kicks", kick_list, False))

        if warnings:
            warning_list = format_rows(kicks, "warning_history")
            fields.append(("Warnings", warning_list, False))

        if automod:
            automod_list = format_rows(automod, "automod_history")
            fields.append(("Warnings", automod_list, False))

        if unbans:
            unban_list = format_rows(unbans, "_history")
            fields.append(("Unbans", unban_list, False))

        if not any((bans, kicks)):
            fields.append(
                ("No previous moderation actions found for user.", None, False)
            )

        try:
            fields.append(
                ("Joined Server:", _user.joined_at.strftime("%Y-%m-%d %H:%M %Z"), True)
            )
        except:
            fields.append(("Joined Server:", "Not currently in server.", True))

        if last:
            fields.append(
                (
                    "Last offense:",
                    f"<t:{get_timestamp(last.timestamp)}:F> (<t:{get_timestamp(last.timestamp)}:R>) by **{last.code}**",
                    True,
                )
            )

        embed = create_embed(
            title="**__Moderation Statistics__**",
            colour=discord.Color.random(),
            author=f"{_user.name}#{_user.discriminator} - {_user.id}",
            author_icon=_user.avatar.url,
            timestamp=datetime.now(),
            thumbnail=_user.avatar.url,
            footer="\u200b",
            fields=fields,
        )

        await ctx.send(embed=embed)

    # get complete history of a table by user in the server
    @commands.hybrid_command(name="history")
    @commands.has_permissions(ban_members=True)
    async def history(
        self, ctx, user: discord.Member = None, table: str = None
    ) -> None:
        """
        Get the complete history of a user in a specified table in the server.

        Parameters:
            ctx (discord.Context): The context of the message.
            user (discord.Member): The user to get the history for.
            table (str): The name of the table to get the history from.

        Example:
            !history @user warning_history
        """
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

    # get last entry made in a table by user in the server
    @commands.hybrid_command(name="last_entry")
    @commands.has_permissions(ban_members=True)
    async def last_history(
        self, ctx, user: discord.Member = None, table: str = None
    ) -> None:
        """
        Get the last entry made in a specified table by a user in the server.
        
        Parameters:
            ctx (discord.Context): The context of the message.
            user (discord.Member): The user to get the history entry for.
            table (str): The name of the table to get the entry from.
        
        Example:
            !last_entry @user warning_history
        """
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

    # get last entry made between all tables in the server
    @commands.hybrid_command(name="last_entry_all")
    @commands.has_permissions(ban_members=True)
    async def last_entry(self, ctx: commands.Context) -> None:
        """
        Get the last entry made in any table by any user in the server.

        Parameters:
            ctx (discord.Context): The context of the message.

        Example:
            !last_entry_all
        """
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

    @commands.hybrid_command(name="set_perms")
    @commands.has_permissions(ban_members=True)
    @commands.has_any_role("turn", "TURNINATOR")
    async def set_perms(
        self, ctx: commands.Context, *, perms: str = None
    ) -> None:
        """
        Set default server permissions.

        Parameters:
            ctx (discord.Context): The context of the message.
            perms (str, optional): The default server permissions to set. Defaults to None.

        Example:
            !set_perms default
        """
        if perms == "default":
            await set_default_permissions(ctx.guild)
            await ctx.send(f"Default server permissions set by {ctx.author.mention}")

    @commands.hybrid_command(name="info")
    @commands.has_permissions(ban_members=True)
    async def get_member_info(self, ctx, user: discord.Member = None) -> None:
        """
        Get information about a user in the server.

        Parameters:
            ctx (discord.Context): The context of the message.
            user (discord.Member, optional): The user to get information about. Defaults to None.

        Example:
            !info @user
        """
        if user is None:
            user = ctx.author

        name = user.name
        id = user.id
        nickname = user.nick
        roles = [role.name for role in user.roles]
        roles = "\n".join(roles)

        permissions = get_permission_fields(user)
        fields = [
            ("Username", name, False),
            ("User ID", id, False),
            ("Server Nickname", nickname, False),
            ("User Roles", roles, False),
        ]
        fields += permissions

        embed = create_embed(
            title="**__Info__**",
            thumbnail=user.avatar.url,
            author=f'User info for {user.name} in "{user.guild}"',
            author_icon=user.avatar.url,
            colour=discord.Color.random(),
            fields=fields,
        )

        await ctx.send(embed=embed)

    @commands.hybrid_command(with_app_command=True)
    @commands.has_any_role("turn", "TURNINATOR", "wranglers")
    async def clean(
        self, ctx: commands.Context, limit: int, user: discord.Member = None
    ) -> None:
        """
        Delete messages in the server.

        Parameters:
            ctx (discord.Context): The context of the message.
            limit (int): The number of messages to delete.
            user (discord.Member, optional): The user whose messages to delete. Defaults to None.

        Example:
            !clean 10 @user
        """
        if user is None:
            deleted = await ctx.channel.purge(limit=limit)
        else:
            deleted = await bulk_delete(ctx, limit, user)

        msg = f"Removal completed of {len(deleted)} message(s)"
        if user:
            msg += f" by {user.mention}."
        msg += "."
        await ctx.send(msg)
