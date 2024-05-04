from motor.motor_asyncio import AsyncIOMotorClient
import logging
from config.config import (DB_NAME, DB_USERNAME, DB_PASSWORD, DB_HOST, URI)
from utils.functions.database_functions import get_db_connection, close_db_connection
from utils.functions.character_functions import active_character

# Groups
#_______________________________________________________________________________________________________________________


# ______________________________________________________________________________________________________________________            
# Check if a party invite exists between two users
# Return: Boolean 
# ______________________________________________________________________________________________________________________   

async def invite_exists(db, character_document, second_character_document, invite_type):
    logging.debug(f"Invite Exists: Party data: {character_document['_id']} and {second_character_document['_id']}")
    if invite_type == "party":
        party_document = await db["invites"].find_one({
            "inviter_id": character_document['_id'],
            "invitee_id": second_character_document['_id'],
            "invite_type": invite_type
        })
    logging.debug(f"Invite Exists: Party document: {party_document}")
    return bool(party_document)
