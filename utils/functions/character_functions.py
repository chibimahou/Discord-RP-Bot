import logging
import math
from utils.functions.database_functions import get_db_connection, close_db_connection
# Characters
#_______________________________________________________________________________________________________________________

def construct_player_data(character_data, include_active=False, characters_name=None):
    fields_to_check = ['discord_tag', 'guild_id']
    query = {
        f"player.{field}": character_data[field]
        for field in fields_to_check
        if field in character_data
    }
    if include_active:
        query["player.active"] = True
    if characters_name:
        query["character.characters_name"] = characters_name
    return query
    
# add character data to an object
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
    "equipped:": {"head": None,
                      "chest": None,
                      "legs": None,
                      "arms": None,
                      "accessory1": None,
                      "accessory2": None,
                      "left_hand": None,
                      "right_hand": None},
    "group": {"guild": None,
                "party": None},
    "stats": {  "hp": 10,
                "str": 5,
                "def": 5,
                "spe": 5,
                "dex": 5,
                "cha": 5,
                "points_to_distribute": 0
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
    player_data = construct_player_data(character_data, include_active=True)
    character_document = await db["characters"].find_one(player_data)
    if character_document:
        return character_document
    else:
        logging.debug("No active character found.")
        return None

# Delete a character from the database
async def delete_character(db, character_data):
    try:
        player_data = construct_player_data(character_data, False, character_data['characters_name'])
        character_document = await db['characters'].find_one(player_data)
        if not character_document:
            logging.info("Character not found or already deleted.")
            return "```Character not found or already deleted.```"
        if character_document.get("player", {}).get("active", False):
            logging.info("Cannot delete an active character.")
            return "```Cannot delete an active character. Please switch to another character before deleting.```"
        delete_result = await db['characters'].delete_one(player_data)
        if delete_result.deleted_count > 0:
            logging.info("Character successfully deleted.")
            return "```Character successfully deleted!```"
        else:
            logging.info("Character not found or already deleted.")
            return "```Character not found or already deleted.```"
    except Exception as e:
        logging.exception(f"Error: {e}")
        return "```An error occurred while attempting to delete the character.```"
        
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
    player_data = construct_player_data(character_data)

    try:
        # Await the to_list coroutine to get the actual list of characters
        characters = await db["characters"].find(player_data).to_list(length=None)
        logging.debug(f"Characters found: {characters}")
        return characters
    except Exception as e:
        logging.exception(f"Error fetching characters: {e}")
        return []
    finally:
        await close_db_connection(client)

# Add points to the assigned stat
async def add_points_to_stat(db, character_data):
    player_data = construct_player_data(character_data, include_active=True)
    # If the field stat points to distripbution is empty, return a failure message
    character_document = await db["characters"].find_one(player_data)
    if character_document:
            # If the field stat points to distripbution is empty, return a failure message
            stat_points_left = character_document["stats"]["points_to_distribute"] - character_data['stat_value']
            if stat_points_left >= 0:
                # Convert the stat name to common names
                converted_stat_name = await convert_stat_name(character_data['stat_name'].lower())
                logging.debug(f"Converted stat name: {converted_stat_name}")
                logging.debug (character_document["stats"])
                # Add points to the stat
                updated_stat_value = character_document["stats"][converted_stat_name] + character_data['stat_value']
                logging.debug(f"Current stat value: {updated_stat_value}")
                # Update the character's stats
                update = await db["characters"].update_one(player_data,
                    {
                        "$set": {
                            f"stats.{converted_stat_name}": updated_stat_value,
                            "stats.points_to_distribute": stat_points_left
                        }
                    })
                # If the update was successful, update the corresponding stat
                if (update.modified_count > 0):
                    logging.debug(f"Stat: {character_document['stats'][converted_stat_name]} updated to {updated_stat_value} for {character_data['discord_tag']}")
                    # message = await update_combat(converted_stat_name, updated_stat_value, character_document["stats"][converted_stat_name], "add", character_data['discord_tag'], converted_stat_name['guild_id'])
                logging.info(f"{character_data['stat_value']} point(s) added to {converted_stat_name} for player {character_document['character']['characters_name']}.\nStat points remaining: {stat_points_left}")
                return f"{character_data['stat_value']} point(s) added to {converted_stat_name} for player {character_document['character']['characters_name']}.\nStat points remaining: {stat_points_left}"
            else:
                return f"You do not have enough stat points to distribute. Stat points remaining: {character_document['stats']['points_to_distribute']}"

    else:
            return f"No active character found for {character_data['discord_tag']}"
        
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
            player_data = construct_player_data(character_data, include_active=True)
            # Add increase to level annd add stat points to distribute
            updated_level = character_document["character"]["level"] + 1
            updated_points_to_distribute = character_document["stats"]["points_to_distribute"] + 3
            # Update the character's level and stat points to distribute
            update = await db["characters"].update_one(player_data,
                    {
                        "$set": {
                            "character.level": updated_level,
                            "stats.points_to_distribute": updated_points_to_distribute
                        }
                    })
            # If the update was successful, update the corresponding stat
            if (update.modified_count > 0):
                return True
            else:
                return False

async def update_combat(stat_name, updated_stat_value, points_to_remove, add_or_remove, discord_tag, guild_id):
    client, db = await get_db_connection()
    try:
        character_document = await db["characters"].find_one({
            "player.discord_tag": discord_tag,
            "player.guild_id": guild_id,
            "player.active": True
        })
        if(character_document):
            # TODO: Add check for weapon damage type
            # If weapon damage type is str and stat points are added to str, then run the update.
            # If they are different, skip the update.
            
            if(stat_name == "str"):
            # Update base damage using the formula base_damage = dex (+/-) dex_weapon_damage
            # Update graze chance using the formula graze_chance = old_graze_chance (+/-) (dex (+/-) dex_graze_chance)
                combat_stat_name = "damage"
                logging.debug(f"Updating {combat_stat_name} for {discord_tag}")
                update_field = await updated_damage_value(character_document, updated_stat_value, points_to_remove, add_or_remove, discord_tag, guild_id, combat_stat_name)
            elif(stat_name == "dex" and add_or_remove == "add"):
                original_damage = character_document["combat"]["damage"] + points_to_remove
                original_graze_chance = character_document["combat"]["graze_chance"] - math.floor(character_document["stats"]["dex"])
                update_field = original_graze_chance + math.floor(updated_stat_value/5)
            elif(stat_name == "dex" and add_or_remove == "remove"):
                update_combat_field = character_document["combat"]["damage"] - updated_stat_value
                update_field = character_document["combat"]["graze_chance"] - math.floor(updated_stat_value / 5)
            # Update initiative using the formula initiative = str (+/-) weapon_damage
            elif(stat_name == "spe" and add_or_remove == "add"):
                original_initiative = character_document["combat"]["initiative"] - math.floor(character_document["stats"]["spe"])
                update_field = original_initiative + math.floor(updated_stat_value / 2)
            elif(stat_name == "spe" and add_or_remove == "remove"):
                update_field = character_document["combat"]["initiative"] - (updated_stat_value / 2)
            # Update initiative using the formula initiative = str (+/-) weapon_damage
            elif(stat_name == "cha" and add_or_remove == "add"):
                original_initiative = character_document["combat"]["initiative"] - math.floor(character_document["stats"]["spe"])
                update_field = original_initiative + math.floor(updated_stat_value / 2)
            elif(stat_name == "cha" and add_or_remove == "remove"):
                update_field = character_document["combat"]["initiative"] - (updated_stat_value / 2)
            # Update initiative using the formula initiative = str (+/-) weapon_damage
            elif(stat_name == "def" and add_or_remove == "add"):
                original_initiative = character_document["combat"]["initiative"] - math.floor(character_document["stats"]["spe"])
                update_field = original_initiative + math.floor(updated_stat_value / 2)
            elif(stat_name == "def" and add_or_remove == "remove"):
                update_field = character_document["combat"]["initiative"] - (updated_stat_value / 2)
            logging.debug(f"test 2")
            # Update the character's combat stats
            update = await db["characters"].update_one(
                {
                    "player.discord_tag": discord_tag,
                    "player.guild_id": guild_id,
                    "player.active": True
                },
                {
                    "$set": {
                        f"combat.{combat_stat_name}": update_field
                    }
                })
            return "Successfully updated combat stats."
    except Exception as e:
        logging.exception(f"Error updating combat stats: {e}")
        return "Failed to update combat stats"
    finally:
        await close_db_connection(client)  
            
async def updated_damage_value(character_document, updated_stat_value, points_to_remove, add_or_remove, discord_tag, guild_id, damage):
    # Update base damage using the formula base_damage = str (+/-) str_weapon_damage
    if add_or_remove == "add":
        logging.debug(f"points to remove: {points_to_remove}")
        logging.debug(f"Updating damage for {character_document['character']['characters_name']}: original damage value: {character_document['combat']['damage'] - points_to_remove} New Value: {(character_document['combat']['damage'] - points_to_remove) + updated_stat_value}")
        original_damage = character_document["combat"]["damage"] - points_to_remove
        update_field = original_damage + updated_stat_value
    else:
        update_field = character_document["combat"]["damage"] - updated_stat_value
        
        
    return update_field

async def updated_defense_value(character_document, updated_stat_value, points_to_remove, add_or_remove, discord_tag, guild_id, damage):
    # Update base defense using the formula base_damage = def (+/-) str_weapon_damage
    if add_or_remove == "add":
        original_damage = character_document["combat"]["defense"] - points_to_remove
        update_field = original_damage + updated_stat_value
    else:
        update_field = character_document["combat"]["defense"] - updated_stat_value
        
    return update_field

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
    player_data = construct_player_data(character_data, include_active=True)
    logging.info(f"Character data: {character_data}")
    return await db["characters"].find_one(player_data)

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