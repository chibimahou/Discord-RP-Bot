import discord
from discord import app_commands
from mysql.connector import Error

from cogs.utility import (validate_alphanumeric, validate_height, validate_age, 
                     validate_date, validate_text, validate_level, get_db_connection,
                     close_db_connection, active_character)

async def create_character_logic(character_data, interaction):
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
            print(f"Invalid value for {field}.")
            return interaction.response.send_message(f"Invalid value for {field}.")

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
        print("Connection to MongoDB failed.")
        await interaction.response.send_message("Failed to connect to the database.")
        return
    
    try:
        # Insert the character data into the database
        rp_bot_collection = db['characters']  # Assuming 'characters' is the correct collection name
        rp_bot_collection.insert_one(character_data)
        await interaction.response.send_message("Character successfully created!")
    except Exception as e:
        print(f"Unexpected error: {e}")
        await interaction.response.send_message("An unexpected error occurred.")
    finally:
        client.close()     
                 
async def delete_character_logic(character_data, interaction):
    # Validate the character name
    if not validate_alphanumeric(character_data.get("characters_name", "")):
        print("Invalid character name.")
        await interaction.response.send_message("Invalid value for character name.")
        return

    client, db = await get_db_connection()
    if db is None:
        print("Connection to MongoDB failed.")
        await interaction.response.send_message("Failed to connect to the database.")
        return

    try:
        print(f"Type of db: {type(db)}")  # This should not be a tuple
        print(f"Type of character_data: {type(character_data)}")  # This should be dict
        print(character_data["characters_name"])
        delete_result = await db['characters'].delete_one({
            "characters_name": character_data["characters_name"],
            "discord_tag": character_data["discord_tag"]
        })
        print('1')
        if delete_result.deleted_count > 0:
            print("Character successfully deleted.")
            await interaction.response.send_message("Character successfully deleted!")
        else:
            print("Character not found or already deleted.")
            await interaction.response.send_message("Character not found or already deleted.")
    except Exception as e:
        print(f"Error: {e}")
        await interaction.response.send_message("An error occurred while attempting to delete the character.")

async def active_character_logic(interaction, discord_tag):
    username, message = await active_character(discord_tag)
    print(username)
    if username is not None:
        await interaction.response.send_message(f"Your active character is {username}!")
    else:
        await interaction.response.send_message(message)