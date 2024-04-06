from motor.motor_asyncio import AsyncIOMotorClient
from config.config import (DB_NAME, DB_USERNAME, DB_PASSWORD, DB_HOST, URI)
from utils.functions.database_functions import get_db_connection, close_db_connection
from utils.functions.character_functions import active_character

# Database
#_______________________________________________________________________________________________________________________

# Connect to the database
async def create_party_document(party_data):
    party_insert = {
        "party": {
            "party_id": party_data["party_id"],
            "party_name": party_data["party_name"],
            "leader_id": party_data["discord_tag"],  # Assuming interaction has a user attribute
            "members": [
                {
                    "user_id": _uid,  # Leader's user ID
                    "username": character_name,  # Leader's username
                    "role": "Leader"
                }
            ],
            "status": party_data.get("status", "Open"),  # Default status to Open if not provided
            "creation_date": party_data["creation_date"],
            "last_activity_date": party_data["creation_date"],  # Initial activity date is the creation date
            "settings": {
                "loot_distribution": party_data.get("loot_distribution", "Equal"),
                "experience_sharing": party_data.get("experience_sharing", True),
                "max_members": party_data.get("max_members", 5)
            }
        },
        "activities": {
            "completed": [],
            "in_progress": []
        },
        "chat": {
            "messages": []
        },
        "guild_id": party_data["guild_id"]  # Assuming interaction has a guild_id attribute
    }
    return party_insert

