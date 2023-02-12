import asyncio
import unittest
from datetime import datetime
from unittest.mock import patch

import discord

from bot import Turnbot
from commands.general import Replies
from config.config import discord_prefix, discord_token
from utils.logging import get_logger, setup_logger


class TestTurnbot(unittest.TestCase):
    def setUp(self):
        setup_logger("logs", "bot.log")
        setup_logger("logs", "commands.py")
        setup_logger("logs", "tools.log")
        self.logger = get_logger("bot.log")
        self.bot = Turnbot()

    @patch("discord.Client.login")
    def test_on_ready(self, mock_login) -> None:
        '''
        This method tests the on_ready method of Turnbot class which is responsible for setting up the bot when it is ready to receive messages.

        Parameters:
            - mock_login: a patch object that mocks the Client.login method.
        '''
        mock_login.return_value = None
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(self.bot.on_ready())
        mock_login.assert_called_once_with(discord_token)
        self.assertEqual(self.logger.info.call_count, 1)
        self.assertEqual(self.bot.launchtime, {"Test Guild": datetime.now()})
        self.assertEqual(self.bot.user.activity.name, "ur mom")
        self.assertEqual(self.bot.user.activity.type, discord.ActivityType.watching)
        self.assertEqual(self.bot._intents.message_content, True)
        self.assertEqual(self.bot._intents.bans, True)
        self.assertEqual(self.bot.command_prefix, discord_prefix)
        self.assertEqual(self.bot.tree.copy_global_to.call_count, 1)
        self.assertEqual(self.bot.tree.sync.call_count, 1)
        self.assertEqual(self.logger.info.call_count, 1)

    @patch("discord.Client.login")
    def test_setup_hook(self, mock_login) -> None:
        '''
        This method tests the setup_hook method of Turnbot class which is responsible for setting up the bot after the bot is logged in and connected to Discord.

        Parameters:
            - mock_login: a patch object that mocks the Client.login method.
        '''
        mock_login.return_value = None
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(self.bot.setup_hook())
        self.assertEqual(mock_login.call_count, 1)
        self.assertEqual(self.bot.cogs, {"Replies": Replies(self.bot)})


if __name__ == "__main__":
    unittest.main()
