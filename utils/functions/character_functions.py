import logging
from utils.functions.database_functions import get_db_connection, close_db_connection

# Characters
#_______________________________________________________________________________________________________________________

# select active character name
async def active_character(discord_tag):
    client, db = await get_db_connection()
    try:
        character_document = await db["characters"].find_one({"discord_tag": discord_tag, "active": True})
        if character_document:
            character_name = character_document.get("characters_name")
            return character_name, "Data fetched successfully!"
        else:
            return None, "No active character found for this Discord tag."
    except Exception as e:
        logging.exception(f"Error fetching active character: {e}")
        return None, f"Error fetching active character: {e}"
    finally:
        await close_db_connection(client)
        
# validate character exists in the database
async def validate_character_exists(character_name, discord_tag):
    client, db = await get_db_connection()
    try:
        character_document = await db["characters"].find_one({"discord_tag": discord_tag, "characters_name": character_name})
        if character_document:
            return True
        else:
            return False
    except Exception as e:
        logging.exception(f"Error validating character: {e}")
        return False
    finally:
        await close_db_connection(client)
        
# return all characters for a user
async def available_characters(discord_tag):
    client, db = await get_db_connection()
    try:
        # Await the to_list coroutine to get the actual list of characters
        characters = await db["characters"].find({"discord_tag": discord_tag}).to_list(length=None)
        return characters
    except Exception as e:
        logging.exception(f"Error fetching characters: {e}")
        return []
    finally:
        await close_db_connection(client)

