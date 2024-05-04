import discord
import logging
from discord import app_commands
from utils.impl.groupsImpl import (party_invite_logic, accept_party_invite_logic, decline_party_invite_logic)
from cogs.utility import (validate_alphanumeric, validate_height, validate_age, 
                     validate_date, validate_text, validate_level, get_db_connection,
                     close_db_connection, active_character)
from utils.functions.character_functions import (get_character_by_name, get_active_character)
from utils.functions.utility_functions import comment_wrap
from utils.functions.invite_functions import invite_exists
from datetime import datetime

class tradeInviteView(discord.ui.View):
    def __init__(self, invitee: discord.Member, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.invitee = invitee
        
# ______________________________________________________________________________________________________________________
# send party invite
# ______________________________________________________________________________________________________________________
async def send_trade_invite_logic (invite_data, interaction):
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
        view = tradeInviteView(invitee=inviter_character_document['player']['discord_tag'])
        await interaction.response.defer()
        # Check if the invitor has an active character
        if not inviter_character_document:
            return await comment_wrap(f"You don't have an active character.")
        # Check if the invitor is trying to invite themselves
        elif invitee_character_document['player']['discord_tag'] == invite_data['discord_tag']:
            return await comment_wrap(f"You can't invite yourself for a trade!")
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
# ______________________________________________________________________________________________________________________ 
# Accept trade invite
# ______________________________________________________________________________________________________________________
async def accept_trade_invite_logic(character_data, interaction, user_id):
    results = await accept_party_invite_logic(character_data, interaction, user_id)
    return results

# ______________________________________________________________________________________________________________________
# Decline trade invite
# ______________________________________________________________________________________________________________________
async def decline_trade_invite_logic(character_data, interaction, user_id):
    results = await decline_party_invite_logic(character_data, interaction, user_id)
    return results
