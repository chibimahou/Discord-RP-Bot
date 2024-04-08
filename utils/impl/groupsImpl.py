import discord
import logging
from discord import app_commands
from datetime import datetime
from mysql.connector import Error
from utils.functions.character_functions import get_active_character, update_characters_party
from utils.functions.group_functions import party_exists, update_party_document
from utils.functions.database_functions import get_db_connection, close_db_connection
from utils.functions.utility_functions import comment_wrap

async def party_invite_logic(invite_data, interaction):
    try:
        client, db = await get_db_connection()
    except Exception as e:
        logging.exception("Database connection failed: %s", e)
        return await comment_wrap("Database connection failed.")
    
    
    return ()

async def create_party_logic(party_data):
    try:
        client, db = await get_db_connection()
    except Exception as e:
        logging.exception("Database connection failed: %s", e)
        return await comment_wrap("Database connection failed.")
    
    try:
        character_document = await get_active_character(db, party_data)
        logging.debug(f"Create Party: Obtained Character Data")
        if not character_document:
            return comment_wrap("You don't have an active character.")
        if await party_exists(db, party_data, character_document):
            return comment_wrap("You are already in a party.") 
        # Insert the party data into the database
        current_date = datetime.now()
        date_string = current_date.strftime('%Y-%m-%d')
        party_data["creation_date"] = date_string
        party_insert = await update_party_document(party_data, character_document) 
        update = await db["parties"].insert_one(party_insert)   
        if update:
            await update_characters_party(db, character_document, update.inserted_id) 
            return comment_wrap("Party created successfully.")
        return comment_wrap("Failed to add party.")
    except Exception as e:
        logging.exception(f"Create_Party: Error getting character data: {e}")
        return comment_wrap("An unexpected error occurred.")
    finally:
        await close_db_connection(client)

