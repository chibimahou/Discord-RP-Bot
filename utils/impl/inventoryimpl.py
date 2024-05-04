import logging
import discord
from discord import app_commands

from cogs.utility import close_db_connection
from utils.functions.character_functions import (get_active_character, get_character_by_name, update_combat_stats)
from utils.functions.inventory_functions import (add_item_to_inventory, remove_item_from_inventory, check_inventory,
                                                 equip, item_exists_in_inventory, get_equipped_item, unequip)
from utils.functions.database_functions import (get_db_connection)
from utils.functions.item_functions import get_item
from utils.functions.utility_functions import comment_wrap
from utils.functions.validation_functions import (validate_alphanumeric, validate_height, validate_age, 
                                                  validate_text, validate_level)

from pymongo import MongoClient

def add_logic(interaction, characters_data, item_data):
    message = add_item_to_inventory(characters_data, item_data)
    return message

def remove_logic(interaction, characters_data, item_data):
    message = remove_item_from_inventory(characters_data, item_data)
    return message

def check_logic(interaction, characters_data):
    message = check_inventory(characters_data)
    return message

async def equip_logic(character_data, item_data):
    # Get the database connection
    try:
        client, db = await get_db_connection()
    except Exception as e:
        logging.exception("Database connection failed: %s", e)
        return await comment_wrap("Database connection failed.")
    
    try:
        # Get the invitors data
        character_document = await get_active_character(db, character_data)
        # Get the item data
        item_document = await get_item(db, item_data)
        # Check if the character exists
        if not character_document:
            return await comment_wrap(f"Character not found.")
        # Check if item exists in character inventory
        in_inventory = item_exists_in_inventory(character_document, item_document)
        if not in_inventory:
            return await comment_wrap(f"Item not found in inventory.")
        # Check if currently equipped item exists
        currently_equipped = await get_equipped_item(db, character_document, item_data["slot"])
        if currently_equipped:
            # Remove currently equipped item and add it to the inventory
            removed = await unequip(db, character_document, currently_equipped, item_data["slot"])
            if not removed:
                return await comment_wrap(f"Failed to remove currently equipped item.")
        # Change head equipment
        equipment_changed = await equip(character_document, item_document, item_data["slot"])
        # Check if changing equipment was successful
        if equipment_changed:
            # Update the characters combat stats with new eqipment
            await update_combat_stats(db, character_document)
        return await comment_wrap(f"Failed to equip head armor.")
    except Exception as e:
        logging.exception(f"Error equipping head armor: {e}")
        return await comment_wrap(f"Error equipping head armor.")
    finally:
        await close_db_connection(client)
        
async def equip_offhand_logic():
    return None