from discord.ext import commands

from utils.logging import get_logger, setup_logger
from utils.tools import create_embed

setup_logger("logs", "mod_events.log")
logger = get_logger("mod_events.log")


class ModActions(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def log_event(self, event_name, user, guild):
        try:
            channel_name = f"turninator-{event_name}"
            channel = [c for c in guild.text_channels if c.name == channel_name][0]
            if channel is not None:
                embed = create_embed(
                    title=f"{event_name.title()} Event Triggered",
                    description=f"{user.mention} triggered a {event_name} event in {guild.name} : {channel.name}.",
                    colour=0x00FF00,
                )
                await channel.send(embed=embed)
            print(f"{event_name} event triggered by {user.mention} in {guild.name}")
            logger.info(
                f"{event_name} event triggered by {user.mention} in {guild.name}"
            )
        except Exception as error:
            print(error)

    @commands.Cog.listener()
    async def on_member_join(self, member):
        # Log user join
        await self.log_event("user_join", member, member.guild)
        # Send welcome message
        channel = self.bot.get_channel(member.guild.id)
        await channel.send(
            f"Welcome {member.mention} to {member.guild.name}! Please read {member.guild.rules_channel.mention} to get started."
        )

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        # Log user leave
        await self.log_event("user_leave", member, member.guild)

    @commands.Cog.listener()
    async def on_message_delete(self, message):
        # Log message delete
        await self.log_event("message_delete", message.author, message.guild)

    @commands.Cog.listener()
    async def on_message_edit(self, before, after):
        # Log message edit
        await self.log_event("message_edit", before.author, after.guild)

    @commands.Cog.listener()
    async def on_member_update(self, before, after):
        # Log role change
        if before.roles != after.roles:
            await self.log_event("role_change", after, after.guild)
        # Log nickname change
        if before.nick != after.nick:
            await self.log_event("nickname_change", after, after.guild)

    @commands.Cog.listener()
    async def on_mute(self, member):
        # Log mute
        await self.log_event("mute", member, member.guild)

    @commands.Cog.listener()
    async def on_unmute(self, member):
        # Log unmute
        await self.log_event("unmute", member, member.guild)

    @commands.Cog.listener()
    async def on_warn(self, member):
        # Log warn
        await self.log_event("warn", member, member.guild)

    @commands.Cog.listener()
    async def on_ban(self, member):
        # Log ban
        await self.log_event("ban", member, member.guild)

    @commands.Cog.listener()
    async def on_unban(self, member):
        # Log unban
        await self.log_event("unban", member, member.guild)

    @commands.Cog.listener()
    async def on_kick(self, member):
        # Log kick
        await self.log_event("kick", member, member.guild)

    @commands.Cog.listener()
    async def on_automod(self, message):
        # Log automod
        await self.log_event("automod", message.author, message.guild)

    @commands.Cog.listener()
    async def on_spam_detection(self, message):
        # Log spam detection
        await self.log_event("spam_detection", message.author, message.guild)

    @commands.Cog.listener()
    async def on_event(self, event_name, user, guild):
        # Log event
        await self.log_event(event_name, user, guild)
