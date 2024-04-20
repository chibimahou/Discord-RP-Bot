import logging
import math
from utils.functions.database_functions import get_db_connection, close_db_connection
from utils.functions.character_functions import active_character

# moderation
#_______________________________________________________________________________________________________________________
# add character data to an object
async def add_item_to_database(character_data, item_data):
    client, db = await get_db_connection()
    try:
        item_document = await db["items"].find_one({
            "item_name": item_data["item_name"],
            "guild_id": character_data["guild_id"]
        })
        # Check if the item exists and if not, return an error message
        if not item_document:
            logging.info(f"Item not found: {item_data['item_name']}")
            return "Item not found"
        update = await db["characters"].insert_one(
                    {
                            "player.discord_tag": character_data['discord_tag'],
                            "player.guild_id": character_data['guild_id'],
                            "player.active": True
                        },
                        {
                            "$set": {
                                f"inventory.{item_document['slot']}.item_name": item_document['name'],
                                f"inventory.{item_document['slot']}._id": item_document['_id'],
                                f"inventory.{item_document['slot']}._id": 1
                            }
                        })
        # If the update was successful, update the corresponding stat
        if (update.modified_count > 0):
                return ""
        else:
                return f""
    except Exception as e:
        logging.exception(f"Error adding points to stat: {e}")
        return f""
    finally:
        await close_db_connection(client)    