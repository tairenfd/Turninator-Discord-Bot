import json
from datetime import datetime

import discord
import requests

from utils.logging import get_logger

logger = get_logger("tools.log")


def create_embed(title: str, description: str, colour: int, **kwargs):
    """
    Creates a discord embed object to send
    :param title: The title of the embed
    :param description: The description of the embed
    :param colour: The colour of the embed
    :param kwargs: Optional arguments for the embed such as author (str),
        thumbnail (url), image (url), footer (str), and fields
        (list of tuples containing title (str), description (str),
        and boolean specifying if field should be inline)
    :return: discord.Embed
    """

    embed = discord.Embed(title=title, description=description, colour=colour)
    embed.timestamp = datetime.utcnow()

    # Add optional arguments
    if "author" in kwargs:
        embed.set_author(name=kwargs["author"])
    if "thumbnail" in kwargs:
        embed.set_thumbnail(url=kwargs["thumbnail"])
    if "image" in kwargs:
        embed.set_image(url=kwargs["image"])
    if "footer" in kwargs:
        embed.set_footer(text=kwargs["footer"])
    if "fields" in kwargs:
        if isinstance(kwargs["fields"], list):
            for field in kwargs["fields"]:
                embed.add_field(name=field[0], value=field[1], inline=field[2])
        else:
            raise TypeError("Fields must be a list of tuples")
    return embed


def parse_mentions(string):
    """
    Parse a string and return a list of mentions
    """
    mentions = []
    for word in string.split():
        if word.startswith("<@") and word.endswith(">"):
            mentions.append(word)
    return mentions


def format_dict_data(data):
    """
    Format data into a readable string
    """
    formatted_data = ""
    for key, value in data.items():
        formatted_data += f"{key}: {value}\n"
    return formatted_data


def get_discord_data(client, user_id):
    """
    Get user data from the Discord API
    Returns: -> dict
        'username': user.name,
        'discriminator': user.discriminator,
        'avatar': user.avatar_url

    """
    user = client.get_user(user_id)
    data = {
        "username": user.name,
        "discriminator": user.discriminator,
        "avatar": user.avatar_url,
    }
    return data


def get_other_data(url):
    """
    Get data from an external API
    """
    response = requests.get(url)
    data = response.json()
    return data


def create_backup(data):
    """
    Create a backup of given data
    """
    with open("backup.json", "w") as f:
        json.dump(data, f)


def get_time_difference(first_time, second_time):
    """
    Get the difference between two times
    """
    difference = first_time - second_time
    return difference


def get_timestamp(time):
    """
    Get a timestamp from a given time
    """
    timestamp = int(time.timestamp())
    return timestamp


def check_for_moderation_tables(cls):
    if cls in [
        "models.moderation_tables.AutomodHistory",
        "models.moderation_tables.KickHistory",
        "models.moderation_tables.WarningHistory",
        "models.moderation_tables.BanHistory",
        "models.moderation_tables.UnbanHistory",
        "models.moderation_tables.NotesHistory",
    ]:
        return True
    else:
        return False


def format_rows(rows, table=None):
    message = ""
    if type(rows) is not list:
        if table == "automod_history":
            message = f"[{rows.code}]<t:{get_timestamp(rows.timestamp)}:d>  - AUTOMOD -- {rows.reason}\n"
        # elif table == "ban_history":
        #     message += f"[{row[1]}]<t:{get_timestamp(row[-1])}:d> - <@{row[3]}> -- {ban time formatted back to str}{row[-2]}\n"
        elif table == "notes_history":
            message = f"[{rows.code}]<t:{get_timestamp(rows.timestamp)}:d> - <@{rows.moderator_id}> -- {rows.note}\n"
        else:
            message = f"[{rows.code}]<t:{get_timestamp(rows.timestamp)}:d> - <@{rows.moderator_id}> -- {rows.reason}\n"
    else:
        if table == "automod_history":
            for row in rows:
                message += f"[{row.code}]<t:{get_timestamp(row.timestamp)}:d>  - AUTOMOD -- {row.reason}\n"
        # elif table == "ban_history":
        #     for row in rows:
        #         message += f"[{row[1]}]<t:{get_timestamp(row[-1])}:d> - <@{row[3]}> -- {ban time formatted back to str}{row[-2]}\n"
        elif table == "notes_history":
            for row in rows:
                message += f"[{row.code}]<t:{get_timestamp(row.timestamp)}:d> - <@{row.moderator_id}> -- {row.note}\n"
        else:
            for row in rows:
                message += f"[{row.code}]<t:{get_timestamp(row.timestamp)}:d> - <@{row.moderator_id}> -- {row.reason}\n"
    return message
