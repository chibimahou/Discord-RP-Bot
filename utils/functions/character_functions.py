import logging
import math
import copy
from utils.functions.database_functions import get_db_connection, close_db_connection
# Characters
#_______________________________________________________________________________________________________________________

# ______________________________________________________________________________________________________________________   
# Description: add character data to a JSON object
# Return: Object
# ______________________________________________________________________________________________________________________   
async def create_character_insert(character_data):
    character_insert = {
    "character": {  "first_name": character_data["first_name"],
                        "last_name": character_data["last_name"],
                        "characters_name": character_data["characters_name"],
                        "class": "None",
                        "cursor_color": "Green",
                        "height": character_data["height"],
                        "physique": character_data["physique"],
                        "age": character_data["age"],
                        "birthday": character_data["birthday"],
                        "bio": character_data["bio"],
                        "level": 1,
                        "experience": 0,
                        "experience_to_next_level": 100
                        },
    "inventory": {"equipment": [], 
                      "consumables": [], 
                      "misc": [], 
                      "cratable": [],
                      "key_items": [],
                      "currency": 0},
    "equipped": {"head": {"name": None,
                           "modifier": 1},
                      "chest": {"name": None,
                           "modifier": 1},
                      "legs": {"name": None,
                           "modifier": 1},
                      "arms": {"name": None,
                           "modifier": 1},
                      "accessory1": {"name": None,
                           "modifier": 1},
                      "accessory2": {"name": None,
                           "modifier": 1},
                      "left_hand": {"name": None,
                           "modifier": 1,
                           "atk_type": "str"},
                      "right_hand": {"name": None,
                           "modifier": 1}},
    "group": {"guild": None,
                "party": None},
    "stats": {
        "base": {
            "hp": 10,
            "str": 5,
            "def": 5,
            "spe": 5,
            "dex": 5,
            "cha": 5,
            "points_to_distribute": 0
        },
        "modified": {
            "hp": 10,
            "str": 5,
            "def": 5,
            "spe": 5,
            "dex": 5,
            "cha": 5,
        }
    },
    "combat": { "status_ailment": None,
                "battle_status": False,
                "damage": 10,
                "defense": 10,
                "current_hp": 10,
                },
    "player": {"discord_tag": character_data["discord_tag"],
                "guild_id": character_data["guild_id"],
                "active": False}}
    return character_insert
    
async def create_character(db, character_data):
    # Insert the character data into the database
    await db['characters'].insert_one(character_data)
    return "Character successfully created!"
        
# select active character name
async def active_character(db, character_data):
    character_document = await db["characters"].find_one(
            {
                "player.discord_tag": character_data['discord_tag'], 
                "player.guild_id": character_data['guild_id'], 
                "player.active": True
            }
        )
    if character_document:
        return character_document
    else:
        logging.debug("No active character found.")
        return None

# Delete a character from the database
async def delete_character(db, character_data):
    if db is None:
        logging.error("Connection to MongoDB failed.")
        return "Failed to connect to the database."
    try:
        delete_result = await db['characters'].delete_one({
            "character.characters_name": character_data["characters_name"],
            "player.discord_tag": character_data["discord_tag"],
            "player.guild_id": character_data["guild_id"]
        })
        if delete_result.deleted_count > 0:
            logging.info("Character successfully deleted.")
            return "Character successfully deleted!"
        else:
            logging.info("Character not found or already deleted.")
            return "Character not found or already deleted."
    except Exception as e:
        logging.exception(f"Error: {e}")
        return "An error occurred while attempting to delete the character."
    finally:
        await close_db_connection(client)
        
# Switch the active character for a user
async def switch_active_character(db, character_data, character_documnent, new_characters_document):
        #Validate that a character is active
        # If there is an active character, set it to inactive
            set_inactive = await set_active_status(db, character_documnent, False)
            # Validate if the character was set to inactive
            if set_inactive:
                # Set the new character as active
                set_active = await set_active_status(db, new_characters_document, True)
                if set_active:
                    logging.info(f"Character {character_data['characters_name']} set to active.")
                    return True
                else:
                    logging.info(f"Failed to set {character_data['characters_name']} to active.")
                    return False
            else:
                logging.info(f"Failed to set {character_documnent['character']['characters_name']} to inactive.")
                return False
        
# Set a characters active status to False
async def set_active_status(db, character_document, set_to):
    logging.debug(f"{character_document['_id']}")
    update = await db['characters'].update_one({"_id": character_document['_id']},
                                                  {"$set": {"player.active": set_to}})
    logging.debug(update.modified_count)
    if update.modified_count > 0:
        if set_to:
            logging.info(f"Character {character_document['character']['characters_name']} set to active.")
            return True
        logging.info(f"Character {character_document['character']['characters_name']} set to inactive.")
        return True
    else:
        logging.info(f"Failed to set {character_document['character']['characters_name']}'s active status")
        return False
    
# return all characters for a user
async def available_characters(character_data):
    client, db = await get_db_connection()
    try:
        # Await the to_list coroutine to get the actual list of characters
        characters = await db["characters"].find({
            "player.discord_tag": character_data['discord_tag'],
            "player.guild_id": character_data['guild_id']
            }).to_list(length=None)
        logging.debug(f"Characters found: {characters}")
        return characters
    except Exception as e:
        logging.exception(f"Error fetching characters: {e}")
        return []
    finally:
        await close_db_connection(client)

# Check available stat points
async def available_points(character_document):
    return character_document["stats"]['base']["points_to_distribute"]

# Add points to the assigned stat
async def add_points_to_stat(db, character_data, character_document):
    # If the field stat points to distripbution is empty, return a failure message
        # If the field stat points to distripbution is empty, return a failure message
        stat_points_left = character_document["stats"]['base']["points_to_distribute"] - character_data['stat_value']
        # Add points to the stat
        updated_stat_value = character_document["stats"]['base'][character_data['stat_name']] + character_data['stat_value']
        updated_modified_value = character_document["stats"]['modified'][character_data['stat_name']] + character_data['stat_value']
        logging.debug(f"Current stat value: {updated_stat_value}")
        # Update the character's stats
        update = await db["characters"].update_one(
        {
            "player.discord_tag": character_data['discord_tag'],
            "player.guild_id": character_data['guild_id'],
            "player.active": True
        },
        {
            "$set": {
                f"stats.base.{character_data['stat_name']}": updated_stat_value,
                f"stats.base.points_to_distribute": stat_points_left,
                f"stats.modified.{character_data['stat_name']}": updated_modified_value
            }
        })
        # If the update was successful, return a True
        if (update.modified_count > 0):
            return True
        return False

# Convert the stat name to common names
async def convert_stat_name(stat_name):
    if(stat_name == "strength" or stat_name == "attack" or stat_name == "atk" or stat_name == "str"):
        return "str"
    elif(stat_name == "dexterity" or stat_name == "dex"):
        return "dex"
    elif(stat_name == "constitution"  or stat_name == "defense" or stat_name == "con" or stat_name == "def"):
        return "def"
    elif(stat_name == "charisma" or stat_name == "cha"):
        return "cha"
    elif(stat_name == "speed" or stat_name == "agility" or stat_name == "spe" or stat_name == "spd" or stat_name == "agi"):
        return "spe"
    else:
        return None
    
async def level_up(db, character_data, character_document):
            # Add increase to level annd add stat points to distribute
            updated_level = character_document["character"]["level"] + 1
            updated_points_to_distribute = character_document["stats"]['base']["points_to_distribute"] + 3
            # Update the character's level and stat points to distribute
            update = await db["characters"].update_one(
                {
                        "player.discord_tag": character_data['discord_tag'],
                        "player.guild_id": character_data['guild_id'],
                        "player.active": True
                    },
                    {
                        "$set": {
                            "character.level": updated_level,
                            "stats.base.points_to_distribute": updated_points_to_distribute
                        }
                    })
            # If the update was successful, update the corresponding stat
            if (update.modified_count > 0):
                return True
            else:
                return False

async def calculate_base_damage(character_document, item_document):
    if item_document is None:
        return character_document['stats']['modified'][item_document['atk_type']]
    
    return (item_document['damage'] + character_document['stats']['modified'][item_document['atk_type']]) * item_document['modifier']

async def calculate_base_defense(character_document):
    total_armor_def = sum(armor['base_def'] for armor in character_document['equipment']['armor'])
    return (total_armor_def + character_document['stats']['def']) * character_document['equipment']['armor_modifier']

async def update_combat_stats(db, character_document, item_document, stats_to_update):
    try:
        updates = {}

        if 'str' in stats_to_update or 'dex' in stats_to_update:
            base_damage = await calculate_base_damage(character_document, item_document)
            updates['combat.damage'] = base_damage

        if 'dex' in stats_to_update:
            graze_chance = character_document['stats']['dex'] // 3
            updates['combat_stats.graze_chance'] = graze_chance

        if 'spe' in stats_to_update:
            initiative = character_document['stats']['spe']
            updates['combat_stats.initiative'] = initiative

        if 'def' in stats_to_update:
            base_defense = await calculate_base_defense(character_document)
            updates['combat_stats.base_defense'] = base_defense

        if 'cha' in stats_to_update:
            taming_bond = character_document['stats']['cha']
            updates['combat_stats.taming_bond'] = taming_bond

        if updates:
            update_result = await db['characters'].update_one(
                {"_id": character_document['_id']},
                {"$set": updates}
            )
            return update_result.modified_count > 0

        return False

    except Exception as e:
        logging.exception("Failed to update combat stats: %s", e)
        return False        

async def updated_initiative_value(character_document, updated_stat_value, points_to_remove, add_or_remove, discord_tag, guild_id, damage):
    # Update initiative using the formula base_damage = spe (+/-) str_weapon_damage
    if add_or_remove == "add":
        original_damage = character_document["combat"]["initiative"] - points_to_remove
        update_field = original_damage + updated_stat_value
    else:
        update_field = character_document["combat"]["initiative"] - updated_stat_value
        
    return update_field

async def updated_graze_value(character_document, updated_stat_value, points_to_remove, add_or_remove, discord_tag, guild_id, damage):
    # Update graze chance using the formula base_damage = dex (+/-) dex_weapon_damage
    if add_or_remove == "add":
        original_damage = character_document["combat"]["graze_chance"] - points_to_remove
        update_field = original_damage + updated_stat_value
    else:
        update_field = character_document["combat"]["graze_chance"] - updated_stat_value
        
    return update_field

async def updated_taming_value(character_document, updated_stat_value, points_to_remove, add_or_remove, discord_tag, guild_id, damage):
    # Update taming chance using the formula base_damage = cha (+/-) str_weapon_damage
    if add_or_remove == "add":
        original_damage = character_document["combat"]["taming"] - points_to_remove
        update_field = original_damage + updated_stat_value
    else:
        update_field = character_document["combat"]["taming"] - updated_stat_value
        
    return update_field

async def get_active_character(db, character_data):
    logging.info(f"Character data: {character_data}")
    return await db["characters"].find_one(
        {
            "player.discord_tag": character_data["discord_tag"], 
            "player.guild_id": character_data["guild_id"],
            "player.active": True
        })

async def update_characters_party(db, character_document, party_id):
    return await db["characters"].update_one(
        {
            "_id": character_document['_id']
        },
        {
            "$set": {
                "group.party_id": party_id
            }
        })

async def check_character_exists(db, character_data):
    return bool(await db["characters"].find_one(
        {
            "character.characters_name": character_data["characters_name"],
            "player.guild_id": character_data["guild_id"]
        }))
    
# Get a character by characters_name
async def get_character_by_name(db, character_data):
    return await db["characters"].find_one(
        {
            "character.characters_name": character_data['characters_name'],
            "player.guild_id": character_data["guild_id"]
        })