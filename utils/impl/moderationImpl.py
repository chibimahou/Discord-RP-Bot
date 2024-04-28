import logging
import discord
from discord import app_commands
from utils.functions.moderation_functions import(check_if_mob_exists)




from cogs.utility import (validate_alphanumeric, validate_height, validate_age, 
                     validate_date, validate_text, validate_level, get_db_connection,
                     close_db_connection, active_character,) 

def add_item_logic(interaction, item_data):
    validators = {
        "item_name": validate_text,
        "item_description": validate_text,
        "rarity": validate_alphanumeric,
        "how_to_obtain": validate_text,
        "category": validate_alphanumeric,  # Fixed typo from 'catagory' to 'category'
        "method_to_obtain": validate_alphanumeric
    }

    # Validate each field
    for field, validator in validators.items():
        if field not in item_data or not validator(item_data[field]):
            print(f"Invalid value for {field}.")
            return interaction.response.send_message(f"Invalid value for {field}.")

    db = get_db_connection()
    if db is None:
        return interaction.response.send_message("Failed to connect to the database.")
        
    try:
        # Items collection
        items_collection = db['items']

        # Check if the item already exists
        if items_collection.find_one({"item_name": item_data["item_name"]}):
            return interaction.response.send_message(f"Item {item_data['item_name']} already exists.")

        # Insert the new item
        insert_result = items_collection.insert_one(item_data)

        if insert_result.inserted_id:
            return interaction.response.send_message(f"Item successfully added!")
        else:
            return interaction.response.send_message("Failed to add the item.")
    except Exception as e:
        print(f"Error: {e}")
        return interaction.response.send_message("Error adding item to the database.")
    
async def add_mob_logic( mob_data):
    client,db = await get_db_connection()
    if db is None:
        return"Failed to connect to the database."

    try:
        # Assuming 'Mobs' is a collection within your MongoDB database
        # Check if the mob already exists
        existing_mob = await check_if_mob_exists(mob_data)
        if existing_mob:
            return "Mob already exists."

        # Insert the new mob data into the database
        db.mobs.insert_one(mob_data)

        return "Mob added successfully!"
    except Exception as e:
        print(f"An error occurred: {e}")
        return "An error occurred while adding the mob."
    
    
async def remove_mob_logic(mob_name: str, guild_id: int):
    try:
        # Establish database connection
        client, db = await get_db_connection()
        if db is None:
            return "Failed to connect to the database."

        # Check if the mob exists
        existing_mob = await db["mobs"].find_one({"mob_name": mob_name, "guild_id": guild_id})
        if existing_mob is None:
            return "Mob not found."

        # Delete the mob
        result = await db["mobs"].delete_one({"mob_name": mob_name, "guild_id": guild_id})
        if result.deleted_count == 1:
            return f"Mob '{mob_name}' deleted successfully!"
        else:
            return f"Failed to delete mob '{mob_name}'."

    except Exception as e:
        logging.error(f"An error occurred: {e}")
        return "An error occurred while deleting the mob."



async def view_mob_logic(guild_id: int, query: str):
    try:
        # Establish database connection
        client, db = await get_db_connection()
        
        if db is None:
            return "Failed to connect to the database."

        # Define your search query based on the provided query string and guild ID
        search_query = {
            "$text": {"$search": query},
            "guild_id": guild_id  # Filter by guild ID
        }

        # Execute the query
        mobs = await db["mobs"].find(search_query).to_list(length=None)

        if not mobs:
            return "No mobs found matching the search query."
        else:
            # Format the mobs information into a readable format
            formatted_info = format_mobs_info(mobs)
            return formatted_info

    except Exception as e:
        return "An error occurred while searching for mobs."



def format_mobs_info(mobs):
    if not mobs:
        return None
    
    formatted_info = ""
    for mob in mobs:
        formatted_info += f"Name: {mob['mob_name']}\n"
        formatted_info += f"Description: {mob['mob_description']}\n"
        formatted_info += f"Type: {mob['mob_type']}\n"
        formatted_info += f"Level: {mob['level']}\n"
        formatted_info += f"hp: {mob['hp']}\n"
        formatted_info += f"str: {mob['str']}\n"
        formatted_info += f"Defense: {mob['defense']}\n"
        formatted_info += f"spd: {mob['spd']}\n"
        formatted_info += f"dex: {mob['dex']}\n"
        formatted_info += f"cha: {mob['cha']}\n"
        formatted_info += f"xp: {mob['xp']}\n"
        formatted_info += f"spawn_message: {mob['spawn_message']}\n"
        formatted_info += f"drops: {mob['drops']}\n"
        formatted_info += f"spawn_channel: {mob['spawn_channel']}\n"
        formatted_info += "-------------------------\n"
        
    return formatted_info

async def search_mob_info(interaction, search_query):
    try:
        logging.debug(f"Received search query: {search_query}")

        # Get the database connection
        client,db = await get_db_connection()
        logging.debug(f"Database connection: {db}")

        # Execute the query
        mobs = await db["mobs"].find({"mob_name": search_query}).to_list(length=None)
        logging.debug(f"Retrieved mobs: {mobs}")

        if not mobs:
            return "No mobs found matching the search query."

        # Log the structure of the mobs variable
        logging.debug(f"Type of mobs: {type(mobs)}")
        logging.debug(f"Length of mobs: {len(mobs)}")
        logging.debug(f"First mob: {mobs[0]}")

        # Format the mobs information into a readable format
        formatted_info = ""
        for mob in mobs:
            formatted_info += f"mob_name: {mob['mob_name']}\n"
            formatted_info += f"Description: {mob['mob_description']}\n"
            formatted_info += f"Type: {mob['mob_type']}\n"
            formatted_info += f"Level: {mob['level']}\n"
            formatted_info += f"hp: {mob['hp']}\n"
            formatted_info += f"Strength: {mob['str']}\n"
            formatted_info += f"Defense: {mob['defense']}\n"
            formatted_info += f"Speed: {mob['spd']}\n"
            formatted_info += f"Dexterity: {mob['dex']}\n"
            formatted_info += f"Charisma: {mob['cha']}\n"
            formatted_info += f"Experience_Points: {mob['xp']}\n"
            formatted_info += f"Spawn_Message: {mob['spawn_message']}\n"
            formatted_info += f"drops: {mob['drops']}\n"
            formatted_info += f"spawn_location: {mob['spawn_location']}\n"
            formatted_info += "-------------------------\n"

        return formatted_info
        
    except Exception as e:
        logging.error(f"An error occurred while searching for mobs: {e}")
        return "An error occurred while searching for mobs."





def active_character_logic(interaction, discord_tag):
    username = active_character(discord_tag)
    return interaction.response.send_message(f"Your active character is {username}!")
    # Your logic to create a character goes here
    # This might involve validation, database operations, etc.
    