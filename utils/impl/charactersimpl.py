import discord
from discord import app_commands
from mysql.connector import Error

from cogs.utility import (validate_alphanumeric, validate_height, validate_age, 
                     validate_date, validate_text, validate_level, get_db_connection,
                     close_db_connection, active_character)

def create_character_logic(character_data, interaction):
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
            if not validator(character_data[field]):
                print(f"Invalid value for {field}.")
                return interaction.response.send_message(f"Invalid value for {field}.")

        # Below logic needs to be executed in a synchronous environment 
        # since mysql-connector-python is not async. Consider using aiomysql for async.

        # Connect to MySQL
        try:
            connection = get_db_connection()
            
            if connection:
                cursor = connection.cursor()

                # Define the stored procedure name and parameters
                stored_procedure_name = 'sp_create_character'
                stored_procedure_parameters = (
                        character_data["first_name"],
                        character_data["last_name"],
                        character_data["height"],
                        character_data["physique"],
                        character_data["age"],
                        '',  # Keeping the old value for proficiency skills
                        '',  # ... and so on for other parameters
                        '',
                        '',
                        character_data["bio"],
                        '',
                        '',
                        character_data["birthday"],
                        character_data["characters_name"], 
                        '',
                        '', 
                        '', 
                        '', 
                        '', 
                        '', 
                        '', 
                        '', 
                        '', 
                        100, 
                        0, 
                        1, 
                        5, 
                        5, 
                        5, 
                        5, 
                        5, 
                        5, 
                        5,
                        5, 
                        '', 
                        '', 
                        character_data["discord_tag"],
                        ''
                )

                # Call the stored procedure
                cursor.callproc(stored_procedure_name, stored_procedure_parameters)

                # Commit the transaction
                connection.commit()
            else:
                print("Connection failed.")
                return None
        except Error as e:
            print(f"Error: {e}")
            return None 
        finally:
            # Close the cursor and connection
            if cursor:
                cursor.close()
            close_db_connection(connection) 
            return interaction.response.send_message(f"Character successfully created!")
        
def delete_character_logic(character_data, interaction):
        # Your logic to delete a character goes here
        # This might involve validation, database operations, etc.
        valid_character_name = validate_alphanumeric("characters_name")
        if not valid_character_name:
            print(f"Invalid character_name.")
            return False, f"Invalid value for character name."
        else:
            try:
                connection = get_db_connection()
                
                if connection:
                    cursor = connection.cursor()

                    # Define the stored procedure name and parameters
                    stored_procedure_name = 'sp_delete_character'
                    stored_procedure_parameters = (             
                        character_data["characters_name"], 
                        character_data["discord_tag"], 
                    )
                    # Call the stored procedure
                    cursor.callproc(stored_procedure_name, stored_procedure_parameters)

                    # Commit the transaction
                    connection.commit()
                else:
                    print("Connection failed.")
                return None
            except Error as e:
                print(f"Error: {e}")
                return None
            finally:
                # Close the cursor and connection
                if cursor:
                    cursor.close()
                close_db_connection(connection) 
                return interaction.response.send_message(f"Character successfully deleted!")
            
def active_character_logic(interaction, discord_tag):
    username = active_character(discord_tag)
    return interaction.response.send_message(f"Your active character is {username}!")
    # Your logic to create a character goes here
    # This might involve validation, database operations, etc.
    