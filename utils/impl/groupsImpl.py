import discord
import logging
from discord import app_commands
from datetime import datetime
from mysql.connector import Error
from utils.functions.character_functions import (get_active_character, get_character_by_name, 
                                                 update_characters_party)
from utils.functions.group_functions import (party_exists, create_party_document, send_invite, 
                                             invite_exists, get_party, handle_invite_response,
                                             leave_active_party, update_leader)
from utils.functions.database_functions import (get_db_connection, close_db_connection)
from utils.functions.utility_functions import (comment_wrap)

class PartyInviteView(discord.ui.View):
    def __init__(self, invitee: discord.Member, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.invitee = invitee
        
async def party_invite_logic(invite_data, interaction):
    # Get the database connection
    try:
        client, db = await get_db_connection()
    except Exception as e:
        logging.exception("Database connection failed: %s", e)
        return await comment_wrap("Database connection failed.")
    
    try:
        # Get the invitors data
        inviter_character_document = await get_active_character(db, invite_data)
        # Get the invitees data
        invitee_character_document = await get_character_by_name(db, invite_data)
        user_id = await interaction.guild.fetch_member(invitee_character_document['player']['discord_tag'])
        invitee: discord.Member = user_id
        logging.debug(f"Party Invite: Obtained Character Data")
        view = PartyInviteView(invitee=inviter_character_document['player']['discord_tag'])
        await interaction.response.defer()
        # Check if the invitor has an active character
        if not inviter_character_document:
            return await comment_wrap(f"You don't have an active character.")
        # Check if the invitor is trying to invite themselves
        elif invitee_character_document['player']['discord_tag'] == invite_data['discord_tag']:
            return await comment_wrap(f"You can't invite yourself to a party.")
        # Check if the invitee exists
        elif not invitee_character_document:
            return await comment_wrap(f"The player {invite_data['characters_name']} invite does not exist.")
        # Check if the invitee is already in a party
        elif invitee_character_document['group']['party_id'] is not None:
            return await comment_wrap(f"{invite_data['characters_name']} is already in a party.")
        # Check if the invitee has already been invited
        elif await invite_exists(db, inviter_character_document, invitee_character_document, "party"):
            return await comment_wrap(f"An invite already exists for this player. The invite will expire in") 
        invite_data["creation_date"] = datetime.now().strftime('%Y-%m-%d')
        # Insert invite data to the database
        invite = await send_invite(db, invite_data, inviter_character_document, invitee_character_document) 
        # If the invite was successfully added to the database
        if invite:
            await interaction.followup.send(f"{invitee.mention}, you've been invited to a party!", view=view, ephemeral=False)
            return await comment_wrap(f"invite sent to {invite_data['characters_name']}.")
        return await comment_wrap(f"Failed to send invite to {invite_data['characters_name']}.")
    
    except Exception as e:
        logging.exception(f"Party Invite: Error getting character data: {e}")
        return await comment_wrap("An unexpected error occurred.")
    
    finally:
        await close_db_connection(client)
    
async def create_party_logic(party_data):
    try:
        client, db = await get_db_connection()
    except Exception as e:
        logging.exception("Database connection failed: %s", e)
        return await comment_wrap("Database connection failed.")
    
    try:
        character_document = await get_active_character(db, party_data)
        logging.debug(f"Create Party: Obtained Character Data")
        if not character_document:
            return await comment_wrap("You don't have an active character.")
        if await party_exists(db, party_data, character_document):
            return await comment_wrap("You are already in a party.") 
        # Insert the party data into the database
        current_date = datetime.now()
        date_string = current_date.strftime('%Y-%m-%d')
        party_data["creation_date"] = date_string
        party_insert = await create_party_document(party_data, character_document) 
        update = await db["parties"].insert_one(party_insert)   
        if update:
            await update_characters_party(db, character_document, update.inserted_id) 
            return await comment_wrap("Party created successfully.")
        return await comment_wrap("Failed to add party.")
    except Exception as e:
        logging.exception(f"Create_Party: Error getting character data: {e}")
        return await comment_wrap("An unexpected error occurred.")
    finally:
        await close_db_connection(client)

# ______________________________________________________________________________________________________________________
# Accept a party invite
#   character document: The Invitee
#   second character document: The Inviter
# ______________________________________________________________________________________________________________________
async def accept_party_invite_logic(invite_data, interaction, invitee: discord.Member):
    try:
        client, db = await get_db_connection()
        
    except Exception as e:
        logging.exception("Database connection failed: %s", e)
        return await comment_wrap("Database connection failed.")
    
    try:
        invitee_character_document = await get_active_character(db, invite_data)
        inviter_character_document = await get_character_by_name(db, invite_data)
        party_document = await get_party(db, inviter_character_document['group']['party_id'])
        view = PartyInviteView(invitee=inviter_character_document['player']['discord_tag'])
        await interaction.response.defer()
        logging.debug(f"Accept Party Invite: Obtained Character Data")
        if not invitee_character_document:
            return await comment_wrap("You don't have an active character.")
        
        if not inviter_character_document:
            return await comment_wrap(f"The player {invite_data['characters_name']} invite does not exist.")
        
        if not await invite_exists(db, inviter_character_document, invitee_character_document, "party"):
            return await comment_wrap("No invite exists for this player.")
        
        if invitee_character_document['group']['party_id'] is not None:
            return await comment_wrap(f"{invitee_character_document['character']['characters_name']} is already in a party.")
        
        if party_document['party']['settings']['max_members'] == len(party_document['party']['members']):
            return await comment_wrap(f"Party is full.")
        
        # Insert the party data into the database
        update = await handle_invite_response(db, invitee_character_document, inviter_character_document, party_document, "accept")
        if update:
            await interaction.followup.send(f"{invitee.mention}, {invitee_character_document['character']['characters_name']} Has accepted your party invite!", view=view, ephemeral=False)
            return await comment_wrap(f"Party invite accepted.")
        
        return await comment_wrap(f"Failed to accept party invite.")
    except Exception as e:
        logging.exception(f"Accept Party Invite: Error getting character data: {e}")
        return await comment_wrap("An unexpected error occurred.")
    
    finally:
        await close_db_connection(client)
        
# ______________________________________________________________________________________________________________________
# Decline a party invite
#   character document: The Invitee
#   second character document: The Inviter
# ______________________________________________________________________________________________________________________
async def decline_party_invite_logic(invite_data, interaction, invitee: discord.Member):
    try:
        client, db = await get_db_connection()
        
    except Exception as e:
        logging.exception("Database connection failed: %s", e)
        return await comment_wrap("Database connection failed.")
    
    try:
        invitee_character_document = await get_active_character(db, invite_data)
        inviter_character_document = await get_character_by_name(db, invite_data)
        party_document = await get_party(db, invitee_character_document['group']['party_id'])
        view = PartyInviteView(invitee=invitee_character_document['player']['discord_tag'])
        await interaction.response.defer()
        logging.debug(f"Accept Party Invite: Obtained Character Data")
        if not invitee_character_document:
            return await comment_wrap("You don't have an active character.")
        
        if not inviter_character_document:
            return await comment_wrap(f"The player {invite_data['characters_name']} invite does not exist.")
        
        if not await invite_exists(db, invitee_character_document, inviter_character_document, "party"):
            return await comment_wrap("No invite exists for this player.")
        
        if invitee_character_document['group']['party_id'] is not None:
            return await comment_wrap(f"{invitee_character_document['character']['characters_name']} is already in a party.")
        
        if party_document['party']['settings']['max_members'] == len(party_document['party']['members']):
            return await comment_wrap(f"Party is full.")
        
        # Insert the party data into the database
        update = await handle_invite_response(db, invitee_character_document, inviter_character_document, party_document, "decline")
        if update:
            await interaction.followup.send(comment_wrap(f"{invitee.mention}, you've been invited to a party!"), view=view, ephemeral=False)
            return await comment_wrap(f"Party invite accepted.")
        
        return await comment_wrap(f"Failed to accept party invite.")
    except Exception as e:
        logging.exception(f"Accept Party Invite: Error getting character data: {e}")
        return await comment_wrap("An unexpected error occurred.")
    
    finally:
        await close_db_connection(client)
        
async def leave_party_logic(party_data, interaction):
    try:
        client, db = await get_db_connection()
        
    except Exception as e:
        logging.exception("Database connection failed: %s", e)
        return await comment_wrap("Database connection failed.")
    
    try:
        invitee_character_document = await get_active_character(db, party_data)
        party_document = await get_party(db, invitee_character_document['group']['party_id'])
        view = PartyInviteView(invitee=invitee_character_document['player']['discord_tag'])
        id = await interaction.guild.fetch_member(invitee_character_document['player']['discord_tag'])
        invitee: discord.Member = id
        await interaction.response.defer()
        if not invitee_character_document:
            return await comment_wrap("You don't have an active character.")
        
        elif not party_document:
            return await comment_wrap("You are not in a party.")
        
        # If user is the party leader
        if party_document['party']['leader'] == invitee_character_document['_id']:
            update_leader()
        update = await leave_active_party(db, invitee_character_document, party_document)
        if update:
            await interaction.followup.send(comment_wrap(f"{invitee.mention}, {invitee_character_document['character']['characters_name']} has left the party!"), view=view, ephemeral=False)
            return await comment_wrap(f"You have left the party.")
        
        return await comment_wrap(f"Failed to leave the party.")
    
    except Exception as e:
        logging.exception(f"Leave Party: Error getting character data: {e}")
        return await comment_wrap("An unexpected error occurred.")
    
    finally:
        await close_db_connection(client)
        
        