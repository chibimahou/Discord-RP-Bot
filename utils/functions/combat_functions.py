import datetime
from motor.motor_asyncio import AsyncIOMotorClient
import logging
from config.config import (DB_NAME, DB_USERNAME, DB_PASSWORD, DB_HOST, URI)
from utils.functions.database_functions import (get_db_connection, close_db_connection)
from utils.functions.character_functions import (active_character, get_character_by_name)

# Groups
#_______________________________________________________________________________________________________________________

# ______________________________________________________________________________________________________________________            
# Description: Create a database entry object for a party
# Return: Object
# ______________________________________________________________________________________________________________________   

async def create_combat_document(initiative_order, character_document, target_document, party_document):
    target_value = 1
    combat_insert = {
            "metadata": {
                "created_by": character_document['character']['characters_name'],
                "created_at": datetime.datetime.now(),
                "finished_at": None,
                "status": "Active"},
            "initiative_order": initiative_order,
            "round": 1,
            "turn": 1,
            "team_1": [],
            "team_2": []
        }
    # Conditionally add the "party" field based on party_document's existence and add party members to the combat_insert
    if party_document:
        combat_insert['party'] = party_document['_id']
        # Add all party members to the combat_insert
        for member in party_document['party']['members']:
            combat_insert['players'].append({
                "player_id": member['username'],
                "health": member['combat']['current_hp'],
                "target_value": target_value,
                "actions": [
                    {
                        "name": None,
                        "skill": None,
                        "target": None,
                        "hits": [],
                    }],
                "team": 1
            })
            target_value += 1
    else:
        # If player is not in a party, add them to the player section and add them to team 1
        combat_insert['team_1'].append({
            "player_id": character_document['_id'],
            "health": character_document['combat']['current_hp'],
            "target_value": target_value,
            "actions": [
                {
                    "name": None,
                    "skill": None,
                    "target": None,
                    "hits": [],
                }],
            "team": 1
        })
        target_value += 1

    # Add the target or mobs to the document with team: 2
    if target_document:
        for target in target_document:
            combat_insert['team_2'].append({
                "_id": target['_id'],
                "health": target['combat']['current_hp'],
                "target_value": target_value,
                "actions": [
                    {
                        "name": None,
                        "skill": None,
                        "target": None,
                        "hits": [],
                    }],
                "team": 2
            })
            target_value += 1

    return combat_insert
# ______________________________________________________________________________________________________________________            
# Description: Add all combat participants to the initiative order and sort them by initiative
# Return: array of objects, initiative_order
# ______________________________________________________________________________________________________________________   

async def get_initiative_order(db, character_document, party_document=None, mob_spawn_data=None, target_document=None, party_combat=False):
    initiative_order = []

    # 1. Add player to the initiative order
    initiative_order.append({
        "_id": character_document['_id'],
        "initiative": character_document['combat']['initiative'],
        "team": character_document.get('team', 'player')  # Default team 'player' if not specified
    })

    # 2. If party_combat is true, add the party to initiative order
    if party_combat:
        if party_document is not None:
            for member in party_document['party']['members']:
                member_data = await get_character_by_name(db, member['username'])
                initiative_order.append({
                    "_id": member_data[character_document['_id']],
                    "initiative": member_data['combat']['initiative'],
                    "team": member_data.get('team', 'player')  # Same default or retrieve from data
                })
        else:
            # 2b. If no party is present, return False
            return False

    # 3. If mob_spawn_data is not none, add mobs to the initiative order
    if mob_spawn_data is not None:
        for mob in mob_spawn_data:
            initiative_order.append({
                "_id": mob['_id'],
                "initiative": mob['combat']['initiative'],
                "team": 'mob'
            })

    # 4. if target_document is not none, add the target to the initiative order
    for target in target_document:
        if target is not None:
            initiative_order.append({
                "_id": target['_id'],
                "initiative": target['combat']['initiative'],
                "team": 'target'
            })
            
    # 5. If mob spawn data and target_document did not return anything, return false
    if not initiative_order:
        return False

    # Sort the initiative order by initiative descending (higher goes first)
    initiative_order = sorted(initiative_order, key=lambda x: x['initiative'], reverse=True)

    return initiative_order

# ______________________________________________________________________________________________________________________
# Description: Create a combat instance in the database
# Return: Object
# ______________________________________________________________________________________________________________________
async def create_combat_instance(db, combat_document):
    combat_collection = db['combat']
    combat_insert = await combat_collection.insert_one(combat_document)
    # If the combat_insert is successful, return true
    if combat_insert:
        return True
    # Insert failed, return false
    return False

# ______________________________________________________________________________________________________________________
# Description: Get the combat instance from the database
# Return: Object
# ______________________________________________________________________________________________________________________
async def get_combat_instance(db, character_document):
    combat_collection = await db['combat'].find_one({"_id": character_document['combat']['combat_id']})
    return combat_collection

# ______________________________________________________________________________________________________________________
# Description: find the command and execute it
# Return: Object
# ______________________________________________________________________________________________________________________
async def execute_action(db, character_data, character_document, combat_document, action_document):
    # Get the action from the character_data
    action = character_data['action']
    # Get the target of the action
    target = character_data['target']
    # Get the target document from the combat_document
    target_document = await get_target_document(db, target)
    # Get the combat instance document
    combat_instance = combat_document
    # Get the player's turn from the combat_instance
    player_turn = combat_instance['initiative_order'][0]
    if not target_valid:
        return await comment_wrap("Invalid target.")
    # Execute the action
    action_result = await execute_action_logic(action, action_document, target_document)
    # Check if the action was successful
    if action_result:
        # Remove the player from the initiative order
        await remove_from_initiative_order(db, combat_instance, character_document)
        # Add the player back to the initiative order
        await add_to_initiative_order(db, combat_instance, character_document)
        # Update the combat instance
        await update_combat_instance(db, combat_instance)
        return await comment_wrap(f"{action} successful.")
    # If the action failed, return a failure message
    return await comment_wrap(f"{action} failed.")

# ______________________________________________________________________________________________________________________
# Description: Find the action in the combat document
# Return: Object
# ______________________________________________________________________________________________________________________
async def find_action(action):
    if action is None:
        return False
    elif action == "attack":
        return True
    elif action == "vorpalstrike":
        return True
    elif action == "flee":
        return True
    
# ______________________________________________________________________________________________________________________
# Description: Calculate damage dealt by taking the attacker's damage and subtracting the target's defense
# Return: Object
# ______________________________________________________________________________________________________________________
async def calculate_damage(db, combat_document, target, modifier=1):
    # Get the attacker's damage times their skill modifier
    attacker_damage = (combat_document['players'][0]['combat_stats']['base_damage']) * modifier
    # Get the target's defense
    target_defense = combat_document['players'][target]['combat_stats']['base_defense']
    # Calculate the damage dealt
    damage_dealt = attacker_damage - target_defense
    return damage_dealt
    