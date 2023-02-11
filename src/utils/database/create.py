from models.moderation_tables import (
    AutomodHistory,
    BanHistory,
    KickHistory,
    NotesHistory,
    UnbanHistory,
    WarningHistory,
)
from utils.database.session import get_session


def insert_row_into_table(user_id, moderator_id, server_id, reason, table):
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
