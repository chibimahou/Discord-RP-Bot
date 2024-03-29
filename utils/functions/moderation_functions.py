import logging
from utils.functions.database_functions import get_db_connection, close_db_connection
from utils.functions.character_functions import active_character

# moderation
#_______________________________________________________________________________________________________________________

# Add points to the assigned stat
async def add_points_to_stat(discord_tag, guild_id, stat_name, points_to_add):
    client, db = await get_db_connection()
    try:
        character_document = await db["characters"].find_one({
            "player.discord_tag": discord_tag,
            "player.guild_id": guild_id,
            "player.active": True
        })
        if character_document:
            # Convert the stat name to common names
            converted_stat_name = await convert_stat_name(stat_name.lower())
            logging.debug(f"Converted stat name: {converted_stat_name}")
            logging.debug (character_document["stats"])
            # Add points to the stat
            updated_stat_value = character_document["stats"][converted_stat_name] + points_to_add
            logging.debug(f"Current stat value: {updated_stat_value}")
            # Update the character's stats
            await db["characters"].update_one(
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
            logging.info(f"{points_to_add} points added to {converted_stat_name} for {discord_tag}")
            return f"{points_to_add} points added to {converted_stat_name} for {discord_tag}"
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