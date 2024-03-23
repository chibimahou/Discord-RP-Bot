import discord
import logging
from discord import app_commands

from utils.functions.character_functions import (
                    active_character, available_characters, create_character_insert, create_character, 
                    delete_character, switch_active_character, add_points_to_stat, level_up,
                    check_character_exists, get_character_by_name)
from utils.functions.database_functions import (
                    get_db_connection, close_db_connection)
from utils.functions.validation_functions import (validate_alphanumeric, validate_height, validate_age, 
                    validate_text, validate_level, validate_date)
from utils.functions.utility_functions import comment_wrap


async def create_logic(character_data):
    validators = {
        "first_name": validate_alphanumeric,
        "last_name": validate_alphanumeric,
        "characters_name": validate_alphanumeric,
        "height": validate_height,
        "physique": validate_alphanumeric,
        "age": validate_age,
        "birthday": validate_date,
        "bio": validate_text,
        "level": validate_level
    }

    # Validate each field
    for field, validator in validators.items():
        if field not in character_data or not validator(character_data[field]):
            logging.info(f"Invalid value for {field}.")
            return await comment_wrap(f"Invalid value for {field}.")

    try:
        client, db = await get_db_connection()
    except Exception as e:
        logging.exception("Database connection failed: %s", e)
        return await comment_wrap("There seems to be a problem. Please reach out to an administrator.")
    
    try:
        character_document = await active_character(db, character_data)
        # Now including the guild_id in character_data before insertion
        character_insert = await create_character_insert(character_data)
        # Check if character exists
        character_data["character_name"] = character_data["characters_name"]
        character_exists = await check_character_exists(db, character_data)
        if character_exists:
            return await comment_wrap("Character already exists.")
        # Validates if there is an active character, if not, sets the new character as active
        logging.debug(f"character Document: {character_document}")
        if character_document is None:
            logging.debug("No Active Character")
            character_insert["player"]['active'] = True
        else:
            logging.debug("Active Character Exists")
            character_insert["player"]['active'] = False
        # Insert the character data into the database
        await create_character(db, character_insert)
        logging.debug("Character created successfully.")
        return await comment_wrap("Character created successfully.")
    except Exception as e:
        logging.exception(f"Unexpected error: {e}")
        return await comment_wrap(f"An unexpected error occurred: {e}")
    finally:
        await close_db_connection(client)
                     
async def delete_logic(character_data, interaction):
    # Validate the character name
    if not validate_alphanumeric(character_data.get("characters_name", "")):
        logging.info("Invalid character name.")
        return "Invalid value for character name."
    try:
        client, db = await get_db_connection()
    except Exception as e:
        logging.exception("Database connection failed: %s", e)
        return await comment_wrap("Database connection failed.")
    
    try:
        message = await delete_character(db, character_data)
        return message
    except Exception as e: 
        logging.exception(f"Unexpected error: {e}")
        return "An unexpected error occurred."
    finally:
        await close_db_connection(client)
        
async def switch_active_logic(character_data):
    # Validate the character name
    if not validate_alphanumeric(character_data.get("characters_name", "")):
        logging.info("Invalid character name.")
        return "Invalid value for character name."
    
    try:
        client, db = await get_db_connection()
    except Exception as e:
        logging.exception("Database connection failed: %s", e)
        return await comment_wrap("Database connection failed.")
    
    try:
        character_document = await active_character(db, character_data)
        new_characters_document = await get_character_by_name(db, character_data)
        if character_document is None:
            logging.info("No characters found.")
            return await comment_wrap("No characters found.")
        status = await switch_active_character(db, character_data, character_document, new_characters_document)
        if status:
            return await comment_wrap(f"Active character switched to {character_data['characters_name']}!")
        
        return await comment_wrap(f"Please validate the information you provided is correct. \nNote: You can use the command `all_available` to see all available characters.")
    except Exception as e:
        logging.exception(f"Unexpected error: {e}")
        return await comment_wrap("An unexpected error occurred.")
    finally:
        await close_db_connection(client)
        
# Display all available characters for a user
async def all_available_logic(character_data):
    try:
        # Find all characters for the user
        logging.debug(character_data['discord_tag'])
        characters = await available_characters(character_data)
        if not characters:  # This checks for both empty list and None
            logging.info("No characters found.")
            return "No characters found."
        # Display the characters
        character_list = "\n".join([character.get('character', {}).get('characters_name', 'unnamed') for character in characters])
        return f"Your characters are: \n\n{character_list}"
    except Exception as e:
        logging.exception(f"Error: {e}")
        return "An error occurred while attempting to display the characters."

async def active_logic(character_data):
    try:
        client, db = await get_db_connection()
    except Exception as e:
        logging.exception("Database connection failed: %s", e)
        return await comment_wrap("Database connection failed.")

    try:
        # Assuming active_character is correctly implemented and returns None if no character is found
        character_document = await active_character(db, character_data)
        if character_document is None:
            logging.info("No characters found.")
            return await comment_wrap("No characters found.") 
        return await comment_wrap(f"Active character: {character_document['character']['characters_name']}")
    except Exception as e:  # Catching a general exception to handle any unexpected errors
        logging.exception("Error: %s", e)
        return await comment_wrap("An error occurred while attempting to display the characters.")
    finally:
        await close_db_connection(client)

# Function to add stat points to a character
async def add_stat_logic(character_data):
    try:
        client, db = await get_db_connection()
    except Exception as e:
        logging.exception("Database connection failed: %s", e)
        return await comment_wrap("Database connection failed.")
    try:
        message = await add_points_to_stat(db, character_data)
        return await comment_wrap(message)
    except Exception as e:
        logging.exception(f"Unexpected error: {e}")
        return await comment_wrap("An unexpected error occurred.")
    finally:
        await close_db_connection(client)
        
# Function to level up a character
async def level_up_logic(character_data):
    try:
        client, db = await get_db_connection()
    except Exception as e:
        logging.exception("Database connection failed: %s", e)
        return await comment_wrap("Database connection failed.")
    
    try:
        logging.info(f"Leveling up {character_data['discord_tag']} in guild {character_data['guild_id']}")
        character_document = await active_character(db, character_data)
        if character_document is None:
            logging.info("No characters found.")
            return await comment_wrap("No characters found.")
        status = await level_up(db, character_data, character_document)
        return f"Level up! You are now level. You have 3 points to distribute."
    except Exception as e:
        logging.exception(f"Unexpected error: {e}")
        return await comment_wrap("An unexpected error occurred.")
    finally:
        await close_db_connection(client)