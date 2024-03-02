import mysql.connector
from mysql.connector import Error
from pymongo import MongoClient
from config.config import DB_HOST, DB_USERNAME, DB_PASSWORD, DB_NAME, URI

def get_database():
    try:
        # For a local MongoDB database
        client = MongoClient(URI)
        db = client[DB_NAME]  # Replace 'yourDatabaseName' with your actual database name

        # Optionally, check if the connection was successful by listing the database names
        # This is not a direct equivalent of the MySQL is_connected, but it can serve as a simple connection check
        if DB_NAME in client.list_database_names():
            print("Connected to database: {DB_NAME}")
            return db
        else:
            print("Failed to connect to MongoDB")
            return None
    except Exception as e:  # It's generally a good idea to catch more specific exceptions, but for simplicity, we'll catch all here.
        print(f"Error connecting to MongoDB: {e}")
        return None

def close_db_connection(connection):
    if connection.is_connected():
        connection.close()

# Add other database utility functions as needed
