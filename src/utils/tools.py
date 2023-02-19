import json
from typing import Union, Optional
from datetime import datetime, timedelta
import discord
from discord import Colour
import requests
from utils.database.read import get_last_BWK_from_all_tables_by_user
from utils.logging import get_logger

logger = get_logger("tools.log")


def create_embed(
    title: str,
    description: str = None,
    colour: Optional[Union[int, Colour]] = None,
    **kwargs,
) -> discord.Embed:
    """
    Creates a discord embed object to send

    Parameters:
        title: The title of the embed
        description: The description of the embed
        colour: The colour of the embed
        kwargs: Optional arguments for the embed such as author (str),
            thumbnail (url), image (url), footer (str), and fields
            (list of tuples containing title (str), description (str),
            and boolean specifying if field should be inline)
    Return:
        discord.Embed
    """

    embed = discord.Embed(title=title, description=description, colour=colour)
    embed.timestamp = datetime.utcnow()

    # Add optional arguments
    if "author" in kwargs:
        if "author_icon" in kwargs:
            embed.set_author(name=kwargs["author"], icon_url=kwargs["author_icon"])
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


def parse_mentions(string: str) -> list:
    """
    Parse a string and return a list of mentions
    """
    mentions = []
    for word in string.split():
        if word.startswith("<@") and word.endswith(">"):
            mentions.append(word)
    return mentions


def format_dict_data(data) -> str:
    """
    Format data into a readable string
    """
    formatted_data = ""
    for key, value in data.items():
        formatted_data += f"{key}: {value}\n"
    return formatted_data


def get_discord_data(client, user_id) -> dict:
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


def get_other_data(url) -> dict:
    """
    Get data from an external API
    """
    response = requests.get(url)
    data = response.json()
    return data


def create_backup(data) -> None:
    """
    Create a backup of given data
    """
    with open("backup.json", "w") as f:
        json.dump(data, f)


def get_time_difference(first_time, second_time) -> timedelta:
    """
    Get the difference between two times
    """
    difference = first_time - second_time
    return difference


def get_timestamp(time) -> int:
    """
    Get a timestamp from a given time
    """
    timestamp = int(time.timestamp())
    return timestamp


def check_for_moderation_tables(cls) -> bool:
    """
    Checks for a given string in a list of moderation tables
    """
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


def format_rows(rows, table=None) -> str:
    """
    Formats rows for different moderation tables
    """
    message = ""
    flag = False
    if type(rows) is not list:
        if table == "automod_history":
            message = f"[{rows.code}] <t:{get_timestamp(rows.timestamp)}:d>  - AUTOMOD -- {rows.reason}\n"
        elif table == "ban_history":
            message += f"[{rows.code}] <t:{get_timestamp(rows.timestamp)}:d> - <@{rows.moderator_id}> -- (*{format_ban_time(rows.ban_time)}*) {rows.reason}\n"
        elif table == "notes_history":
            message = f"[{rows.code}] <t:{get_timestamp(rows.timestamp)}:d> - <@{rows.moderator_id}> -- {rows.note}\n"
        else:
            message = f"[{rows.code}] <t:{get_timestamp(rows.timestamp)}:d> - <@{rows.moderator_id}> -- {rows.reason}\n"
    else:
        for row in rows:
            if get_last_BWK_from_all_tables_by_user(row.user_id, row.server_id) is not None:
                if row.code == get_last_BWK_from_all_tables_by_user(row.user_id, row.server_id).code:
                    flag = True
                else:
                    flag = False
            else:
                flag = False
            if table == "automod_history":
                if flag:
                    message += f"[**{row.code}**] <t:{get_timestamp(row.timestamp)}:d>  - AUTOMOD -- {row.reason}\n"
                else:
                    message += f"[{row.code}] <t:{get_timestamp(row.timestamp)}:d>  - AUTOMOD -- {row.reason}\n"
            elif table == "ban_history":
                if flag:
                    message += f"[**{row.code}**] <t:{get_timestamp(row.timestamp)}:d> - <@{row.moderator_id}> -- (*{format_ban_time(row.ban_time)}*) {row.reason}\n"
                else:
                    message += f"[{row.code}] <t:{get_timestamp(row.timestamp)}:d> - <@{row.moderator_id}> -- (*{format_ban_time(row.ban_time)}*) {row.reason}\n"
            elif table == "notes_history":
                if flag:
                    message += f"[**{row.code}**] <t:{get_timestamp(row.timestamp)}:d> - <@{row.moderator_id}> -- {row.note}\n"
                else:
                    message += f"[{row.code}] <t:{get_timestamp(row.timestamp)}:d> - <@{row.moderator_id}> -- {row.note}\n"
            else:
                if flag:
                    message += f"[**{row.code}**] <t:{get_timestamp(row.timestamp)}:d> - <@{row.moderator_id}> -- {row.reason}\n"
                else:
                    message += f"[{row.code}] <t:{get_timestamp(row.timestamp)}:d> - <@{row.moderator_id}> -- {row.reason}\n"
    return message


async def set_default_permissions(server) -> None:
    """
    Sets default permissions for server roles
    """
    moderator_permissions = discord.Permissions(
        add_reactions=True,
        administrator=False,
        attach_files=True,
        ban_members=True,
        change_nickname=True,
        connect=True,
        create_instant_invite=False,
        create_private_threads=False,
        create_public_threads=True,
        deafen_members=True,
        embed_links=True,
        kick_members=True,
        manage_channels=False,
        manage_emojis=False,
        manage_emojis_and_stickers=False,
        manage_events=False,
        manage_guild=False,
        manage_messages=True,
        manage_nicknames=False,
        manage_permissions=False,
        manage_roles=False,
        manage_threads=False,
        manage_webhooks=False,
        mention_everyone=False,
        moderate_members=True,
        move_members=True,
        mute_members=True,
        priority_speaker=False,
        read_message_history=True,
        read_messages=True,
        request_to_speak=False,
        send_messages=True,
        send_messages_in_threads=True,
        send_tts_messages=False,
        speak=True,
        stream=True,
        use_application_commands=True,
        use_embedded_activities=True,
        use_external_emojis=True,
        use_external_stickers=True,
        use_voice_activation=True,
        view_channel=True,
        view_audit_log=True,
        view_guild_insights=False
    )

    general_permissions = discord.Permissions(
        add_reactions=True,
        administrator=False,
        attach_files=True,
        ban_members=False,
        change_nickname=True,
        connect=True,
        create_instant_invite=False,
        create_private_threads=False,
        create_public_threads=False,
        deafen_members=False,
        embed_links=True,
        kick_members=False,
        manage_channels=False,
        manage_emojis=False,
        manage_emojis_and_stickers=False,
        manage_events=False,
        manage_guild=False,
        manage_messages=False,
        manage_nicknames=False,
        manage_permissions=False,
        manage_roles=False,
        manage_threads=False,
        manage_webhooks=False,
        mention_everyone=False,
        moderate_members=False,
        move_members=False,
        mute_members=False,
        priority_speaker=False,
        read_message_history=True,
        read_messages=True,
        request_to_speak=False,
        send_messages=True,
        send_messages_in_threads=True,
        send_tts_messages=False,
        speak=True,
        stream=True,
        use_application_commands=True,
        use_embedded_activities=True,
        use_external_emojis=True,
        use_external_stickers=True,
        use_voice_activation=True,
        view_channel=True,
        view_audit_log=False,
        view_guild_insights=False
    )

    turn_role = discord.utils.get(server.roles, name="turn")
    wranglers_role = discord.utils.get(server.roles, name="wranglers")
    friends_role = discord.utils.get(server.roles, name="friends")
    everyone_role = discord.utils.get(server.roles, name="@everyone")

    await wranglers_role.edit(permissions=moderator_permissions)
    await friends_role.edit(permissions=general_permissions)
    await everyone_role.edit(permissions=general_permissions)

    # Restrict normal users from entering nsfw channels
    for role in server.roles:
        if role != turn_role and role != wranglers_role:
            for channel in server.channels:
                if channel.is_nsfw():
                    if role == friends_role:
                        await channel.set_permissions(
                            target=friends_role,
                            view_channel=True
                        )
                    elif role == everyone_role:
                        await channel.set_permissions(
                            target=everyone_role,
                            view_channel=False
                        )


def get_permission_fields(user) -> discord.Embed:
    """
    Get user permissions and returns discord.Embed
    """
    perms = [perm for perm in user.guild_permissions]
    fields = []

    for perm in perms:
        if perm[1]:
            fields.append((perm[0], "\u2705", False))
        else:
            fields.append((perm[0], "\u274C", False))

    return fields


def parse_ban_time(time_string: str) -> int:
    """
    Parse ban time string into seconds
    """
    unit = time_string[-1]
    num = int(time_string[:-1])
    if unit == "s":
        ban_time = num
    elif unit == "m":
        ban_time = num * 60
    elif unit == "h":
        ban_time = num * 3600
    elif unit == "d":
        ban_time = num * 86400
    elif unit == "w":
        ban_time = num * 86400 * 7
    elif unit == "M":
        ban_time = num * 86400 * 30
    elif unit == "y":
        ban_time = num * 86400 * 30 * 12
    elif time_string in ["p", "perm", "perma", "permanent"]:
        ban_time = -1
    else:
        raise ValueError("Invalid ban time unit.")
    return ban_time


def format_ban_time(ban_time: int) -> str:
    """
    Format ban time in seconds to human-readable time
    """
    if ban_time == -1:
        return "permanent"
    elif ban_time >= 86400 * 30 * 12:
        return f"{ban_time // 86400 // 30 // 12}y"
    elif ban_time >= 86400 * 30:
        return f"{ban_time // 86400 // 30}M"
    elif ban_time >= 86400 * 7:
        return f"{ban_time // 86400 // 7}w"
    elif ban_time >= 86400:
        return f"{ban_time // 86400}d"
    elif ban_time >= 3600:
        return f"{ban_time // 3600}h"
    elif ban_time >= 60:
        return f"{ban_time // 60}m"
    else:
        return f"{ban_time}s"


async def bulk_delete(self, ctx, limit, user) -> list:
    """
    Bulk delete messages by a given user in a channel
    """
    deleted = []
    async for message in ctx.channel.history(limit=limit):
        if message.author == user:
            deleted.append(message)
            if len(deleted) == limit:
                break
    await ctx.channel.delete_messages(deleted)
    return deleted
