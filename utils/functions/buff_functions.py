import logging
import math
from utils.functions.database_functions import get_db_connection, close_db_connection
from utils.functions.character_functions import active_character
from utils.functions.item_functions import check_if_item_exists, get_item, add_item_to_db
from utils.functions.inventory_functions import add_item_to_inventory, remove_item_from_inventory

# Buffs
#_______________________________________________________________________________________________________________________
async def get_buff(db, buff_data):
    logging.info(f"Getting item: {buff_data["name"]}")
    return db["buffs"].find_one({"name": buff_data["name"],
                                "guild_id": buff_data["guild_id"]})

async def check_if_buff_exists(db, buff_data):
    item = await get_item(db, buff_data["name"], buff_data["guild_id"])
    if item:
        return True
    return False

async def apply_buff_to_item(character_data, item_data, old_item_data):
    try:
        # Add item to inventory
        await add_item_to_inventory(character_data, item_data)
        # Remove old item from inventory
        await remove_item_from_inventory(character_data, old_item_data)
        # Return success message
        logging.info("Buff applied successfully.")
        return await "Buff applied successfully."
    # Handle exceptions
    except Exception as e:
        logging.exception(f"Unexpected error: {e}")
        return await f"An unexpected error occurred: {e}"
    
async def apply_buff_to_character(db, buff_data, character_data):
    try:
        # Check if the item already exists
        item_exists = await check_if_item_exists(db, buff_data)
        if item_exists:
            # Get item data
            item_data = await get_item(db, buff_data)
            # Apply buff to item
            results = await apply_buff_to_item(db, character_data, item_data)
            return results
        # Return failure message
        logging.warning("Buff failed to apply.")
        return await "Buff failed to apply."
    # Handle exceptions
    except Exception as e:
        logging.exception(f"Unexpected error: {e}")
        return await f"An unexpected error occurred: {e}"
    
