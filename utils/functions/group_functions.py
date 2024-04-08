from motor.motor_asyncio import AsyncIOMotorClient
import logging
from config.config import (DB_NAME, DB_USERNAME, DB_PASSWORD, DB_HOST, URI)
from utils.functions.database_functions import get_db_connection, close_db_connection
from utils.functions.character_functions import active_character

# Database
#_______________________________________________________________________________________________________________________

# Connect to the database
async def update_party_document(party_data, character_document):
    party_insert = {
        "party": {
            "party_name": party_data["party_name"],
            "leader_id": character_document['_id'],  # Assuming interaction has a user attribute
            "members": [
                {
                    "user_id": character_document['_id'],  # Leader's user ID
                    "username": character_document['character']['characters_name'],  # Leader's usernameF
                    "role": "Leader"
                }
            ],
            "status": party_data.get("status", "Open"),  # Default status to Open if not provided
            "creation_date": party_data["creation_date"],
            "last_activity_date": party_data["creation_date"],  # Initial activity date is the creation date
            "settings": {
                "loot_distribution": party_data.get("loot_distribution", "Equal"),
                "experience_sharing": party_data.get("experience_sharing", True),
                "max_members": party_data.get("max_members", 5),
                "guild_id": party_data["guild_id"]
            }
        },
        "activities": {
            "completed": [],
            "in_progress": []
        },
        "chat": {
            "messages": []
        },
    }
    return party_insert

async def party_exists(db, party_data, character_document):
    logging.debug(f"Party Exists: Party data: {character_document['group']['party_id']} and {party_data['guild_id']}")
    party_document = await db["parties"].find_one({
        "_id": character_document['group']['party_id'],  # Assuming party_id is the character's ID
        "party.settings.guild_id": party_data['guild_id']
    })
    logging.debug(f"Party Exists: Party document: {party_document}")
    return bool(party_document)