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


def get_session():
    engine = create_engine(url)
    Session = sessionmaker(bind=engine)
    session = Session()
    return session
