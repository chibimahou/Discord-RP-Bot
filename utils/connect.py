import mysql.connector
from mysql.connector import Error
from config.config import DB_HOST, DB_USERNAME, DB_PASSWORD, DB_NAME

def get_database():
    try:
        connection = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USERNAME,
            password=DB_PASSWORD,
            database=DB_NAME
        )
        if connection.is_connected():
            print(f"Connected to database {DB_NAME}")
            return connection
    except Error as e:
        print(f"Error: {e}")
        return None

# Add other database utility functions as needed
