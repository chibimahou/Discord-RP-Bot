import discord
from discord import app_commands
from mysql.connector import Error

from cogs.utility import (validate_alphanumeric, validate_height, validate_age, 
                     validate_date, validate_text, validate_level, get_db_connection,
                     close_db_connection)

def add_inventory_logic(interaction, characters_name, discord_tag, item_name, quantity):
    connection = get_db_connection()
    if connection is None:
        return "Failed to connect to the database."

    try:
        cursor = connection.cursor()

        # Get the user_id and item_id using the characters_name and item_name
        cursor.execute("SELECT user_id FROM Users WHERE characters_name = %s", (characters_name,))
        user = cursor.fetchone()
        cursor.execute("SELECT item_id FROM Items WHERE item_name = %s", (item_name,))
        item = cursor.fetchone()

        if not user or not item:
            return "User or item not found."

        user_id = user[0]
        item_id = item[0]

        # Check if the item already exists in the user's inventory
        cursor.execute("SELECT quantity FROM Inventory WHERE user_id = %s AND item_id = %s", (user_id, item_id))
        result = cursor.fetchone()

        if result:
            # Update the quantity if the item exists
            new_quantity = result[0] + quantity
            cursor.execute("UPDATE Inventory SET quantity = %s WHERE user_id = %s AND item_id = %s", (new_quantity, user_id, item_id))
        else:
            # Insert a new item if it doesn't exist
            cursor.execute("INSERT INTO Inventory (user_id, item_id, quantity) VALUES (%s, %s, %s)", (user_id, item_id, quantity))
        
        # Commit the transaction
        connection.commit()
        
        return "Item added successfully!"

    except Error as e:
        print(f"Error: {e}")
        return interaction.response.send_message("Failed to add item to inventory.")

    finally:
        cursor.close()
        close_db_connection(connection)
        return interaction.response.send_message("added item to inventory!")        


def close_db_connection(connection):
    if connection.is_connected():
        connection.close()

