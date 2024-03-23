import discord
import logging
from discord import app_commands

from cogs.utility import (validate_alphanumeric, validate_height, validate_age, 
                     validate_date, validate_text, validate_level, get_db_connection,
                     close_db_connection, active_character, validate_character_exists,
                     available_characters)

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
    character_data['guild_id'] = interaction.guild.id  # Add guild ID to character data
    active_character_name, message = await active_character(character_data["discord_tag"])
    # Validates if there is an active character, if not, sets the new character as active
    if active_character_name is None:
        print("Active: True")
        character_data['active'] = True
    else:
        print("Active: False")
        character_data['active'] = False
    
    client, db = await get_db_connection()  # Adjust this function as needed
    if db is None:
        logging.error("Connection to MongoDB failed.")
        return "Failed to connect to the database."
        return
    
    try:
        # Insert the character data into the database
        rp_bot_collection = db['characters']  # Assuming 'characters' is the correct collection name
        rp_bot_collection.insert_one(character_data)
        return "Character successfully created!"
    except Exception as e:
        logging.exception(f"Unexpected error: {e}")
        return "An unexpected error occurred."
    finally:
        client.close()     
                 
async def delete_logic(character_data, interaction):
    # Validate the character name
    if not validate_alphanumeric(character_data.get("characters_name", "")):
        logging.info("Invalid character name.")
        return "Invalid value for character name."

    client, db = await get_db_connection()
    if db is None:
        logging.error("Connection to MongoDB failed.")
        return "Failed to connect to the database."

    try:
        delete_result = await db['characters'].delete_one({
            "characters_name": character_data["characters_name"],
            "discord_tag": character_data["discord_tag"]
        })
        if delete_result.deleted_count > 0:
            logging.info("Character successfully deleted.")
            return "Character successfully deleted!"
        else:
            logging.info("Character not found or already deleted.")
            return "Character not found or already deleted."
    except Exception as e:
        logging.exception(f"Error: {e}")
        return "An error occurred while attempting to delete the character."

async def switch_active_logic(character_data, interaction):
    # Validate the character name
    if not validate_alphanumeric(character_data.get("characters_name", "")):
        logging.info("Invalid character name.")
        return "Invalid value for character name."
    #Validate character exists
    character_exists = await validate_character_exists(character_data["characters_name"], character_data["discord_tag"])
    if(character_exists == False):
        return "Character does not exist."
    client, db = await get_db_connection()
    if db is None:
        logging.error("Connection to MongoDB failed.")
        return "Failed to connect to the database."
    try:
        #Validate that a character is active
        active_character_name, message = await active_character(character_data["discord_tag"])
        # If there is an active character, set it to inactive
        if active_character_name is not None:
            await db['characters'].update_one({"characters_name": active_character_name, "discord_tag": character_data["discord_tag"]},{"$set": {"active": False}})
        # Set the new character as active
        await db['characters'].update_one({"characters_name": character_data["characters_name"], "discord_tag": character_data["discord_tag"]},{"$set": {"active": True}})
        return f"You are now using the character {character_data['characters_name']}!"
    except Exception as e:
        logging.exception(f"Error: {e}")
        return f"An error occurred while attempting to switch the active character to {character_data['characters_name']}."
    finally:
        client.close()
        
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
    logging.debug(username)
    if username is not None:
        return f"Your active character is {username}!"
    else:
        return message