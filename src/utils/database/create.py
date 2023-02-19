from models.moderation_tables import (
    AutomodHistory,
    BanHistory,
    KickHistory,
    NotesHistory,
    UnbanHistory,
    WarningHistory,
)
from utils.database.session import get_session


def insert_row_into_table(user_id: int,
                          moderator_id: int,
                          server_id: int,
                          reason: str,
                          table: str,
                          ban_time: int = 0
                          ) -> None:
    """
    Insert a new row in the specified table in the database.

    Parameters:
        - user_id (int): The ID of the user being added to the table.
        - moderator_id (int): The ID of the moderator adding the user to the table.
        - server_id (int): The ID of the server where the action took place.
        - reason (str): The reason for the action taken on the user.
        - table (str): The name of the table where the row should be inserted.
    """
    try:
        session = get_session()
        with session:
            if table == "automod_history":
                row = AutomodHistory(
                    user_id=user_id,
                    moderator_id=000000000000000000,
                    server_id=server_id,
                    reason=reason,
                )
                session.add(row)
            elif table == "kick_history":
                row = KickHistory(
                    user_id=user_id,
                    moderator_id=moderator_id,
                    server_id=server_id,
                    reason=reason,
                )
                session.add(row)
            elif table == "warning_history":
                row = WarningHistory(
                    user_id=user_id,
                    moderator_id=moderator_id,
                    server_id=server_id,
                    reason=reason,
                )
                session.add(row)
            elif table == "ban_history":
                row = BanHistory(
                    user_id=user_id,
                    moderator_id=moderator_id,
                    server_id=server_id,
                    reason=reason,
                    ban_time=ban_time
                )
                session.add(row)
            elif table == "unban_history":
                row = UnbanHistory(
                    user_id=user_id,
                    moderator_id=moderator_id,
                    server_id=server_id,
                    reason=reason,
                )
                session.add(row)
            elif table == "notes_history":
                row = NotesHistory(
                    user_id=user_id,
                    moderator_id=moderator_id,
                    server_id=server_id,
                    note=reason,
                )
                session.add(row)
            session.commit()
    except Exception as error:
        # TODO: error handling
        raise error
    finally:
        session.close()
