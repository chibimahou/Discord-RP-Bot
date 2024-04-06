import discord
import logging
from discord import app_commands
from mysql.connector import Error
from utils.functions.character_functions import active_character
from utils.functions.group_functions import party_exists
from cogs.utility import (validate_alphanumeric, validate_height, validate_age, 
                     validate_date, validate_text, validate_level, get_db_connection,
                     close_db_connection, active_character, get_party_or_guild_id, is_user_in_a_party, 
                     is_user_invited, insert_invitation_into_db, is_party_leader, select_new_leader, remove_user_from_party)

async def party_invite_logic(invite_data, interaction):
    
    return ()

async def create_party_logic(party_data, interaction):
    character_data, message = await active_character(party_data["discord_tag"], party_data["guild_id"])
    logging.info(f"Character data: {character_data}")
    return "You are already in a party."

