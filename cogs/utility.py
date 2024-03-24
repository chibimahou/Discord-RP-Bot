import discord
import logging
import re
from discord import app_commands
from datetime import datetime
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
from motor.motor_asyncio import AsyncIOMotorClient


async def get_db_connection():
    client = AsyncIOMotorClient(URI)
    db = client[DB_NAME]
    return client, db

async def close_db_connection(db):
    # MongoDB uses a different approach to close connections. However, MongoClient automatically handles connection pooling.
    # It's generally safe to reuse MongoClient instances across your application.
    # Explicitly closing connection is often not necessary, but if you need to, you can call client.close()
    db.close()
#_______________________________________________________________________________________________________________________
# select active character name
async def active_character(discord_tag):
    client, db = await get_db_connection()
    try:
        character_document = await db["characters"].find_one({"discord_tag": discord_tag, "active": True})
        if character_document:
            character_name = character_document.get("characters_name")
            return character_name, "Data fetched successfully!"
        else:
            return None, "No active character found for this Discord tag."
    except Exception as e:
        logging.exception(f"Error fetching active character: {e}")
        return None, f"Error fetching active character: {e}"
    finally:
        await close_db_connection(client)
        
# validate character exists in the database
async def validate_character_exists(character_name, discord_tag):
    client, db = await get_db_connection()
    try:
        character_document = await db["characters"].find_one({"discord_tag": discord_tag, "characters_name": character_name})
        if character_document:
            return True
        else:
            return False
    except Exception as e:
        logging.exception(f"Error validating character: {e}")
        return False
    finally:
        await close_db_connection(client)
        
# return all characters for a user
async def available_characters(discord_tag):
    client, db = await get_db_connection()
    try:
        # Await the to_list coroutine to get the actual list of characters
        characters = await db["characters"].find({"discord_tag": discord_tag}).to_list(length=None)
        return characters
    except Exception as e:
        logging.exception(f"Error fetching characters: {e}")
        return []
    finally:
        await close_db_connection(client)


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
    db = get_db_connection()
    if db is None:
        logging.err("Failed to connect to the database.")
        return False
    
    try:
        # Assuming 'PartyMemberships' is the collection where membership information is stored
        # This query looks for a document where the user_id and guild_id fields match the provided arguments
        membership = db.PartyMemberships.find_one({"user_id": user_id, "guild_id": guild_id})
        
        # If a document is found, it means the user is in a party within the specified guild
        return membership is not None
        
    except Exception as e:
        print(f"Error: {e}")
        return False
  
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
    db = get_db_connection()
    if db is None:
        print("Failed to connect to the database.")
        return
    
    try:
        # Assuming you have a 'parties' collection and each party document has a 'members' array
        # First, find the party by its ID
        party = db.parties.find_one({"_id": party_id})
        if party:
            # Assuming party['members'] is a list of member IDs and you choose a new leader somehow
            # For example, let's randomly select a new leader from members
            import random
            new_leader_id = random.choice(party['members'])
            
            # Now, update the party document with the new leader ID
            # Assuming there's a 'leader_id' field in the party document
            db.parties.update_one({"_id": party_id}, {"$set": {"leader_id": new_leader_id}})
            print("New leader selected successfully.")
        else:
            print("Party not found.")
        
    except Exception as e:
        print(f"Error selecting new leader: {e}")

def remove_user_from_party(character_id, party_id):
    db = get_db_connection()
    if db is None:
        print("Failed to connect to the database.")
        return "Failed to connect to the database."
    
    try:
        # Convert string IDs to ObjectId if they're not already in that format
        if isinstance(character_id, str):
            character_id = bson.ObjectId(character_id)
        if isinstance(party_id, str):
            party_id = bson.ObjectId(party_id)
        
        # Update the party document to remove the character from the members array
        update_result = db.parties.update_one(
            {"_id": party_id},
            {"$pull": {"members": character_id}}
        )
        
        # Check if the update operation was successful
        if update_result.modified_count > 0:
            print("User removed from party successfully.")
            return "User removed from party successfully."
        else:
            print("Failed to remove user from party or user was not in party.")
            return "Failed to remove user from party or user was not in party."
    except Exception as e:
        print(f"Error: {e}")
        return "Error removing user from party."

#_______________________________________________________________________________________________________________________
def add_guild(guild_id, guild_name):
    db = get_db_connection()
    if db is None:
        print("Failed to connect to the database.")
        return
    
    try:
        # Assuming 'guilds' is the collection where guild information is stored
        # Create a new guild document
        guild_document = {
            "_id": guild_id,
            "name": guild_name
        }
        
        # Insert the new guild document into the 'guilds' collection
        insert_result = db.guilds.insert_one(guild_document)
        
        if insert_result.inserted_id:
            print(f"Guild {guild_name} added successfully!")
        else:
            print("Failed to add the guild.")
    except Exception as e:
        print(f"Error adding guild: {e}")

async def setup(bot):
    bot.tree.add_command(utility(name="utility", description="Common utility functions, helpers, or shared logic used across cogs."))
