import discord
from discord import app_commands
from mysql.connector import Error
import logging

from utils.functions.database_functions import (
                    get_db_connection, close_db_connection)
from utils.functions.mod_functions import (
                    add_mob_to_db, create_mob_data, check_if_mob_exists)
from utils.functions.utility_functions import comment_wrap

from pymongo import MongoClient

async def create_mob_logic(mob_data):
    try:
        client, db = await get_db_connection()
    except Exception as e:
        logging.exception("Database connection failed: %s", e)
        return await comment_wrap("There seems to be a problem. Please reach out to an administrator.")
    try:
        # Check if the mob already exists
        mob_exists = await check_if_mob_exists(db, mob_data["name"], mob_data["guild_id"])
        if (mob_exists):
            return await comment_wrap("Mob already exists.")
        mob_insert = await create_mob_data(mob_data)
        # Insert the character data into the database
        await add_mob_to_db(db, mob_insert)
        logging.debug("Character created successfully.")
        return await comment_wrap("Character created successfully.")
    except Exception as e:
        logging.exception(f"Unexpected error: {e}")
        return await comment_wrap(f"An unexpected error occurred: {e}")
    finally:
        await close_db_connection(client)