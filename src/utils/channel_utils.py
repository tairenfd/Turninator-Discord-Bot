import discord
from utils.logging import get_logger, setup_logger

setup_logger("logs", "mod_events.log")
logger = get_logger("mod_events.log")


async def create_mod_channels(guild: discord.Guild) -> None:
    '''
    Creates moderation channels in a Discord guild

    Parameters:
        guild: Discord guild object
    Return:
        None
    '''
    default_role = guild.default_role
    moderator_role = None
    sub_mod_role = None
    bot_role = None
    for role in guild.roles:
        print(role)
        if role.name.lower() == "turn":
            logger.info(f"{role.name} found")
            moderator_role = role
        elif role.name.lower() == "wranglers":
            logger.info(f"{role.name} found")
            sub_mod_role = role
        elif role.is_bot_managed and role.name.lower() == "turninator":
            logger.info(f"{role.name} found")
            bot_role = role
        if moderator_role and sub_mod_role and bot_role:
            break
    if not moderator_role:
        print("no mod role found")
        return
    default_overwrite = discord.PermissionOverwrite(view_channel=False)
    moderator_overwrite = discord.PermissionOverwrite(
        read_messages=True,
        send_messages=True,
        read_message_history=True,
        view_channel=True,
    )
    bot_overwrite = discord.PermissionOverwrite(
        read_messages=True,
        send_messages=True,
        read_message_history=True,
        view_channel=True,
        manage_guild=True,
        embed_links=True,
        attach_files=True,
    )

    # Create category
    category = await guild.create_category(
        "TURNINATOR Channels",
        overwrites={
            default_role: default_overwrite,
            moderator_role: moderator_overwrite,
            sub_mod_role: moderator_overwrite,
            bot_role: bot_overwrite,
        },
        reason="Moderation channels",
    )

    # Create channels in category
    for channel_name in [
        "turninator-ban",
        "turninator-unban",
        "turninator-kick",
        "turninator-warn",
        "turninator-mute",
        "turninator-unmute",
        "turninator-user_join",
        "turninator-user_leave",
        "turninator-message_delete",
        "turninator-message_edit",
        "turninator-role_change",
        "turninator-nickname_change",
        "turninator-automod",
        "turninator-spam_detection",
    ]:
        channel = await category.create_text_channel(
            channel_name,
            overwrites={
                default_role: default_overwrite,
                moderator_role: moderator_overwrite,
                sub_mod_role: moderator_overwrite,
                bot_role: bot_overwrite,
            },
            reason=f"Moderation channel for {channel_name.replace('turninator-', '')} actions",
        )
        await channel.set_permissions(guild.me, read_messages=True, send_messages=True)

        logger.info(
            f"Moderation channel {channel_name} created in {guild.name} (id: {guild.id})"
        )


async def delete_mod_channels(guild: discord.Guild) -> None:
    '''
    Deletes moderation channels and the moderation channel category in a
        Discord guild

    Function annotations:
        - Parameter guild: Discord guild object
        - Return: None
    '''
    category = discord.utils.get(guild.categories, name="Moderation Channels")
    if category is not None:
        for channel in category.channels:
            await channel.delete(reason="Deleting moderation channel")
        await category.delete(reason="Deleting moderation channel category")
        logger.info(
            f"Moderation channel category deleted in {guild.name} (id: {guild.id})"
        )
    else:
        logger.info(
            f"Moderation channel category not found in {guild.name} (id: {guild.id})"
        )
