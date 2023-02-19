# Turninator

Turninator is a discord bot designed to provide moderation and utility functions to discord servers. It is written in Python and uses the discord.py library.

## Features

Turninator provides a wide range of features for discord servers, including:

- Moderation commands such as banning, kicking, and adding notes to users
- Utility commands such as getting user information, creating and deleting moderation channels, and synchronizing commands with the server
- Reply commands such as sending a list of links, generating AI responses for Ultrared's quotes, and sending an image file
- Logging of all moderation events and commands

## Installation

To install Turninator, you will need to have Python 3.6 or higher installed on your system.

1. Clone the repository: `git clone https://github.com/tairenfd/turninator.git`
2. Install the dependencies: `pip install -r requirements.txt`
3. Create a `config.json` file in the `config` directory, based on the `config.json.example` file.
4. Run the bot: `python src/bot.py` or install with `pip install ./` while in the main directory which contains the `setup.py` file.

## Usage

To use Turninator, you will need to have the `Manage Server` permission in the server you wish to use it in.

Once the bot is added to the server and running, you can use the `!help` command to view a list of available commands. You can also use the `!help <command>` command to get more information about a specific command.

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change or add.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
