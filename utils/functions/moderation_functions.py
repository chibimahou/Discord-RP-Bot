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
         
#_______________________________________________________________________________________________________________________
# Toggle function between enabled and disabled for specific servers
#_______________________________________________________________________________________________________________________
async def toggle_functions(function_name, guild_id):
    client, db = await get_db_connection()
    try:
        # Check if function is enabled or disabled in allowed_functions collection
        function_document = await db["allowed_functions"].find_one({
            "function_name": function_name,
            "guild_id": guild_id
        })
        # If the function is not found, create it and disable it
        if not function_document:
            await db["allowed_functions"].insert_one({
                "function_name": function_name,
                "guild_id": guild_id,
                "enabled": False
            })
            return f"{function_name} is now disabled."
        # If the function is found, toggle the enabled status
        else:
            enabled = not function_document["enabled"]
            await db["allowed_functions"].update_one({
                "function_name": function_name,
                "guild_id": guild_id
            }, {
                "$set": {
                    "enabled": enabled
                }
            })
            return f"{function_name} is now {'enabled' if enabled else 'disabled'}."
        
    except Exception as e:
        logging.exception(f"Error toggling {function_name}: {e}")
        return f"Error toggling {function_name}."
    
    finally:
        await close_db_connection(client)