from datetime import datetime
import discord
import openai
from discord.ext import commands
from config.config import openai_key, images_dir, ultra_dir
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

        CURRENT_PROMPT = f"{ctx.message.content.replace('!ultrared ', '')}"

        with open(f"{ultra_dir}ultra_prompt", "r") as file:
            file_contents = file.read()

        response = openai.Completion.create(
            model="text-davinci-003",
            prompt=f"""
                {file_contents}

                CURRENT_PROMPT: f'"{CURRENT_PROMPT}"'
            """,
            temperature=1,
            max_tokens=150,
        )

        with open(f"{ultra_dir}ultra_history", "a") as file:
            history_string = f'from: {ctx.author.name} -- ' + '{"prompt": ' + f'"{CURRENT_PROMPT} ->" ' + '"completion": ' + f'"{response}"' + '}'
            file.write(history_string)

        content = response.choices[0]["text"].replace('-> ', '').replace('completion: ', '').replace('Completion: ', '').strip()
        file = discord.File(f"{images_dir}ultrared.png", filename="ultrared.png")
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
            file=discord.File(f"{images_dir}tierlist.png", filename="tierlist.png")
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

    async def handle_error(self, ctx: commands.Context, error) -> None:
        """A function that handles errors for the Replies class"""
        if isinstance(error, commands.MissingPermissions):
            logger.info(
                f"Insufficient role privileges. {ctx.author.name} tried {ctx.command_failed}"
            )
            await ctx.send("Insufficient role privileges.")
        elif isinstance(error, discord.DiscordException):
            logger.info(f"Error: Could not send file. {error}")
            await ctx.send(f"Error: Could not send file. {error}")
        elif isinstance(error, Exception):
            logger.info(f"An unexpected error has occurred: {error}")
            await ctx.send(f"An unexpected error has occurred: {error}")
        elif isinstance(error, openai.error.APIError):
            logger.info(f"OpenAI API returned an API Error - {error}")
            await ctx.send(f"OpenAI API returned an API Error - {error}")
        elif isinstance(error, openai.error.APIConnectionError):
            logger.info(f"Failed to connect to OpenAI API - {error}")
            await ctx.send(f"Failed to connect to OpenAI API - {error}")
        elif isinstance(error, openai.error.RateLimitError):
            logger.info(f"OpenAI API request exceeded rate limit - {error}")
            await ctx.send(f"OpenAI API request exceeded rate limit - {error}")
        else:
            logger.info(f"Error: {error}")
            await ctx.send(f"Error: {error}")

    @turn.error
    async def turn_error(
        self, ctx: commands.Context, error
    ) -> None:
        await self.handle_error(ctx, error)

    @ultrared.error
    async def ultrared_error(
        self, ctx: commands.Context, error
    ) -> None:
        await self.handle_error(ctx, error)

    @tierlist.error
    async def tierlist_error(
        self, ctx: commands.Context, error
    ) -> None:
        await self.handle_error(ctx, error)

    @uptime.error
    async def uptime_error(
        self, ctx: commands.Context, error
    ) -> None:
        await self.handle_error(ctx, error)
