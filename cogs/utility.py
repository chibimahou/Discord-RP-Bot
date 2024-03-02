import discord
from discord import app_commands
import re
from datetime import datetime
import mysql.connector
from mysql.connector import Error
from cryptography.fernet import Fernet
from pymongo import MongoClient
from config.config import (DB_NAME, DB_USERNAME, DB_PASSWORD, DB_HOST, URI)

class utility(app_commands.Group):
    @app_commands.command()
    async def create_character(self, interaction: discord.Interaction):
        await interaction.response.send_message("test")
        
def validate_alphanumeric(input_str):
    """Validate string to contain only alphanumeric characters and underscores."""
    pattern = re.compile(r'^\w+$')
    return bool(pattern.match(input_str))

def validate_height(input_str):
    """Validate string to be a valid height format, e.g., 5'2"."""
    pattern = re.compile(r"^\d+'\d+\"$")
    return bool(pattern.match(input_str))

def validate_age(input_str):
    """Validate string to be a valid age (integer)."""
    return input_str.isdigit()

def validate_date(input_str):
    """Validate string to be a valid date."""
    try:
        datetime.strptime(input_str, "%m/%d/%y")
        return True
    except ValueError:
        return False

def validate_text(input_str):
    """Validate string to be a valid text without special characters."""
    pattern = re.compile(r"^[a-zA-Z0-9.,'\"!? ]+$")
    return bool(pattern.match(input_str))

def validate_level(input_str):
    """Validate string to be a valid level (integer) and non-negative."""
    return input_str.isdigit() and int(input_str) >= 0
#_______________________________________________________________________________________________________________________
#Open connection to database
def get_db_connection():
    try:
        # For a local MongoDB database
        client = MongoClient(URI)
        print("Connected to client")
        db = client[DB_NAME]  # Replace 'yourDatabaseName' with your actual database name
        print("Connecting to db")
        # Optionally, check if the connection was successful by listing the database names
        # This is not a direct equivalent of the MySQL is_connected, but it can serve as a simple connection check
        print(client.list_database_names())
        print("test: " + DB_NAME)
        if DB_NAME in client.list_database_names():
            print("Connected to MongoDB")
            return db
        else:
            print("Failed to connect to MongoDB")
            return None
    except Exception as e:  # It's generally a good idea to catch more specific exceptions, but for simplicity, we'll catch all here.
        print(f"Error connecting to MongoDB: {e}")
        return None

def close_db_connection(client):
    # MongoDB uses a different approach to close connections. However, MongoClient automatically handles connection pooling.
    # It's generally safe to reuse MongoClient instances across your application.
    # Explicitly closing connection is often not necessary, but if you need to, you can call client.close()
    client.close()
#_______________________________________________________________________________________________________________________
# select active character name
def active_character(discord_tag):
    try:
                connection = get_db_connection()
                
                if connection:
                    cursor = connection.cursor()

                    # Define the stored procedure name and parameters
                    stored_procedure_name = 'sp_get_active_character'
                    stored_procedure_parameters = (
                        discord_tag,
                    )

                    # Call the stored procedure
                    cursor.callproc(stored_procedure_name, stored_procedure_parameters)

                    # Fetching the results
                    for result in cursor.stored_results():
                        data = result.fetchone()
                    
                    for row in data:
                        character_name = row
                    
                    return data, "Data fetched successfully!"
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
        return character_name, active_character
#_______________________________________________________________________________________________________________________
# select party id
def get_party_or_guild_id(invitors_name, invite_to):
    #Create a encryption for the party id using the discord tag and invitors name
    party_id = invite_to + invitors_name
    # Generate a Key and instantiate a Fernet instance
    key = Fernet.generate_key()
    cipher_suite = Fernet(key)
    encrypted_id = cipher_suite.encrypt(party_id)
    #Return the encrypted party id
    return party_id
    
def is_user_in_a_party(user_id, guild_id):
    # Connect to your database
    connection = get_db_connection()
    try:
        cursor = connection.cursor(buffered=True)
        
        # Query to check if the user is in the party
        stored_procedure_name = 'sp_check_for_user_in_party'
        stored_procedure_parameters = (
            user_id,
            guild_id
        )
        
        # Execute the query with the provided user_id and party_id
        cursor.callproc(stored_procedure_name, stored_procedure_parameters)
        connection.commit()
                
        # Check if a result is found
        return cursor.fetchone() is not None
        
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return False
    finally:
        # Close the cursor and connection
        cursor.close()
        connection.close()
    
def is_user_invited(invitor, invitee, guild_id):
    # Connect to your database
    connection = get_db_connection()
    try:
        cursor = connection.cursor(buffered=True)
        
        # Query to check if the user is in the party
        stored_procedure_name = 'sp_check_if_user_is_invited'
        stored_procedure_parameters = (
            invitor,
            invitee,
            guild_id
        )
        
        # Execute the query with the provided user_id and party_id
        cursor.callproc(stored_procedure_name, stored_procedure_parameters)
        connection.commit()
                
        # Check if a result is found
        return cursor.fetchone() is not None
        
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return False
    finally:
        # Close the cursor and connection
        cursor.close()
        connection.close()
    
def insert_invitation_into_db(guild_id, party_id, invitee):
    # Connect to your database
    connection = get_db_connection()
    try:
        cursor = connection.cursor(buffered=True)
        
        # Query to check if the user is in the party
        stored_procedure_name = 'sp_insert_invitation'
        stored_procedure_parameters = (
            party_id,
            invitee,
            guild_id
        )
        
        # Execute the query with the provided user_id and party_id
        cursor.callproc(stored_procedure_name, stored_procedure_parameters)
        connection.commit()
        
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return False
    finally:
        # Close the cursor and connection
        cursor.close()
        connection.close()
        return True
    
def is_party_leader(character, guild_id):
    connection = get_db_connection()
    try:
        cursor = connection.cursor(buffered=True)
        
        # Query to check if the user is in the party
        stored_procedure_name = 'sp_get_party_leader'
        stored_procedure_parameters = (character, guild_id)
        
        # Execute the query with the provided user_id and party_id
        cursor.callproc(stored_procedure_name, stored_procedure_parameters)
        
        # Fetch the result
        result = cursor.fetchone()
    except mysql.connector.Error as error:
        print(f"Failed to retrieve data: {error}")
    finally:
        # Close the cursor and connection
        if cursor is not None and connection.is_connected():
            cursor.close()
            connection.close()
    
    # Check the result
    if result is not None:
        return True
    else:
        return False
    
def select_new_leader(party_id):
    connection = get_db_connection()
    cursor = None
    
    try:
        cursor = connection.cursor()
        
        # Name of the stored procedure and parameters
        stored_procedure_name = 'sp_update_party_leader'
        stored_procedure_parameters = (party_id, )
        
        # Call the stored procedure
        cursor.callproc(stored_procedure_name, stored_procedure_parameters)
        
        # Commit the transaction
        connection.commit()
        
        # Optionally return some result if needed
    except Error as e:
        print(f"Error: {e}")
        # Optionally return some result or re-raise the exception
    finally:
        if cursor is not None and connection.is_connected():
            cursor.close()
            connection.close()
            
def remove_user_from_party(character_id, party_id):
    connection = get_db_connection()    
    try:
        cursor = connection.cursor()
        
        # Name of the stored procedure and parameters
        stored_procedure_name = 'sp_remove_user_from_party'
        stored_procedure_parameters = (character_id, party_id)
        
        # Call the stored procedure
        cursor.callproc(stored_procedure_name, stored_procedure_parameters)
        
        # Commit the transaction
        connection.commit()
        
        # Optionally return some result if needed, e.g., a success message.
    except Error as e:
        print(f"Error: {e}")
        # Optionally return some result or re-raise the exception
    finally:
        if cursor is not None and connection.is_connected():
            cursor.close()
            connection.close()

#_______________________________________________________________________________________________________________________
def add_guild(guild_id, guild_name):
    connection = get_db_connection()    
    try:
        cursor = connection.cursor()

        # Define the stored procedure name and parameters
        stored_procedure_name = 'sp_add_guild'
        stored_procedure_parameters = (guild_id, guild_name)
        # Call the stored procedure
        cursor.callproc(stored_procedure_name, stored_procedure_parameters)
        # Commit the transaction
        connection.commit()
        print(f"Guild {guild_name} added successfully!")

    except Error as e:
        print(f"Error: {e}")

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            
async def setup(bot):
    bot.tree.add_command(utility(name="utility", description="Common utility functions, helpers, or shared logic used across cogs."))
