import discord
import logging
from discord import app_commands
from mysql.connector import Error

from utils.functions.character_functions import (
                    active_character, available_characters, create_character_insert, create_character, 
                    delete_character, switch_active_character, add_points_to_stat, level_up)
from utils.functions.database_functions import (
                    get_db_connection)
from utils.functions.validation_functions import (validate_alphanumeric, validate_height, validate_age, 
                    validate_text, validate_level)

async def create_logic(character_data, interaction):
    validators = {
        "first_name": validate_alphanumeric,
        "last_name": validate_alphanumeric,
        "characters_name": validate_alphanumeric,
        "height": validate_height,
        "physique": validate_alphanumeric,
        "age": validate_age,
        "birthday": validate_alphanumeric,
        "bio": validate_text,
        "level": validate_level
    }

    # Validate each field
    for field, validator in validators.items():
        if field not in character_data or not validator(character_data[field]):
            logging.info(f"Invalid value for {field}.")
            return f"Invalid value for {field}."

    # Now including the guild_id in character_data before insertion
    character_insert = await create_character_insert(character_data, interaction.guild.id)
    active_character_name, message = await active_character(character_insert["player"]["discord_tag"], character_insert["player"]["guild_id"])
    # Validates if there is an active character, if not, sets the new character as active
    if active_character_name is None:
        print("Active: True")
        character_insert["player"]['active'] = True
    else:
        print("Active: False")
        character_insert["player"]['active'] = False
    try:
        # Insert the character data into the database
        await create_character(character_insert)
    except Exception as e:
        logging.exception(f"Unexpected error: {e}")
        return "An unexpected error occurred."
    finally:
        return "Character successfully created!"
                     
async def delete_logic(character_data, interaction):
    # Validate the character name
    if not validate_alphanumeric(character_data.get("characters_name", "")):
        logging.info("Invalid character name.")
        return "Invalid value for character name."
    message = await delete_character(character_data)
    return message

async def switch_active_logic(character_data, interaction):
    # Validate the character name
    if not validate_alphanumeric(character_data.get("characters_name", "")):
        logging.info("Invalid character name.")
        return "Invalid value for character name."
    message = await switch_active_character(character_data)
    return message
        
# Display all available characters for a user
async def all_available_logic(interaction, discord_tag):
    try:
        # Find all characters for the user
        logging.debug(discord_tag)
        characters = await available_characters(discord_tag)
        if characters is None:
            logging.info("No characters found.")
            return "No characters found."
        # Display the characters
        character_list = "\n".join([character["characters_name"] for character in characters])
        return f"Your characters are: \n\n{character_list}"
    except Exception as e:
        logging.exception(f"Error: {e}")
        return "An error occurred while attempting to display the characters."

async def active_logic(interaction, discord_tag):
    username, message = await active_character(discord_tag)
    return message

# Function to add stat points to a character
async def add_stat_logic(discord_tag, guild_id, stat_name, stat_value):
    message = await add_points_to_stat(discord_tag, guild_id, stat_name, stat_value)

    return message

# Function to level up a character
async def level_up_logic(discord_tag, guild_id):
    logging.info(f"Leveling up {discord_tag} in guild {guild_id}")
    message = await level_up(discord_tag, guild_id)

    return message