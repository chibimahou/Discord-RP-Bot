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
    
async def create_buff_data(buff_data):
    buff_insert = {
    "buff": {  "name": buff_data["name"],
        "description": buff_data["description"],
    },
    "effect_1": {  "stat": buff_data["stat_1"],
                    "operation": buff_data["operation_1"],
                    "value": buff_data["value_1"],
                    "activates": buff_data["activates_1"],
    },
    "effect_2": {  "stat": buff_data["stat_2"],
                    "operation": buff_data["operation_2"],
                    "value": buff_data["value_2"],
                    "activates": buff_data["activates_2"],
    },
    "debuff_1": {  "stat": buff_data["debuff_stat_1"],
                    "operation": buff_data["debuff_operation_1"],
                    "value": buff_data["debuff_value_1"],
                    "activates": buff_data["debuff_activates_1"],
    },
    "debuff_2": {  "stat": buff_data["debuff_stat_2"],
                    "operation": buff_data["debuff_operation_2"],
                    "value": buff_data["debuff_value_2"],
                    "activates": buff_data["debuff_activates_2"],
    },
        "misc": {"inserted_by": buff_data["inserted_by"],
                "insertion_date": buff_data["insertion_date"],
                "guild_id": buff_data["guild_id"]
        }
    }
    return buff_insert

async def add_mob_to_db(db, character_data):
    # Insert the character data into the database
    await db['mobs'].insert_one(character_data)
    return "Mob successfully created!"

async def delete_mob_from_db(db, name, guild_id):
    # Insert the character data into the database
    await db['mobs'].delete_one({"mob.name": name, "misc.guild_id": guild_id})
    return "Mob successfully removed!"

async def check_if_mob_exists(db, mob_name, guild_id):
    mob = await db['mobs'].find_one({"mob.name": mob_name, "misc.guild_id": guild_id})
    return mob

async def add_buff_to_db(db, buff_data):
    # Insert the character data into the database
    await db['buffs'].insert_one(buff_data)
    return "Buff successfully created!"

async def delete_buff_from_db(db, name, guild_id):
    # Insert the character data into the database
    await db['buffs'].delete_one({"buff.name": name, "misc.guild_id": guild_id})
    return "Buff successfully removed!"

async def check_if_buff_exists(db, buff_name, guild_id):
    buff = await db['buffs'].find_one({"buff.name": buff_name, "misc.guild_id": guild_id})
    return buff