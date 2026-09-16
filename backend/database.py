import sqlite3
DATABASE = "app.db"

def get_db_connection():
    connection = sqlite3.connect(DATABASE)
    connection.row_factory = sqlite3.Row
    return connection

def initialize_database():
    connection = get_db_connection()

    with open("schema.sql", "r") as file:
        schema = file.read()

    connection.executescript(schema)
    connection.commit()
    connection.close()
    