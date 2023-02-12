from discord.ext import commands
from typing import Optional, Union
import discord
from utils.logging import get_logger, setup_logger
from utils.tools import create_embed, get_timestamp

setup_logger("logs", "mod_events.log")
logger = get_logger("mod_events.log")


class ModActions(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    async def log_event(
        self, 
        event_name: str, 
        user: discord.Member,
        guild: discord.Guild,
        before: Optional[Union[discord.Member, discord.Message]] = None,
        after: Optional[Union[discord.Member, discord.Message]] = None
    ) -> None:
        """
        Log various moderation events that occur in a server.

        Parameters:
            bot (discord.ext.commands.Bot): The bot instance.

        Methods:
            log_event(event_name, user, guild, before=None, after=None): Logs
                the details of the event triggered by the user.
            on_member_join(member): Logs the event of a new member joining
                the server and sends them a welcome message.
            on_member_remove(member): Logs the event of a member leaving the
                server.
            on_message_delete(message): Logs the event of a message being
                deleted.
            on_message_edit(before, after): Logs the event of a message being
                edited.
            on_member_update(before, after): Logs the event of a member's
                role or nickname being updated.
            on_mute(member): Logs the event of a member being muted.
            on_unmute(member): Logs the event of a member being unmuted.
            on_warn(member): Logs the event of a member being warned.
            on_ban(member): Logs the event of a member being banned.
            on_unban(member): Logs the event of a member being unbanned.
            on_kick(member): Logs the event of a member being kicked.
            on_automod(message): Logs the event of automoderation being
                triggered.
            on_spam_detection(message): Logs the event of spam detection.
            on_event(event_name, user, guild, before, after): Logs the
                details of the event triggered by the user.

        Example:
            # Instantiate the bot and add the ModActions cog
            bot = commands.Bot(command_prefix="!")
            bot.add_cog(ModActions(bot))
        """
        try:
            channel_name = f"turninator-{event_name}"
            channel = [c for c in guild.text_channels if c.name == channel_name][0]
            if channel is not None:
                fields = []
                if before and after:
                    if isinstance(before, discord.Member):
                        fields.append(
                            (
                                "Before",
                                f'Name: {before.name}\nNick: {before.nick}\nRoles: {", ".join([role.name for role in before.roles])}',
                                True,
                            )
                        )
                        fields.append(
                            (
                                "After",
                                f'Name: {after.name}\nNick: {after.nick}\nRoles: {", ".join([role.name for role in after.roles])}',
                                True,
                            )
                        )
                    if isinstance(before, discord.Message):
                        fields.append(
                            (
                                "Before",
                                f"Content: {before.content}\nChannel: {before.channel}\nCreated: <t:{get_timestamp(before.created_at)}:d>",
                                True,
                            )
                        )
                        if after.edited_at:
                            fields.append(
                                (
                                    "After",
                                    f"Content: {after.content}\nChannel: {after.channel}\nEdited: <t:{get_timestamp(after.edited_at)}:d>",
                                    True,
                                )
                            )

                embed = create_embed(
                    title=f"{event_name.title()} Event Triggered",
                    description=f"{user.mention} triggered a {event_name} event in {guild.name} : {channel.name}.",
                    colour=0x00FF00,
                    fields=fields,
                )
                await channel.send(embed=embed)
            logger.info(
                f"{event_name} event triggered by {user.mention} in {guild.name}"
            )
        except Exception as error:
            print(error)

    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member) -> None:
        # Log user join
        await self.log_event("user_join", member, member.guild)
        # Send welcome message
        channel = self.bot.get_channel(member.guild.id)
        await channel.send(
            f"Welcome {member.mention} to {member.guild.name}! Please read {member.guild.rules_channel.mention} to get started."
        )

    @commands.Cog.listener()
    async def on_member_remove(self, member: discord.Member) -> None:
        # Log user leave
        await self.log_event("user_leave", member, member.guild)

    @commands.Cog.listener()
    async def on_message_delete(self, message: discord.Message) -> None:
        # Log message delete
        await self.log_event("message_delete", message.author, message.guild)

    @commands.Cog.listener()
    async def on_message_edit(self, before: discord.Message, after: discord.Message) -> None:
        # Log message edit
        await self.log_event(
            "message_edit", before.author, after.guild, before=before, after=after
        )

    @commands.Cog.listener()
    async def on_member_update(
        self, before: discord.Member, after: discord.Member
    ):
        # Log role change
        if before.roles != after.roles:
            await self.log_event(
                "role_change", after, after.guild, before=before, after=after
            )
        # Log nickname change
        if before.nick != after.nick:
            await self.log_event(
                "nickname_change", after, after.guild, before=before, after=after
            )

    @commands.Cog.listener()
    async def on_mute(self, member: discord.Member) -> None:
        # Log mute
        await self.log_event("mute", member, member.guild)

    @commands.Cog.listener()
    async def on_unmute(self, member: discord.Member) -> None:
        # Log unmute
        await self.log_event("unmute", member, member.guild)

    @commands.Cog.listener()
    async def on_warn(self, member: discord.Member) -> None:
        # Log warn
        await self.log_event("warn", member, member.guild)

    @commands.Cog.listener()
    async def on_ban(self, member: Union[discord.Member, discord.User]) -> None:
        # Log ban
        await self.log_event("ban", member, member.guild)

    @commands.Cog.listener()
    async def on_unban(self, member: Union[discord.Member, discord.User]) -> None:
        # Log unban
        await self.log_event("unban", member, member.guild)

    @commands.Cog.listener()
    async def on_kick(self, member: discord.Member) -> None:
        # Log kick
        await self.log_event("kick", member, member.guild)

    @commands.Cog.listener()
    async def on_automod(self, message: discord.Message) -> None:
        # Log automod
        await self.log_event("automod", message.author, message.guild)

    @commands.Cog.listener()
    async def on_spam_detection(self, message: discord.Message) -> None:
        # Log spam detection
        await self.log_event("spam_detection", message.author, message.guild)

    @commands.Cog.listener()
    async def on_event(self,
                       event_name: str,
                       user: Union[discord.Member, discord.User],
                       guild: discord.Guild,
                       before: Optional[Union[discord.Member, discord.Message]] = None,
                       after: Optional[Union[discord.Member, discord.Message]] = None
                       ) -> None:
        # Log event
        await self.log_event(event_name, user, guild, before=before, after=after)
