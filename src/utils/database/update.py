from models.moderation_tables import (
    AutomodHistory,
    BanHistory,
    KickHistory,
    NotesHistory,
    UnbanHistory,
    WarningHistory,
)
from utils.database.session import get_session


def update_row_by_code(code, new_value, table):
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
