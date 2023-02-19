from models.moderation_tables import (
    AutomodHistory,
    BanHistory,
    KickHistory,
    NotesHistory,
    UnbanHistory,
    WarningHistory,
)
from utils.database.session import get_session


def get_rows_from_user_id_and_server_id(
    user_id: str, server_id: str, table: str
) -> list:
    """
    Retrieve rows from a specific table in the database for a given user ID 
        and server ID.
    
    Parameters:
        user_id (str): The user ID to search for in the table.
        server_id (str): The server ID to search for in the table.
        table (str): The name of the table to search in.
    Returns:
        list: A list of rows matching the search criteria.
    """
    try:
        session = get_session()
        with session:
            if table == "automod_history":
                result = (
                    session.query(AutomodHistory)
                    .filter(
                        AutomodHistory.user_id == user_id,
                        AutomodHistory.server_id == server_id,
                    )
                    .all()
                )
            elif table == "kick_history":
                result = (
                    session.query(KickHistory)
                    .filter(
                        KickHistory.user_id == user_id,
                        KickHistory.server_id == server_id,
                    )
                    .all()
                )
            elif table == "warning_history":
                result = (
                    session.query(WarningHistory)
                    .filter(
                        WarningHistory.user_id == user_id,
                        WarningHistory.server_id == server_id,
                    )
                    .all()
                )
            elif table == "ban_history":
                result = (
                    session.query(BanHistory)
                    .filter(
                        BanHistory.user_id == user_id, BanHistory.server_id == server_id
                    )
                    .all()
                )
            elif table == "unban_history":
                result = (
                    session.query(UnbanHistory)
                    .filter(
                        UnbanHistory.user_id == user_id,
                        UnbanHistory.server_id == server_id,
                    )
                    .all()
                )
            elif table == "notes_history":
                result = (
                    session.query(NotesHistory)
                    .filter(
                        NotesHistory.user_id == user_id,
                        NotesHistory.server_id == server_id,
                    )
                    .all()
                )
    except Exception as error:
        # TODO: error handling logic
        raise error
    finally:
        session.close()
    return result


def get_rows_from_user_id(user_id: str, table: str) -> list:
    """
    Retrieve rows from a specific table in the database for a given user ID.
    
    Parameters:
        user_id (str): The user ID to search for in the table.
        table (str): The name of the table to search in.
    Returns:
        list: A list of rows matching the search criteria.
    """

    try:
        session = get_session()
        with session:
            if table == "automod_history":
                result = (
                    session.query(AutomodHistory)
                    .filter(AutomodHistory.user_id == user_id)
                    .all()
                )
            elif table == "kick_history":
                result = (
                    session.query(KickHistory)
                    .filter(KickHistory.user_id == user_id)
                    .all()
                )
            elif table == "warning_history":
                result = (
                    session.query(WarningHistory)
                    .filter(WarningHistory.user_id == user_id)
                    .all()
                )
            elif table == "ban_history":
                result = (
                    session.query(BanHistory)
                    .filter(BanHistory.user_id == user_id)
                    .all()
                )
            elif table == "unban_history":
                result = (
                    session.query(UnbanHistory)
                    .filter(UnbanHistory.user_id == user_id)
                    .all()
                )
            elif table == "notes_history":
                result = (
                    session.query(NotesHistory)
                    .filter(NotesHistory.user_id == user_id)
                    .all()
                )
    except Exception as error:
        # TODO: error handling logic
        raise error
    finally:
        session.close()
    return result


def get_last_row_from_user_id_and_server_id(user_id: str, server_id: str, table: str):
    """
    Retrieve the last row from a specific table in the database for a given
        user ID and server ID.

    Parameters:
        user_id (str): The user ID to search for in the table.
        server_id (str): The server ID to search for in the table.
        table (str): The name of the table to search in.
    Returns:
        object: The last row matching the search criteria.
    """
    try:
        session = get_session()
        with session:
            if table == "automod_history":
                result = (
                    session.query(AutomodHistory)
                    .filter(
                        AutomodHistory.user_id == user_id,
                        AutomodHistory.server_id == server_id,
                    )
                    .order_by(AutomodHistory.timestamp.desc())
                    .first()
                )
            elif table == "kick_history":
                result = (
                    session.query(KickHistory)
                    .filter(
                        KickHistory.user_id == user_id,
                        KickHistory.server_id == server_id,
                    )
                    .order_by(KickHistory.timestamp.desc())
                    .first()
                )
            elif table == "warning_history":
                result = (
                    session.query(WarningHistory)
                    .filter(
                        WarningHistory.user_id == user_id,
                        WarningHistory.server_id == server_id,
                    )
                    .order_by(WarningHistory.timestamp.desc())
                    .first()
                )
            elif table == "ban_history":
                result = (
                    session.query(BanHistory)
                    .filter(
                        BanHistory.user_id == user_id, BanHistory.server_id == server_id
                    )
                    .order_by(BanHistory.timestamp.desc())
                    .first()
                )
            elif table == "unban_history":
                result = (
                    session.query(UnbanHistory)
                    .filter(
                        UnbanHistory.user_id == user_id,
                        UnbanHistory.server_id == server_id,
                    )
                    .order_by(UnbanHistory.timestamp.desc())
                    .first()
                )
            elif table == "notes_history":
                result = (
                    session.query(NotesHistory)
                    .filter(
                        NotesHistory.user_id == user_id,
                        NotesHistory.server_id == server_id,
                    )
                    .order_by(NotesHistory.timestamp.desc())
                    .first()
                )
    except Exception as error:
        # TODO: error handling logic
        raise error
    finally:
        session.close()
    return result


def get_last_row_from_user_id(user_id: str, table: str):
    """
    Retrieve the last row from a specific table in the database for a given
        user ID.

    Parameters:
        user_id (str): The user ID to search for in the table.
        table (str): The name of the table to search in.
    Returns:
        object: The last row matching the search criteria.
    """
    try:
        session = get_session()
        with session:
            if table == "automod_history":
                result = (
                    session.query(AutomodHistory)
                    .filter(AutomodHistory.user_id == user_id)
                    .order_by(AutomodHistory.timestamp.desc())
                    .first()
                )
            elif table == "kick_history":
                result = (
                    session.query(KickHistory)
                    .filter(KickHistory.user_id == user_id)
                    .order_by(KickHistory.timestamp.desc())
                    .first()
                )
            elif table == "warning_history":
                result = (
                    session.query(WarningHistory)
                    .filter(WarningHistory.user_id == user_id)
                    .order_by(WarningHistory.timestamp.desc())
                    .first()
                )
            elif table == "ban_history":
                result = (
                    session.query(BanHistory)
                    .filter(BanHistory.user_id == user_id)
                    .order_by(BanHistory.timestamp.desc())
                    .first()
                )
            elif table == "unban_history":
                result = (
                    session.query(UnbanHistory)
                    .filter(UnbanHistory.user_id == user_id)
                    .order_by(UnbanHistory.timestamp.desc())
                    .first()
                )
            elif table == "notes_history":
                result = (
                    session.query(NotesHistory)
                    .filter(NotesHistory.user_id == user_id)
                    .order_by(NotesHistory.timestamp.desc())
                    .first()
                )
    except Exception as error:
        # TODO: error handling logic
        raise error
    finally:
        session.close()
    return result


def get_last_row_from_all_tables():
    """
    Retrieve the last row from all tables in the database.

    Returns:
        object: The last row from all tables in the database.
    """

    try:
        session = get_session()
        with session:
            automod_row = (
                session.query(AutomodHistory)
                .order_by(AutomodHistory.timestamp.desc())
                .first()
            )
            kick_row = (
                session.query(KickHistory)
                .order_by(KickHistory.timestamp.desc())
                .first()
            )
            warning_row = (
                session.query(WarningHistory)
                .order_by(WarningHistory.timestamp.desc())
                .first()
            )
            ban_row = (
                session.query(BanHistory).order_by(BanHistory.timestamp.desc()).first()
            )
            unban_row = (
                session.query(UnbanHistory)
                .order_by(UnbanHistory.timestamp.desc())
                .first()
            )
            notes_row = (
                session.query(NotesHistory)
                .order_by(NotesHistory.timestamp.desc())
                .first()
            )
    except Exception as error:
        # Add error handling logic here
        raise error
    finally:
        session.close()

    if automod_row:
        last_row = automod_row
    else:
        last_row = None

    if kick_row and (last_row is None or kick_row.timestamp > last_row.timestamp):
        last_row = kick_row
    if warning_row and (last_row is None or warning_row.timestamp > last_row.timestamp):
        last_row = warning_row
    if ban_row and (last_row is None or ban_row.timestamp > last_row.timestamp):
        last_row = ban_row
    if unban_row and (last_row is None or unban_row.timestamp > last_row.timestamp):
        last_row = unban_row
    if notes_row and (last_row is None or notes_row.timestamp > last_row.timestamp):
        last_row = notes_row

    return last_row


def get_last_row_from_all_tables_by_user(user_id: str):
    """
    Retrieve the last row from all tables in the database for a given user ID.

    Parameters:
        user_id (str): The user ID to search for in the tables.
    Returns:
        object: The last row matching the search criteria.
    """

    try:
        session = get_session()
        with session:
            automod_row = (
                session.query(AutomodHistory)
                .filter(AutomodHistory.user_id == user_id)
                .order_by(AutomodHistory.timestamp.desc())
                .first()
            )
            kick_row = (
                session.query(KickHistory)
                .filter(KickHistory.user_id == user_id)
                .order_by(KickHistory.timestamp.desc())
                .first()
            )
            warning_row = (
                session.query(WarningHistory)
                .filter(WarningHistory.user_id == user_id)
                .order_by(WarningHistory.timestamp.desc())
                .first()
            )
            ban_row = (
                session.query(BanHistory)
                .filter(BanHistory.user_id == user_id)
                .order_by(BanHistory.timestamp.desc())
                .first()
            )
            unban_row = (
                session.query(UnbanHistory)
                .filter(UnbanHistory.user_id == user_id)
                .order_by(UnbanHistory.timestamp.desc())
                .first()
            )
            notes_row = (
                session.query(NotesHistory)
                .filter(NotesHistory.user_id == user_id)
                .order_by(NotesHistory.timestamp.desc())
                .first()
            )
    except Exception as error:
        # Add error handling logic here
        raise error
    finally:
        session.close()

    if automod_row:
        last_row = automod_row
    else:
        last_row = None

    if kick_row and (last_row is None or kick_row.timestamp > last_row.timestamp):
        last_row = kick_row
    if warning_row and (last_row is None or warning_row.timestamp > last_row.timestamp):
        last_row = warning_row
    if ban_row and (last_row is None or ban_row.timestamp > last_row.timestamp):
        last_row = ban_row
    if unban_row and (last_row is None or unban_row.timestamp > last_row.timestamp):
        last_row = unban_row
    if notes_row and (last_row is None or notes_row.timestamp > last_row.timestamp):
        last_row = notes_row

    return last_row


def get_last_BWK_from_all_tables_by_user(user_id: str, server_id: int):
    """
    Retrieve the last ban, warning, or kick row from all tables in the 
        database for a given user ID.

    Parameters:
        user_id (str): The user ID to search for in the tables.
    Returns:
        object: The last row matching the search criteria.
    """
    try:
        session = get_session()
        with session:
            kick_row = (
                session.query(KickHistory)
                .filter(
                    KickHistory.user_id == user_id,
                    KickHistory.server_id == server_id
                )
                .order_by(KickHistory.timestamp.desc())
                .first()
            )
            warning_row = (
                session.query(WarningHistory)
                .filter(
                    WarningHistory.user_id == user_id,
                    WarningHistory.server_id == server_id
                )
                .order_by(WarningHistory.timestamp.desc())
                .first()
            )
            ban_row = (
                session.query(BanHistory)
                .filter(
                    BanHistory.user_id == user_id,
                    BanHistory.server_id == server_id,
                )
                .order_by(BanHistory.timestamp.desc())
                .first()
            )
    except Exception as error:
        # Add error handling logic here
        raise error
    finally:
        session.close()

    if kick_row:
        last_row = kick_row
    else:
        last_row = None

    if warning_row and (last_row is None or warning_row.timestamp > last_row.timestamp):
        last_row = warning_row
    if ban_row and (last_row is None or ban_row.timestamp > last_row.timestamp):
        last_row = ban_row

    return last_row
