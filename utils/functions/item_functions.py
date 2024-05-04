import logging
import math

async def get_item(db, item_data):
    logging.info(f"Getting item: {item_data['name']}")
    return await db["items"].find_one({"name": item_data["name"],
                                "guild_id": item_data["guild_id"]})