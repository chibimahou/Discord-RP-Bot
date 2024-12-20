import logging
from discord import app_commands

from utils.functions.character_functions import (
                    active_character, available_characters, create_character_insert, create_character, 
                    delete_character, switch_active_character, add_points_to_stat, level_up,
                    check_character_exists, get_character_by_name, convert_stat_name, 
                    update_combat_stats, get_character_by_id)
from utils.functions.database_functions import (
                    get_db_connection, close_db_connection, create_copy)
from utils.functions.inventory_functions import (get_equipment)
from utils.functions.validation_functions import (validate_alphanumeric, validate_height, validate_age, 
                    validate_text, validate_level, validate_date)
from utils.functions.group_functions import (get_party)
from utils.functions.combat_functions import (get_initiative_order, calculate_damage, create_combat_document, create_combat_instance, get_combat_instance, find_action, execute_action)
from utils.functions.utility_functions import comment_wrap

# ______________________________________________________________________________________________________________________
# Function: Add combat record into the database
# ______________________________________________________________________________________________________________________
async def start_combat_logic(character_data, target_data=None, mob_data=None, party_data=None):
    try:
        client, db = await get_db_connection()
    except Exception as e:
        logging.exception("Database connection failed: %s", e)
        return await comment_wrap("Database connection failed.")
    
    try:
        # Get the characters document
        character_document = await active_character(db, character_data)
        # Check if the character exists 
        if not character_document:
            return await comment_wrap("Character not found.")
        # Check if character is in combat
        if character_document['instance']['instance_id'] is None:
            return await comment_wrap("Character is doing something else. Please finish your task first.")
        if target_data:
            target_documents = []
            if target_data['type'] == 'mob':
                # target_document = await get_mob_by_name(db, target_data)
                # if not target_document:
                    return await comment_wrap("Mob not found.")
            elif target_data['type'] == 'character':
                target_documents.append(await get_character_by_name(db, target_data))
                if not target_documents:
                    return await comment_wrap("Target not found.")
        else:
            return await comment_wrap("No opponent found. Please make sure you have designated an opponent.")
        # Check if the character is in a party
        if party_data:
            party_document = await get_party(db, character_document['group']['party'])    
            if not party_document:
                return await comment_wrap("Party not found.")
        else: 
            party_document = None
#        elif mob_data:
 #           mob_document = await get_mob_by_name(db, mob_data)
  #          if not mob_document:
   #             return await comment_wrap("Mob not found.")
        # Else, return failure message, need opponent to start combat
        # Set the initiative order
        initiative_order = await get_initiative_order(db, character_document, party_document, mob_data, target_documents, False)
        # TODO: Get the if mobs and add them to the initiative order if mob combat is active
        # Start of combat logic
        
        # Create combat instance document
        combat_document = await create_combat_document(initiative_order, character_document, target_documents, party_document)
        logging.debug("Combat document: %s", combat_document)
        # Insert the combat document into the database
        combat_insert = await create_combat_instance(db, combat_document)
        # if successful. return success message
        if combat_insert:
            return await comment_wrap("Combat has started.")
        # if failed, return failure message
        return await comment_wrap("Combat failed to start.")
    except Exception as e:
        logging.exception("Error starting combat: %s", e)
        return await comment_wrap("Error starting combat.")
    finally:
        await close_db_connection(client)
    
# ______________________________________________________________________________________________________________________
# Function: Perform combat actions
# ______________________________________________________________________________________________________________________    
async def action_logic(interaction, character_data, target):
    try:
        client, db = await get_db_connection()
    except Exception as e:
        logging.exception("Database connection failed: %s", e)
        return await comment_wrap("Database connection failed.")
    
    try:
        # Check if inputs are valid
        if not character_data or not isinstance(character_data, dict):
            logging.error("Invalid character data.")
            return await comment_wrap("Invalid character data.")
        if target is None or not isinstance(target, int):
            logging.error("Invalid target.")
            return await comment_wrap("Invalid target.")

        # Get character information from the database
        character_document = await active_character(db, character_data)
        if not character_document:
            logging.error("Character not found.")
            return await comment_wrap("Character not found.")
        
        # Get the combat instance
        combat_document = await get_combat_instance(db, character_document)
        if not combat_document:
            logging.error("Combat instance not found.")
            return await comment_wrap("Combat instance not found.")
        
        # Validate the target index
        if target >= len(combat_document['players']):
            logging.error("Invalid target.")
            return await comment_wrap("Invalid target.")
        
        target_id = combat_document['players'][target]['_id']
        
        # Get the target document
        target_document = await get_character_by_id(db, character_data, target_id)
        if not target_document:
            logging.error("Target not found.")
            return await comment_wrap("Target not found.")
        
        # Calculate damage
        damage = await calculate_damage(db, combat_document, target)
        return await comment_wrap(f"Damage dealt: {damage}")

    except Exception as e:
        logging.exception("Error in combat logic: %s", e)