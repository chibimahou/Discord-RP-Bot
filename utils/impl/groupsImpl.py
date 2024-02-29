import discord
from discord import app_commands
from mysql.connector import Error

from cogs.utility import (validate_alphanumeric, validate_height, validate_age, 
                     validate_date, validate_text, validate_level, get_db_connection,
                     close_db_connection, active_character, get_party_or_guild_id, is_user_in_a_party, 
                     is_user_invited, insert_invitation_into_db, is_party_leader, select_new_leader, remove_user_from_party)

def invite_logic(invite_data, interaction):
    validators = {
        "invitee": validate_text,
    }
    current_character = active_character(invite_data["discord_tag"])
    # Get the guild_id from the interaction
    guild_id = interaction.guild.id
    
    # Your own logic to determine the party to which the user is being invited
    # For instance, it could be the party of the user issuing the invite
    party_id = get_party_or_guild_id(current_character, "party_")
    
    # Check if the user is already in the party or already invited
    if is_user_in_a_party(party_id, guild_id) or is_user_invited(current_character, invite_data["invitee"], guild_id):
        return interaction.response.send_message(f"{invite_data['invitee']} is already in the party or has pending invites!")
        
    
    # Insert the invitation into the database
    # You need to implement this function according to your database setup
    insert_invitation_into_db(guild_id, party_id, validators["invitee"])
    
    # Inform the inviter and the invited user
    interaction.response.send_message(f"Invitation sent to {validators['invitee']}!")
    return interaction.response.send_message(f"Party request for {current_character}'s party was sent to {invite_data['invitee']}!")

def leave_party_logic(leave_data, interaction):
    validators = {
        "leaver": validate_text,
    }
    current_character = active_character(leave_data["discord_tag"])
    
    # Get the guild_id from the interaction
    guild_id = interaction.guild.id
    
    # Your own logic to determine the party the user is leaving
    party_id = get_party_or_guild_id(current_character, "party_")
    
    # Check if the user is in a party
    if not is_user_in_a_party(party_id, guild_id):
        return interaction.response.send_message(f"{leave_data['leaver']} is not in any party!")
    
    # Your own logic to determine if the leaver is the party leader
    if is_party_leader(current_character, guild_id):
        # Logic to select a new leader (could be random, highest level, longest membership, etc.)
        select_new_leader(party_id, guild_id)
    
    # Logic to remove the user from the party
    remove_user_from_party(current_character, party_id, guild_id)
    
    return interaction.response.send_message(f"{leave_data['leaver']} has left the party!")
