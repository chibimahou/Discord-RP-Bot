import discord
import logging
from discord import app_commands
from mysql.connector import Error

from utils.functions.character_functions import (
                    active_character, available_characters, create_character_insert, create_character, 
                    delete_character, switch_active_character, add_points_to_stat, level_up,
                    check_character_exists, get_character_by_name)
from utils.functions.database_functions import (
                    get_db_connection, close_db_connection)
from utils.functions.validation_functions import (validate_alphanumeric, validate_height, validate_age, 
                    validate_text, validate_level, validate_date)
from utils.functions.buff_functions import (check_if_buff_exists, apply_buff_to_item, get_item)
from utils.functions.item_functions import (check_if_item_exists, add_item_to_db)
from utils.functions.utility_functions import comment_wrap


async def apply_buff_logic(item_data):
    client, db = await get_db_connection()
    if db is None:
        return comment_wrap(f"Failed to connect to the database.")
    try:
        # Get Character data
        character_data = await active_character(db, item_data)
        if character_data is not None:
            buff_exists = await check_if_buff_exists(db, item_data)
            if buff_exists: 
                # Check if the item already exists
                item_exists = await check_if_item_exists(db, item_data)
                if item_exists:
                    # Get item name
                    old_item_data = await get_item(db, item_data)
                    apply_buff = await apply_buff_to_item(character_data, item_data, old_item_data)
                    if apply_buff:
                        return await comment_wrap(f"Buff '{item_data["buff_name"]}' successfully applied.")
        return await comment_wrap("No active character found.")
    except Exception as e:
        logging.exception(f"Unexpected error: {e}")
        return await comment_wrap(f"An unexpected error occurred: {e}")
    finally:
        await close_db_connection(client)

        
