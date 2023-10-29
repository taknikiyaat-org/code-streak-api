import mysql.connector
from mysql.connector import Error
from sqlalchemy import create_engine, text

from src.libstreak.database.config import DatabaseConfig

# black src/libstreak/database/connect.py


engine = None


def create_server_connection():
    try:
        mysql_conn = mysql.connector.connect(**DatabaseConfig().get_config())
    except Error as err:
        mysql_conn = f"mysql.connector.Error: '{err}'"
    return mysql_conn


def create_alchemy_engine():
    global engine
    if engine:
        return engine
    engine = create_engine(DatabaseConfig.CONNECTION_STRING, echo=True)
    print("Created engine=", engine)
    return engine


if __name__ == "__main__":
    engine = create_alchemy_engine()
    with engine.connect() as conn:
        result = conn.execute(text("SELECT * FROM user"))
        print("result.all()", result.all())
        result = conn.execute(text("SELECT * FROM example WHERE name = :name"), dict(name="Ashley"))
        for row in result.mappings():
            print("Author:", row["name"])
    connection = create_server_connection()
    print("MySQL Database connection successful", connection)
