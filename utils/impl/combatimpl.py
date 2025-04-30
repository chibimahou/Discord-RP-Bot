import discord
import logging
from discord import app_commands
from datetime import datetime
from mysql.connector import Error
from utils.functions.character_functions import (get_active_character, get_character_by_name, 
                                                 update_characters_party, check_if_parties_busy, 
                                                 )
from utils.functions.group_functions import (party_exists, create_party_document, send_invite, 
                                             invite_exists, get_party, handle_invite_response,
                                             leave_active_party, update_leader, get_party_members)
from utils.functions.combat_functions import (is_players_turn)
from utils.functions.mob_functions import (generate_mobs)

from utils.functions.database_functions import (get_db_connection, close_db_connection)
from utils.functions.utility_functions import (comment_wrap)

class PartyInviteView(discord.ui.View):
    def __init__(self, invitee: discord.Member, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.invitee = invitee
        
async def begin_combat_logic(combat_data):
    try:
        client, db = await get_db_connection()
    except Exception as e:
        logging.exception("Database connection failed: %s", e)
        return await comment_wrap("There seems to be a problem. Please reach out to an administrator.")
    character_document = get_active_character(combat_data)
    if not character_document:
        return "You do not have an active character."
    else:
        doing_something = await check_if_parties_busy(db, character_document)
        if doing_something:
            return "You or your party members are currently busy."
        else:
            combat_initiative = []
            in_party = await party_exists(db, character_document)
            if in_party:
                party_members = await get_party_members(db, character_document)
                for member in party_members:
                    member_data = {"discord_tag": member["member_id"],
                                      "guild_id": combat_data["guild_id"]}
                    member_document = await get_active_character(member_data)
                combat_initiative.append({"player_id": member_document["player"]["discord_tag"],
                                           "initiative": member_document["combat"]["initiative"]})
            else: 
                combat_initiative.append({"player_id": character_document["player"]["discord_tag"],
                                           "initiative": character_document["combat"]["initiative"]})
            mob_data = await generate_mobs(db, combat_data)
        
async def attack_logic(player_character_data):
    # Check if it is this players turn
    player_character_document = get_active_character(player_character_data)
    players_turn = is_players_turn(db, player_character_document)
    if not players_turn:
        return "It is not your turn."
    if not player_character_document:
        return "You do not have an active character."
