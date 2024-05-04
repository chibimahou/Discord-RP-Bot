from motor.motor_asyncio import AsyncIOMotorClient
import logging
from config.config import (DB_NAME, DB_USERNAME, DB_PASSWORD, DB_HOST, URI)
from utils.functions.database_functions import get_db_connection, close_db_connection
from utils.functions.character_functions import active_character

# Groups
#_______________________________________________________________________________________________________________________

# ______________________________________________________________________________________________________________________            
# Description: Create a database entry object for a party
# Return: Object
# ______________________________________________________________________________________________________________________   

async def create_party_document(party_data, character_document):
    party_insert = {
        "party": {
            "party_name": party_data["party_name"],
            "leader_id": character_document['_id'],  # Assuming interaction has a user attribute
            "members": [
                {
                    "user_id": character_document['_id'],  # Leader's user ID
                    "username": character_document['character']['characters_name'],  # Leader's usernameF
                    "role": "Leader"
                }
            ],
            "status": party_data.get("status", "Open"),  # Default status to Open if not provided
            "creation_date": party_data["creation_date"],
            "last_activity_date": party_data["creation_date"],  # Initial activity date is the creation date
            "settings": {
                "loot_distribution": party_data.get("loot_distribution", "Equal"),
                "experience_sharing": party_data.get("experience_sharing", True),
                "max_members": party_data.get("max_members", 5),
                "guild_id": party_data["guild_id"]
            }
        },
        "activities": {
            "completed": [],
            "in_progress": []
        },
        "chat": {
            "messages": []
        },
    }
    return party_insert

# ______________________________________________________________________________________________________________________            
# Description: Check if a party exists in the database
# Return: Boolean
# ______________________________________________________________________________________________________________________   

async def party_exists(db, party_data, character_document):
    logging.debug(f"Party Exists: Party data: {character_document['group']['party']} and {party_data['guild_id']}")
    party_document = await db["parties"].find_one({
        "_id": character_document['group']['party'],  # Assuming party_id is the character's ID
        "party.settings.guild_id": party_data['guild_id']
    })
    logging.debug(f"Party Exists: Party document: {party_document}")
    return bool(party_document)

# ______________________________________________________________________________________________________________________            
# Send an invite to a user to join a party
# Return: Boolean 
# ______________________________________________________________________________________________________________________   

async def send_invite(db, invite_data, inviter_character_document, invitee_character_document):
    party_insert = {
        "inviter_id": inviter_character_document['_id'],
        "invitee_id": invitee_character_document['_id'],
        "invite_type": invite_data["invite_type"],
        "guild_id": invite_data["guild_id"],
        "status": "Pending",
        "creation_date": invite_data["creation_date"]
    }
    
    update = await db["invites"].insert_one(party_insert)
    if update:   
        return True
    return False

# ______________________________________________________________________________________________________________________            
# Add user to the party if they accept. Remove invite from the database
# Return: Boolean 
# ______________________________________________________________________________________________________________________   

async def handle_invite_response(db, inviter_character_document, invitee_character_document, party_document, response):
    # If accepted, add the first character to the party
    if response == "accept":
        # Set player data to add to the party
        member_data = {
            "member": {
                "user_id": inviter_character_document['_id'],
                "username": inviter_character_document['character']['characters_name'],
                "role": "member"
            }
        }
        # Add new user to the party list
        party_document['party']['members'].append(member_data)
        # Commit the party change to the database
        update_result = await db['parties'].update_one(
            {"_id": party_document['_id']},
            {"$set": {'party.members': party_document['party']['members']}}
        )

        # Check if the database update was successful
        if update_result.modified_count == 1:
            # Remove invite from the database
            remove_invite = await remove_party_invite(db, inviter_character_document, invitee_character_document)
            return True
        else:
            return False
        
    elif response == "decline":
        remove_invite = await remove_party_invite(db, inviter_character_document, invitee_character_document)
        if remove_invite:
            return True
        
        else:
            return False
        
    return False

# ______________________________________________________________________________________________________________________            
# Leave the party and delete it if you are the last member
# Return: db 
# ______________________________________________________________________________________________________________________   

async def remove_party_invite(db, invitee_character_document, inviter_character_document):
    logging.debug(f"Remove Party Invite: {await db['invites'].find_one({'inviter_id': inviter_character_document['_id'],'invitee_id': invitee_character_document['_id'],'invite_type': 'party','guild_id': invitee_character_document['player']['guild_id']})}")
    return await db['invites'].delete_one({
        "inviter_id": inviter_character_document['_id'],
        "invitee_id": invitee_character_document['_id'],
        "invite_type": "party",
        "guild_id": invitee_character_document['player']['guild_id']
    })
    
# ______________________________________________________________________________________________________________________            
# Leave the party and delete it if you are the last member
# Return: db
# ______________________________________________________________________________________________________________________   

async def leave_active_party(db, character_document):
    # If you are the only member of the party, delete the party
    if len(character_document['group']['party']['members']) == 1:
        return await db['parties'].delete_one({"_id": character_document['group']['party_id']})
    # If party was successfully deleted, remove the party from the character

    return await db['parties'].update_one(
        {"_id": character_document['group']['party_id']},
        {"$pull": {"party.members": {"user_id": character_document['_id']}}}
    )

# ______________________________________________________________________________________________________________________            
# Leave the party and delete it if you are the last member
# Return: db
# ______________________________________________________________________________________________________________________   
    
async def get_party(db, party_id):
    return await db["parties"].find_one({
        "_id": party_id
    })
    
# ______________________________________________________________________________________________________________________            
# Update the party leader to a random new party member
# Return: db
# ______________________________________________________________________________________________________________________   

async def update_leader(db, party_document):
    # Set the new leader to the second member in the party list and set the old leader to member
    party_document['party']['members'][0]['role'] = "member"
    party_document['party']['members'][1]['role'] = "leader"
    # Commit the party change to the database
    return await db['parties'].update_one(
        {"_id": party_document['_id']},
        {"$set": {'party.members': party_document['party']['members']}}
    )