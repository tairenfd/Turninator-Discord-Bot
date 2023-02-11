import asyncio

import discord

from utils.logging import get_logger, setup_logger

setup_logger("logs", "mod_events.log")
logger = get_logger("mod_events.log")


async def create_mod_channels(guild):
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
    msg_edit_channel = await guild.create_text_channel(
        "turninator-msg_edit",
        overwrites={
            default_role: default_overwrite,
            moderator_role: moderator_overwrite,
            sub_mod_role: moderator_overwrite,
            bot_role: bot_overwrite,
        },
        reason="Moderation channel for message edit logging",
    )
    await asyncio.sleep(1)
    mute_channel = await guild.create_text_channel(
        "turninator-mute",
        overwrites={
            default_role: default_overwrite,
            moderator_role: moderator_overwrite,
            sub_mod_role: moderator_overwrite,
            bot_role: bot_overwrite,
        },
        reason="Moderation channel for mute logging",
    )
    await asyncio.sleep(1)
    warn_channel = await guild.create_text_channel(
        "turninator-warn",
        overwrites={
            default_role: default_overwrite,
            moderator_role: moderator_overwrite,
            sub_mod_role: moderator_overwrite,
            bot_role: bot_overwrite,
        },
        reason="Moderation channel for warn logging",
    )
    await asyncio.sleep(1)
    ban_channel = await guild.create_text_channel(
        "turninator-ban",
        overwrites={
            default_role: default_overwrite,
            moderator_role: moderator_overwrite,
            sub_mod_role: moderator_overwrite,
            bot_role: bot_overwrite,
        },
        reason="Moderation channel for ban logging",
    )
    await asyncio.sleep(1)
    kick_channel = await guild.create_text_channel(
        "turninator-kick",
        overwrites={
            default_role: default_overwrite,
            moderator_role: moderator_overwrite,
            sub_mod_role: moderator_overwrite,
            bot_role: bot_overwrite,
        },
        reason="Moderation channel for kick logging",
    )
    await asyncio.sleep(1)
    unban_channel = await guild.create_text_channel(
        "turninator-unban",
        overwrites={
            default_role: default_overwrite,
            moderator_role: moderator_overwrite,
            sub_mod_role: moderator_overwrite,
            bot_role: bot_overwrite,
        },
        reason="Moderation channel for unban logging",
    )
    await asyncio.sleep(1)
    unmute_channel = await guild.create_text_channel(
        "turninator-unmute",
        overwrites={
            default_role: default_overwrite,
            moderator_role: moderator_overwrite,
            sub_mod_role: moderator_overwrite,
            bot_role: bot_overwrite,
        },
        reason="Moderation channel for unmute logging",
    )
    await asyncio.sleep(1)
    user_join_channel = await guild.create_text_channel(
        "turninator-user_join",
        overwrites={
            default_role: default_overwrite,
            moderator_role: moderator_overwrite,
            sub_mod_role: moderator_overwrite,
            bot_role: bot_overwrite,
        },
        reason="Moderation channel for user join logging",
    )
    await asyncio.sleep(1)
    user_leave_channel = await guild.create_text_channel(
        "turninator-user_leave",
        overwrites={
            default_role: default_overwrite,
            moderator_role: moderator_overwrite,
            sub_mod_role: moderator_overwrite,
            bot_role: bot_overwrite,
        },
        reason="Moderation channel for user leave logging",
    )
    await asyncio.sleep(1)
    message_delete_channel = await guild.create_text_channel(
        "turninator-message_delete",
        overwrites={
            default_role: default_overwrite,
            moderator_role: moderator_overwrite,
            sub_mod_role: moderator_overwrite,
            bot_role: bot_overwrite,
        },
        reason="Moderation channel for message delete logging",
    )
    await asyncio.sleep(1)
    message_edit_channel = await guild.create_text_channel(
        "turninator-message_edit",
        overwrites={
            default_role: default_overwrite,
            moderator_role: moderator_overwrite,
            sub_mod_role: moderator_overwrite,
            bot_role: bot_overwrite,
        },
        reason="Moderation channel for message edit logging",
    )
    await asyncio.sleep(1)
    role_change_channel = await guild.create_text_channel(
        "turninator-role_change",
        overwrites={
            default_role: default_overwrite,
            moderator_role: moderator_overwrite,
            sub_mod_role: moderator_overwrite,
            bot_role: bot_overwrite,
        },
        reason="Moderation channel for role change logging",
    )
    await asyncio.sleep(1)
    nickname_change_channel = await guild.create_text_channel(
        "turninator-nickname_change",
        overwrites={
            default_role: default_overwrite,
            moderator_role: moderator_overwrite,
            sub_mod_role: moderator_overwrite,
            bot_role: bot_overwrite,
        },
        reason="Moderation channel for nickname change logging",
    )
    await asyncio.sleep(1)
    automod_channel = await guild.create_text_channel(
        "turninator-automod",
        overwrites={
            default_role: default_overwrite,
            moderator_role: moderator_overwrite,
            sub_mod_role: moderator_overwrite,
            bot_role: bot_overwrite,
        },
        reason="Moderation channel for automod logging",
    )
    await asyncio.sleep(1)
    spam_detection_channel = await guild.create_text_channel(
        "turninator-spam_detection",
        overwrites={
            default_role: default_overwrite,
            moderator_role: moderator_overwrite,
            sub_mod_role: moderator_overwrite,
            bot_role: bot_overwrite,
        },
        reason="Moderation channel for spam detection logging",
    )

    # Set permissions
    await msg_edit_channel.set_permissions(
        guild.me, read_messages=True, send_messages=True
    )
    await mute_channel.set_permissions(guild.me, read_messages=True, send_messages=True)
    await warn_channel.set_permissions(guild.me, read_messages=True, send_messages=True)
    await ban_channel.set_permissions(guild.me, read_messages=True, send_messages=True)
    await kick_channel.set_permissions(guild.me, read_messages=True, send_messages=True)
    await unban_channel.set_permissions(
        guild.me, read_messages=True, send_messages=True
    )
    await unmute_channel.set_permissions(
        guild.me, read_messages=True, send_messages=True
    )
    await user_join_channel.set_permissions(
        guild.me, read_messages=True, send_messages=True
    )
    await user_leave_channel.set_permissions(
        guild.me, read_messages=True, send_messages=True
    )
    await message_delete_channel.set_permissions(
        guild.me, read_messages=True, send_messages=True
    )
    await message_edit_channel.set_permissions(
        guild.me, read_messages=True, send_messages=True
    )
    await role_change_channel.set_permissions(
        guild.me, read_messages=True, send_messages=True
    )
    await nickname_change_channel.set_permissions(
        guild.me, read_messages=True, send_messages=True
    )
    await automod_channel.set_permissions(
        guild.me, read_messages=True, send_messages=True
    )
    await spam_detection_channel.set_permissions(
        guild.me, read_messages=True, send_messages=True
    )

    logger.info(f"Moderation channel msg_edit created in {guild.name} (id: {guild.id})")
    logger.info(f"Moderation channel mute created in {guild.name} (id: {guild.id})")
    logger.info(f"Moderation channel warn created in {guild.name} (id: {guild.id})")
    logger.info(f"Moderation channel ban created in {guild.name} (id: {guild.id})")
    logger.info(f"Moderation channel kick created in {guild.name} (id: {guild.id})")
    logger.info(f"Moderation channel unban created in {guild.name} (id: {guild.id})")
    logger.info(f"Moderation channel unmute created in {guild.name} (id: {guild.id})")
    logger.info(
        f"Moderation channel user_join created in {guild.name} (id: {guild.id})"
    )
    logger.info(
        f"Moderation channel user_leave created in {guild.name} (id: {guild.id})"
    )
    logger.info(
        f"Moderation channel message_delete created in {guild.name} (id: {guild.id})"
    )
    logger.info(
        f"Moderation channel message_edit created in {guild.name} (id: {guild.id})"
    )
    logger.info(
        f"Moderation channel role_change created in {guild.name} (id: {guild.id})"
    )
    logger.info(
        f"Moderation channel nickname_change created in {guild.name} (id: {guild.id})"
    )
    logger.info(f"Moderation channel automod created in {guild.name} (id: {guild.id})")
    logger.info(
        f"Moderation channel spam_detection created in {guild.name} (id: {guild.id})"
    )
