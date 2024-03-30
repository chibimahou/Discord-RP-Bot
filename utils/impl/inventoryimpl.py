import discord
from discord import app_commands
from mysql.connector import Error

from cogs.utility import (validate_alphanumeric, validate_height, validate_age, 
                     validate_date, validate_text, validate_level, get_db_connection,
                     close_db_connection)

from pymongo import MongoClient

def get_db_connection():
    try:
        # Assuming MongoDB is running on the default host and port
        client = MongoClient('mongodb://localhost:27017/')
        # Assuming the database is named 'game'
        return client['game']
    except Exception as e:
        print(f"Failed to connect to the database: {e}")
        return None

def add_logic(interaction, characters_name, discord_tag, item_name, quantity):
    db = get_db_connection()
    if db is None:
        return "Failed to connect to the database."
    
    try:
        # Assuming 'Users' and 'Items' are collections within your MongoDB database
        user = db.Users.find_one({"characters_name": characters_name, "discord_tag": discord_tag})
        item = db.Items.find_one({"item_name": item_name})

        if not user or not item:
            return "User or item not found."

        user_id = user["_id"]
        item_id = item["_id"]

        # Check if the item already exists in the user's inventory
        inventory_record = db.Inventory.find_one({"user_id": user_id, "item_id": item_id})

        if inventory_record:
            # Update the quantity if the item exists
            new_quantity = inventory_record["quantity"] + quantity
            db.Inventory.update_one({"user_id": user_id, "item_id": item_id}, {"$set": {"quantity": new_quantity}})
        else:
            # Insert a new item if it doesn't exist
            db.Inventory.insert_one({"user_id": user_id, "item_id": item_id, "quantity": quantity})
        
        return "Item added successfully!"
    except Exception as e:
        print(f"An error occurred: {e}")
        return "An error occurred while adding the item."

def close_db_connection(connection):
    connection.close()


