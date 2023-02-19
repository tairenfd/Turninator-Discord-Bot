import json

'''
    discord_token: 
        a string representing the Discord bot token, required to authenticate
        the bot with Discord's API.
    discord_prefix:
        a string representing the prefix that the bot should listen for in
        messages. This allows users to issue commands to the bot.
    discord_admin:
        a string representing the name of the role that grants administrative
        privileges on the Discord server.
    discord_mod:
        a string representing the name of the role that grants moderator
        privileges on the Discord server.
    sql_host:
        a string representing the hostname of the SQL database to be used.
    sql_user:
        a string representing the username to be used for the SQL database
        connection.
    sql_password:
        a string representing the password to be used for the SQL database
        connection.
    sql_database:
        a string representing the name of the SQL database to be used.
    openai_key:
        a string representing the API key to be used for accessing the
        OpenAI API.
'''

# load json data
with open("/home/central-turn/discord_services/turnbot/src/config/config.json") as f:
    data = json.load(f)

# assign data to variables
discord_token = data["discord"]["token"]
discord_prefix = data["discord"]["prefix"]
discord_admin = data["discord"]["admin_role"]
discord_mod = data["discord"]["mod_role"]

sql_host = data["database"]["host"]
sql_user = data["database"]["user"]
sql_password = data["database"]["password"]
sql_database = data["database"]["database"]

openai_key = data["openai"]["openai_key"]

images_dir = data["dirs"]["images_dir"]
ultra_dir = data["dirs"]["ultra_dir"]
