import discord
from discord import app_commands
from mysql.connector import Error
import logging

from utils.functions.database_functions import (
                    get_db_connection, close_db_connection)
from utils.functions.mod_functions import (
                    add_mob_to_db, delete_mob_from_db, create_mob_data, check_if_mob_exists,
                    create_buff_data, add_buff_to_db, delete_buff_from_db,
                    check_if_buff_exists)
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
        # Insert the mob data into the database
        await add_mob_to_db(db, mob_insert)
        logging.debug("Mob created successfully.")
        return await comment_wrap("Mob created successfully.")
    except Exception as e:
        logging.exception(f"Unexpected error: {e}")
        return await comment_wrap(f"An unexpected error occurred: {e}")
    finally:
        await close_db_connection(client)
        
async def delete_mob_logic(mob_data):
    try:
        client, db = await get_db_connection()
    except Exception as e:
        logging.exception("Database connection failed: %s", e)
        return await comment_wrap("There seems to be a problem. Please reach out to an administrator.")
    try:
        # Check if the mob exists
        mob_exists = await check_if_mob_exists(db, mob_data["name"], mob_data["guild_id"])
        if (not mob_exists):
            return await comment_wrap("Mob does not exist.")
        # Delete the mob from the database
        await delete_mob_from_db(db, mob_data["name"], mob_data["guild_id"])
        logging.debug("Mob deleted successfully.")
        return await comment_wrap("Mob deleted successfully.")
    except Exception as e:
        logging.exception(f"Unexpected error: {e}")
        return await comment_wrap(f"An unexpected error occurred: {e}")
    finally:
        await close_db_connection(client)
        
async def create_buff_logic(buff_data):
    try:
        client, db = await get_db_connection()
    except Exception as e:
        logging.exception("Database connection failed: %s", e)
        return await comment_wrap("There seems to be a problem. Please reach out to an administrator.")
    try:
        # Check if the buff already exists
        buff_exists = await check_if_buff_exists(db, buff_data["name"], buff_data["guild_id"])
        if (buff_exists):
            return await comment_wrap("Buff already exists.")
        buff_insert = await create_buff_data(buff_data)
        # Insert the buff data into the database
        await add_buff_to_db(db, buff_insert)
        logging.debug("Buff created successfully.")
        return await comment_wrap("Buff created successfully.")
    except Exception as e:
        logging.exception(f"Unexpected error: {e}")
        return await comment_wrap(f"An unexpected error occurred: {e}")
    finally:
        await close_db_connection(client)
        
async def delete_buff_logic(buff_data):
    try:
        client, db = await get_db_connection()
    except Exception as e:
        logging.exception("Database connection failed: %s", e)
        return await comment_wrap("There seems to be a problem. Please reach out to an administrator.")
    try:
        # Check if the buff exists
        buff_exists = await check_if_buff_exists(db, buff_data["name"], buff_data["guild_id"])
        if (not buff_exists):
            return await comment_wrap("Buff does not exist.")
        # Delete the buff from the database
        await delete_buff_from_db(db, buff_data["name"], buff_data["guild_id"])
        logging.debug("Buff deleted successfully.")
        return await comment_wrap("Buff deleted successfully.")
    except Exception as e:
        logging.exception(f"Unexpected error: {e}")
        return await comment_wrap(f"An unexpected error occurred: {e}")
    finally:
        await close_db_connection(client)
