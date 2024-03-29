import logging
from utils.functions.database_functions import get_db_connection, close_db_connection

# Characters
#_______________________________________________________________________________________________________________________

# add character data to an object
async def create_character_insert(character_data, guild_id):
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
                "current_hp": 10,
                "str": 5,
                "def": 5,
                "spe": 5,
                "dex": 5,
                "cha": 5,
                "points_to_distribute": 0,
                "damage": 10,
                "defense": 10},
    "combat": { "status_ailment": None,
                "battle_status": False},
    "player": {"discord_tag": character_data["discord_tag"],
                   "guild_id": guild_id,
                   "active": False}}
    return character_insert
    
async def create_character(character_data):
    client, db = await get_db_connection()
    if db is None:
        logging.error("Connection to MongoDB failed.")
        return "Failed to connect to the database."
    try:
        # Insert the character data into the database
        await db['characters'].insert_one(character_data)
        return "Character successfully created!"
    except Exception as e:
        logging.exception(f"Error: {e}")
        return "An error occurred while attempting to create the character."
    finally:
        await close_db_connection(client)
        
# select active character name
async def active_character(discord_tag, guild_id):
    client, db = await get_db_connection()
    try:
        character_document = await db["characters"].find_one(
            {
                "player.discord_tag": discord_tag, 
                "player.guild_id": guild_id, 
                "player.active": True
            }
        )
        if character_document:
            character_name = character_document["character"]["characters_name"]  # Accessing nested field
            logging.debug(f"Active character found: {character_name}")
            return character_name, f"Your active character is: " + character_name + "."
        else:
            logging.debug("No active character found.")
            return None, f"No active character found for your profile"
    except Exception as e:
        logging.exception(f"Error fetching active character: {e}")
        return None, f"Failed to fetch active character"
    finally:
        await close_db_connection(client)

# Delete a character from the database
async def delete_character(character_data):
    client, db = await get_db_connection()
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
async def switch_active_character(character_data):
    client, db = await get_db_connection()
    try:
        #Validate that a character is active
        active_character_name, message = await active_character(character_data["discord_tag"], character_data["guild_id"])
        # If there is an active character, set it to inactive
        if active_character_name is not None:
            # Set the old character as inactive
            set_inactive = await db['characters'].update_one({"character.characters_name": active_character_name, 
                                                   "player.discord_tag": character_data["discord_tag"],
                                                   "player.guild_id": character_data["guild_id"]},
                                                  {"$set": {"player.active": False}})
            # Validate if the character was set to inactive
            if set_inactive.modified_count > 0:
                logging.info(f"Character {active_character_name} set to inactive.")            
                # Set the new character as active
                set_active = await db['characters'].update_one({"character.characters_name": character_data["characters_name"], 
                                            "player.discord_tag": character_data["discord_tag"],
                                            "player.guild_id": character_data["guild_id"]},
                                            {"$set": {"player.active": True}})
                if set_active.modified_count > 0:
                    logging.info(f"Character {character_data['characters_name']} set to active.")
                    return f"You are now using the character {character_data['characters_name']}!"
            else:
                logging.info(f"Failed to set {active_character_name} to inactive.")
                return f"Failed to set {active_character_name} to inactive."
        else:
            return f"No active character found, please reach out to a moderator or admin."
    except Exception as e:
        logging.exception(f"Error in switch_active_character: {e}")
        return f"An error occurred while attempting to switch your active character to {character_data['characters_name']}."
    finally:
        await close_db_connection(client)
        
# return all characters for a user
async def available_characters(discord_tag):
    client, db = await get_db_connection()
    try:
        # Await the to_list coroutine to get the actual list of characters
        characters = await db["characters"].find({"discord_tag": discord_tag}).to_list(length=None)
        return characters
    except Exception as e:
        logging.exception(f"Error fetching characters: {e}")
        return []
    finally:
        await close_db_connection(client)

