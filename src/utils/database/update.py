from models.moderation_tables import (
    AutomodHistory,
    BanHistory,
    KickHistory,
    NotesHistory,
    UnbanHistory,
    WarningHistory,
)
from utils.database.session import get_session


def update_row_by_code(code: str, new_value: str, table: str) -> None:
    """
    Update a row in the specified moderation table by the given code.

    Parameters:
        code (str): The code of the row to update.
        new_value (str): The new value to set for the row's reason or note field.
        table (str): The name of the moderation table to update.
    """
    session = get_session()
    if table == "automod_history":
        row = session.query(AutomodHistory).filter(AutomodHistory.code == code).first()
        row.reason = new_value
    elif table == "kick_history":
        row = session.query(KickHistory).filter(KickHistory.code == code).first()
        row.reason = new_value
    elif table == "warning_history":
        row = session.query(WarningHistory).filter(WarningHistory.code == code).first()
        row.reason = new_value
    elif table == "ban_history":
        row = session.query(BanHistory).filter(BanHistory.code == code).first()
        row.reason = new_value
    elif table == "unban_history":
        row = session.query(UnbanHistory).filter(UnbanHistory.code == code).first()
        row.reason = new_value
    elif table == "notes_history":
        row = session.query(NotesHistory).filter(NotesHistory.code == code).first()
        row.note = new_value
    session.commit()
    session.close()
