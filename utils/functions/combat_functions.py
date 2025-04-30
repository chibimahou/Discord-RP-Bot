import logging
import math
from utils.functions.database_functions import get_db_connection, close_db_connection

async def create_combat_instance(db, guild_id, combat_instance):
    logging.info(f"Creating combat instance")
    combat_document = {
        "instance": combat_instance,
        "guild_id": guild_id,
        "combat": {
            "players_turn": None,
            "turn_order": []
        }
    }
    db["combat"].insert_one(combat_document)
    return combat_document
async def is_players_turn(db, character_data):
    logging.info(f"Checking players turn")
    combat_document = db["combat"].find_one({"instance": character_data["character"]["instance"],
                                "guild_id": character_data["guild_id"]})
    if not combat_document:
        return False
    else:
        if combat_document["combat"]["players_turn"] == character_data["discord_tag"]:
            return True 
        else:
            return False