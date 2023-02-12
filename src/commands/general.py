from datetime import datetime

import discord
import openai
from discord.ext import commands

from config.config import openai_key
from utils.logging import get_logger
from utils.tools import create_embed, get_time_difference

logger = get_logger("commands.log")

openai.api_key = openai_key


class Replies(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_command(name="turn", description="turn", with_app_command=True)
    async def turn(self, ctx: commands.Context) -> None:
        """A simple command that sends 'fuck u'"""
        await ctx.send("fuck u")

    @commands.hybrid_command(description="turns links", with_app_command=True)
    async def links(self, ctx: commands.Context):
        """A command that sends a list of Turn's links"""
        embed = create_embed(
            title="Turn's Links",
            description="",
            colour=discord.Color.blue(),
            fields=[
                ("Github", "https://www.github.com/tairenfd", False),
                ("Turns site", "https://www.tairenfd.xyz", False),
            ],
        )
        await ctx.send(embed=embed)

    @commands.hybrid_command(description="ultrared the pedo man", with_app_command=True)
    async def ultrared(self, ctx: commands.Context) -> None:
        """A command that generates AI response for Ultrared's quotes"""
        try:
            with open("src/commands/ultra_replies", "r") as file:
                file_contents = file.read()
        except Exception as e:
            logger.info(f"Something went wrong. Error: {e}")
            print(f"Something went wrong. Error: {e}")

        response = openai.Completion.create(
            model="text-davinci-003",
            prompt=f"""
                The quotes provided below are statements made by 'ultrared'. You will respond
                to all prompts as if they are statements being asked/said to
                'ultrared' by the user, and you will act as 'ultrared'. Use
                the quotes provided as a basis for your personality and belief
                system as much as possible,  but you dont have to be strictly
                bound by them.

                Quotes:
                    {file_contents}


                Prompt from user:
                    {ctx.message.content.replace('!ultrared', '')}

            """,
            temperature=1,
            max_tokens=2000,
        )
        content = response.choices[0]["text"]
        file = discord.File("src/images/ultrared.png", filename="ultrared.png")
        embed = create_embed(
            title="Ultrared AI",
            description=content,
            colour=discord.Color.red(),
            image="attachment://ultrared.png",
        )
        await ctx.send(embed=embed, file=file)

    @commands.hybrid_command(description="cock tierlist", with_app_command=True)
    async def tierlist(self, ctx: commands.Context) -> None:
        """A command that sends an image file"""
        await ctx.send(
            file=discord.File("src/images/tierlist.png", filename="tierlist.png")
        )

    @commands.hybrid_command(description="bot uptime", with_app_command=True)
    @commands.has_permissions(ban_members=True)
    async def uptime(self, ctx: commands.Context) -> None:
        """A command that shows the bot's uptime"""        
        delta_uptime = get_time_difference(
            datetime.now(), self.bot.launchtime[ctx.guild.name]
        )
        hours, remainder = divmod(int(delta_uptime.total_seconds()), 3600)
        minutes, seconds = divmod(remainder, 60)
        days, hours = divmod(hours, 24)
        await ctx.send(f"Running for {days}d, {hours}h, {minutes}m, {seconds}s")

    async def handle_error(self, ctx: commands.Context, error: Exception) -> None:
        """A function that handles errors for the Replies class"""
        if isinstance(error, commands.MissingPermissions):
            logger.INFO(
                f"Insufficient role privileges. {ctx.author.name} tried {ctx.command_failed}"
            )
            await ctx.send("Insufficient role privileges.")
        elif isinstance(error, discord.DiscordException):
            logger.INFO(f"Error: Could not send file. {error}")
            await ctx.send(f"Error: Could not send file. {error}")
        elif isinstance(error, Exception):
            logger.INFO(f"An unexpected error has occurred: {error}")
            await ctx.send(f"An unexpected error has occurred: {error}")

    @turn.error
    async def turn_error(
        self, ctx: commands.Context, error: Exception
    ) -> None:
        self.handle_error(ctx, error)

    @ultrared.error
    async def ultrared_error(
        self, ctx: commands.Context, error: Exception
    ) -> None:
        self.handle_error(ctx, error)

    @tierlist.error
    async def tierlist_error(
        self, ctx: commands.Context, error: Exception
    ) -> None:
        self.handle_error(ctx, error)

    @uptime.error
    async def uptime_error(
        self, ctx: commands.Context, error: Exception
    ) -> None:
        self.handle_error(ctx, error)
