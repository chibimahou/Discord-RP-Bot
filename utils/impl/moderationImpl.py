import discord
from discord import app_commands
from mysql.connector import Error

from cogs.utility import (validate_alphanumeric, validate_height, validate_age, 
                     validate_date, validate_text, validate_level, get_db_connection,
                     close_db_connection, active_character)

def get_db_connection():
    try:
        # Assuming MongoDB is running on the default host and port
        client = MongoClient('mongodb://localhost:27017/')
        # Assuming the database is named 'game'
        return client['game']
    except Exception as e:
        print(f"Failed to connect to the database: {e}")
        return None

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

            
def active_character_logic(interaction, discord_tag):
    username = active_character(discord_tag)
    return interaction.response.send_message(f"Your active character is {username}!")
    # Your logic to create a character goes here
    # This might involve validation, database operations, etc.
    