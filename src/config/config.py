import json

# load json data
with open("config/config.json") as f:
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
