import os

import mysql.connector


# Getting variables from .env for connection to database
host = os.environ.get("HOST")
user = os.environ.get("USER")
password = os.environ.get("PASSWORD")


# Connects to database and returns connection
def get_connection():

    return mysql.connector.connect(
        host=host,
        user=user,
        password=password
    )


# Opens cursor and returns
def open_cursor(connection):
    return connection.cursor()


# Closes the cursor
def close_cursor(cursor):
    cursor.close()


# Closes the connection
def close_connection(connection):
    connection.close()