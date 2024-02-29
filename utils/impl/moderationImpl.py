import discord
from discord import app_commands
from mysql.connector import Error

from cogs.utility import (validate_alphanumeric, validate_height, validate_age, 
                     validate_date, validate_text, validate_level, get_db_connection,
                     close_db_connection, active_character)

def add_item_logic(interaction, item_data):
    validators = {
        "item_name": validate_text,
        "item_description": validate_text,
        "rarity": validate_alphanumeric,
        "how_to_obtain": validate_text,
        "catagory": validate_alphanumeric,
        "method_to_obtain": validate_alphanumeric
    }
    # Validate each field
    for field, validator in validators.items():
        if not validator(item_data[field]):
            print(f"Invalid value for {field}.")
            return interaction.response.send_message(f"Invalid value for {field}.")

    connection = get_db_connection()
    cursor = None  # Define cursor here to avoid possible NameError later
    if connection is None:
        return interaction.response.send_message("Failed to connect to the database.")
        
    try:
        cursor = connection.cursor()

        # Define the stored procedure name and parameters
        stored_procedure_name = 'sp_add_item_to_server'
        stored_procedure_parameters = (
            item_data["item_name"], 
            item_data["item_description"], 
            item_data["rarity"],
            item_data["how_to_obtain"],
            item_data["catagory"],
            item_data["method_to_obtain"]
        )
        print("executing")
        cursor.callproc(stored_procedure_name, stored_procedure_parameters)
        connection.commit()

        return interaction.response.send_message(f"Item successfully added!")

    except Error as e:
        print(f"Error: {e}")
        return interaction.response.send_message("Error adding item to the database.")

    finally:
        # Close the cursor and connection
        if cursor:
            cursor.close()
        close_db_connection(connection) 

            
def active_character_logic(interaction, discord_tag):
    username = active_character(discord_tag)
    return interaction.response.send_message(f"Your active character is {username}!")
    # Your logic to create a character goes here
    # This might involve validation, database operations, etc.
    