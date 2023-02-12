from models.moderation_tables import (
    AutomodHistory,
    BanHistory,
    KickHistory,
    NotesHistory,
    UnbanHistory,
    WarningHistory,
)
from utils.database.session import get_session


def delete_row_by_code(code, table) -> None:
    """
    Deletes a row from the specified table by the code provided.

    Parameters:
        code (str): the code of the row to delete
        table (str): the name of the table to delete from
    """
    try:
        session = get_session()
        with session:
            if table == "automod_history":
                row = (
                    session.query(AutomodHistory)
                    .filter(AutomodHistory.code == code)
                    .first()
                )
                session.delete(row)
            elif table == "kick_history":
                row = (
                    session.query(KickHistory).filter(KickHistory.code == code).first()
                )
                session.delete(row)
            elif table == "warning_history":
                row = (
                    session.query(WarningHistory)
                    .filter(WarningHistory.code == code)
                    .first()
                )
                session.delete(row)
            elif table == "ban_history":
                row = session.query(BanHistory).filter(BanHistory.code == code).first()
                session.delete(row)
            elif table == "unban_history":
                row = (
                    session.query(UnbanHistory)
                    .filter(UnbanHistory.code == code)
                    .first()
                )
                session.delete(row)
            elif table == "notes_history":
                row = (
                    session.query(NotesHistory)
                    .filter(NotesHistory.code == code)
                    .first()
                )
                session.delete(row)
            session.commit()
    except Exception as error:
        # TODO: error handling
        raise error
    finally:
        session.close()
