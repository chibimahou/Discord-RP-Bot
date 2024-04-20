from motor.motor_asyncio import AsyncIOMotorClient
from config.config import (DB_NAME, DB_USERNAME, DB_PASSWORD, DB_HOST, URI)

# Database
#_______________________________________________________________________________________________________________________

# Connect to the database
async def get_db_connection():
    client = AsyncIOMotorClient(URI)
    db = client[DB_NAME]
    if db is None:
        raise Exception("Database connection failed.")
    return client, db

# Close the database connection
async def close_db_connection(client):
    # MongoDB uses a different approach to close connections. However, MongoClient automatically handles connection pooling.
    # It's generally safe to reuse MongoClient instances across your application.
    # Explicitly closing connection is often not necessary, but if you need to, you can call client.close()
    client.close()
    