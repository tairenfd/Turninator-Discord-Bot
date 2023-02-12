import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from config.config import sql_database, sql_host, sql_password, sql_user

url = sqlalchemy.engine.URL.create(
    drivername="mysql+pymysql",
    username=sql_user,
    password=sql_password,
    host=sql_host,
    database=sql_database,
)


def get_session() -> sqlalchemy.orm.Session:
    """
    Create and return a new SQLAlchemy ORM session connected to the database.

    Returns:
        A new SQLAlchemy ORM session connected to the database.
    """
    engine = create_engine(url)
    Session = sessionmaker(bind=engine)
    session = Session()
    return session
