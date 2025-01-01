import logging
import math
from utils.functions.database_functions import get_db_connection, close_db_connection
from utils.functions.character_functions import active_character

# moderation
#_______________________________________________________________________________________________________________________
# add character data to an object
async def create_mob_data(mob_data):
    mob_insert = {
    "mob": {  "name": mob_data["name"],
        "type": "monster",
        "description": mob_data["description"],
        "average_level": mob_data["average_level"],
        "exp_reward": mob_data["exp_reward"],
    },
    "loot": {
    },
    "equipment": {  "head": mob_data["equipment_head"],
                            "chest": mob_data["equipment_body"],
                            "legs": mob_data["equipment_legs"],
                            "feet": mob_data["equipment_feet"],
                            "hands": mob_data["equipment_hands"],
                            "main_hand": mob_data["equipment_main_hand"],
                            "off_hand": mob_data["equipment_off_hand"],
                            "accessory1": mob_data["equipment_accessory_1"],
                            "accessory2": mob_data["equipment_accessory_2"]
    },
    "stats": {  "hp": mob_data["hp"],
                    "str": mob_data["strength"],
                    "def": mob_data["defense"],
                    "spe": mob_data["speed"],
                    "dex": mob_data["dexterity"],
                    "cha": mob_data["charisma"],
        },
        "misc": {"inserted_by": mob_data["inserted_by"],
                    "insertion_date": mob_data["insertion_date"],
                    "guild_id": mob_data["guild_id"]
        }
    }
    return mob_insert
    
async def add_mob_to_db(db, character_data):
    # Insert the character data into the database
    await db['mobs'].insert_one(character_data)
    return "Character successfully created!"

async def check_if_mob_exists(db, mob_name, guild_id):
    mob = await db['mobs'].find_one({"mob.name": mob_name, "misc.guild_id": guild_id})
    return mob