import logging
import math
from utils.functions.database_functions import get_db_connection, close_db_connection
from utils.functions.character_functions import active_character

# moderation
#_______________________________________________________________________________________________________________________

# Add points to the assigned stat
async def add_points_to_stat(discord_tag, guild_id, stat_name, points_to_add):
    client, db = await get_db_connection()
    # If the field stat points to distripbution is empty, return a failure message
    try:
        character_document = await db["characters"].find_one({
            "player.discord_tag": discord_tag,
            "player.guild_id": guild_id,
            "player.active": True
        })
        if character_document:
            # If the field stat points to distripbution is empty, return a failure message
            if character_document["stats"]["points_to_distribute"] > 0:
                # Convert the stat name to common names
                converted_stat_name = await convert_stat_name(stat_name.lower())
                logging.debug(f"Converted stat name: {converted_stat_name}")
                logging.debug (character_document["stats"])
                # Add points to the stat
                updated_stat_value = character_document["stats"][converted_stat_name] + points_to_add
                logging.debug(f"Current stat value: {updated_stat_value}")
                # Update the character's stats
                update = await db["characters"].update_one(
                    {
                        "player.discord_tag": discord_tag,
                        "player.guild_id": guild_id,
                        "player.active": True
                    },
                    {
                        "$set": {
                            f"stats.{converted_stat_name}": updated_stat_value
                        }
                    })
                # If the update was successful, update the corresponding stat
                if (update.modified_count > 0):
                    logging.debug(f"Stat: {character_document['stats'][stat_name]} updated to {updated_stat_value} for {discord_tag}")
                    message = await update_combat(converted_stat_name, updated_stat_value, character_document["stats"][stat_name], "add", discord_tag, guild_id) 
                logging.info(f"{points_to_add} points added to {converted_stat_name} for {discord_tag}")
                return f"{points_to_add} points added to {converted_stat_name} for {discord_tag}"
            else:
                return f"You do not have enough stat points to distribute. Stat points remaining: {character_document['stats']['points_to_distribute']}"

        else:
            return f"No active character found for {discord_tag}"
    except Exception as e:
        logging.exception(f"Error adding points to stat: {e}")
        return "Failed to add points to stat"
    finally:
        await close_db_connection(client)
        
# Convert the stat name to common names
async def convert_stat_name(stat_name):
    if(stat_name == "strength" or stat_name == "attack" or stat_name == "atk" or stat_name == "str"):
        return "str"
    elif(stat_name == "dexterity"):
        return "dex"
    elif(stat_name == "constitution"  or stat_name == "defense" or stat_name == "con" or stat_name == "def"):
        return "def"
    elif(stat_name == "charisma" or stat_name == "cha"):
        return "cha"
    elif(stat_name == "speed" or stat_name == "agility" or stat_name == "spe" or stat_name == "spd" or stat_name == "agi"):
        return "spe"
    else:
        return None
    
async def level_up(discord_tag, guild_id):
    client, db = await get_db_connection()
    try:
        character_document = await db["characters"].find_one({
            "player.discord_tag": discord_tag,
            "player.guild_id": guild_id,
            "player.active": True
        })
        if character_document:
            # Add increase to level annd add stat points to distribute
            updated_level = character_document["character"]["level"] + 1
            updated_points_to_distribute = character_document["stats"]["points_to_distribute"] + 3
            # Update the character's level and stat points to distribute
            update = await db["characters"].update_one(
                {
                        "player.discord_tag": discord_tag,
                        "player.guild_id": guild_id,
                        "player.active": True
                    },
                    {
                        "$set": {
                            "character.level": updated_level,
                            "stats.points_to_distribute": updated_points_to_distribute
                        }
                    })
            # If the update was successful, update the corresponding stat
            if (update.modified_count > 0):
                return f"Level up! You are now level {updated_level}. You have 5 points to distribute."
            else:
                return f"You do not have enough stat points to distribute. Stat points remaining: {character_document['stats']['points_to_distribute']}"
        else:
            return f"No active character found for {discord_tag}"
    except Exception as e:
        logging.exception(f"Error adding points to stat: {e}")
        return "Failed to add points to stat"
    finally:
        await close_db_connection(client)
        
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

async def check_if_mob_exists(mob_data):  
    client, db = await get_db_connection()
    if db is None:
        return False

    try:
        # Assuming 'Mobs' is the collection within your MongoDB database
        # Check if the mob exists based on the provided mob data
        existing_mob = await db['mobs'].find_one({
            "mob_name": mob_data['mob_name'],
            "guild_id": mob_data['guild_id'] 
        })
        logging.debug(f"Checking if mob exists with data: {mob_data}")
        logging.debug(f"Existing mob data: {existing_mob}")
        
        if existing_mob is not None:
            return True
        else:
            return False

    except Exception as e:
        logging.debug(f"An error occurred: {e}")
        return False


async def add_mob(mob_data): 
    client, db = await get_db_connection()
    if db is None:
        return False
    
    try:
        if await check_if_mob_exists(mob_data):
            return "mob already exists."
        
        result= await insert_mob(mob_data)
        
        if result:
            return 'mob added successfully!'
        else:
            return 'False'
        
    except Exception as e:
        print(f"An error occured: {e}")
        return "False"
    
async def insert_mob(mob_data): 
    client, db = await get_db_connection()
    if db is None:
        return False
    
    try: 
        db["mobs"].insert_one(mob_data)
        
        return True
    except Exception as e:
        print(f"An error occurred: {e}")
        return False
    
async def remove_mob(mob_name):
    client, db = await get_db_connection()
    if db is None:
     return False
 
    try:
        existing_mob =db["mobs"].find_one({"mob_name": mob_name})
        if not existing_mob:
            return False
        
        
        db["mobs"].delete_one({"mob_name": mob_name})
        
        return True
    except Exception as e:
        print(f"An error occurred: {e}")
        return False
    



