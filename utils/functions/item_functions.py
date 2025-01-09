import logging
import math

async def get_item(db, identifier, guild_id):
    logging.info(f"Getting item: {identifier}")
    return db["items"].find_one({"name": identifier,
                                "guild_id": guild_id})

async def check_if_item_exists(db, identifier, guild_id):
    item = await get_item(db, identifier, guild_id)
    if item:
        return True
    return False

async def add_item_to_db(db, item_data):
    # Insert the character data into the database
    await db['items'].insert_one(item_data)
    return "Item successfully created!"

