from datetime import datetime

import discord
from discord.ext.commands import Bot

from commands.general import Replies
from commands.moderation import ModCommands
from config.config import discord_prefix, discord_token
from events.on_join_create import CreateChannels
from events.on_mod_action import ModActions
from utils.logging import get_logger, setup_logger

setup_logger("logs", "bot.log")

logger = get_logger("bot.log")


# set intents
class Turnbot(Bot):
    def __init__(self) -> None:
        # `Bot` instance is used because we are going
        # to be creating text-based commands.
        self._intents = discord.Intents.default()
        self._intents.message_content = True
        self._intents.bans = True
        self._intents.guilds = True
        self._intents.members = True
        self._intents.auto_moderation = True
        self.launchtime = {}
        super().__init__(command_prefix=discord_prefix, intents=self._intents)

    async def setup_hook(self) -> None:
        await self.add_cog(ModActions(self))
        logger.info("ModActions cog added")
        print("ModActions cog added")

        await self.add_cog(Replies(self))
        logger.info("Replies cog added")
        print("Replies cog added")

        await self.add_cog(ModCommands(self))
        logger.info("ModCommands cog added")
        print("ModCommands cog added")

        await self.add_cog(CreateChannels(self))
        logger.info("CreateChannels cog added")
        print("CreateChannels cog added")

    async def on_ready(self):
        logger.info(f"{self.user} logged in at {datetime.now()}")
        print(f"{self.user} logged in")
        await self.change_presence(
            activity=discord.Activity(type=discord.ActivityType.watching, name="ur mom")
        )
        for guild in self.guilds:
            self.launchtime[guild.name] = datetime.now()
            _launchtime = self.launchtime[guild.name].strftime("%m/%d/%Y, %H:%M:%S")
            logger.info(
                f"Bot status {self.status.name} in {guild.name} @ {_launchtime}"
            )
            print(f"Bot status {self.status.name} in {guild.name} @ {_launchtime}")


bot = Turnbot()


def main():
    bot.run(discord_token)


if __name__ == "__main__":
    main()
