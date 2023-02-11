from sqlalchemy import BigInteger, Column, DateTime, Integer, String, Text, func
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class AutomodHistory(Base):
    __tablename__ = "automod_history"
    id = Column(Integer, primary_key=True)
    code = Column(String(4), unique=True)
    user_id = Column(BigInteger)
    server_id = Column(BigInteger)
    reason = Column(Text)
    timestamp = Column(DateTime, default=func.now())


class KickHistory(Base):
    __tablename__ = "kick_history"
    id = Column(Integer, primary_key=True)
    code = Column(String(4), unique=True)
    user_id = Column(BigInteger)
    moderator_id = Column(BigInteger)
    server_id = Column(BigInteger)
    reason = Column(Text)
    timestamp = Column(DateTime, default=func.now())


class WarningHistory(Base):
    __tablename__ = "warning_history"
    id = Column(Integer, primary_key=True)
    code = Column(String(4), unique=True)
    user_id = Column(BigInteger)
    moderator_id = Column(BigInteger)
    server_id = Column(BigInteger)
    reason = Column(Text)
    timestamp = Column(DateTime, default=func.now())


class BanHistory(Base):
    __tablename__ = "ban_history"
    id = Column(Integer, primary_key=True)
    code = Column(String(4), unique=True)
    user_id = Column(BigInteger)
    moderator_id = Column(BigInteger)
    server_id = Column(BigInteger)
    ban_time = Column(BigInteger)
    reason = Column(Text)
    timestamp = Column(DateTime, default=func.now())


class UnbanHistory(Base):
    __tablename__ = "unban_history"
    id = Column(Integer, primary_key=True)
    code = Column(String(4), unique=True)
    user_id = Column(BigInteger)
    moderator_id = Column(BigInteger)
    server_id = Column(BigInteger)
    reason = Column(Text)
    timestamp = Column(DateTime, default=func.now())


class NotesHistory(Base):
    __tablename__ = "notes_history"
    id = Column(Integer, primary_key=True)
    code = Column(String(4), unique=True)
    user_id = Column(BigInteger)
    moderator_id = Column(BigInteger)
    server_id = Column(BigInteger)
    note = Column(Text)
    timestamp = Column(DateTime, default=func.now())
