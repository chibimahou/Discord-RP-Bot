import discord
import sqlite3
import os
import re
import math as mat
import function_calls.calc as calc
from discord.ext import commands
from discord import app_commands
from discord.utils import get

#Sends a party invite request to character_name_b from character_name_a.
#Convert the character names to lowercase and check if each user exists in the charactersheets table.
#If users do not exist, return False, if they do, return true.
def request_party_invite(character_name_a, character_name_b):
    if(calc.validate_fields(character_name_a) == True and  calc.validate_fields(character_name_b) == True):
        character_a = calc.verify_player_exists(character_name_a)
        character_b = calc.verify_player_exists(character_name_b)
        if character_a == True and character_b == True:
                return('```' + character_name_a + ' has sent ' + character_name_b + ' a party invite.\n\n Use the command \'/accept_or_decline_party_invite to reply.\'```')   
        return('```One of the character nmames do not exist.```')

def accept_or_decline_party_invite(character_name_a, character_name_b, accept_or_decline):
    if(calc.validate_fields(character_name_a) == True and  calc.validate_fields(character_name_b) == True):
        character_a = calc.verify_player_exists(character_name_a)
        character_b = calc.verify_player_exists(character_name_b)
        if character_a == True and character_b == True:
                accept_or_decline_lower = accept_or_decline.lower()
                if accept_or_decline_lower != "accept" and accept_or_decline_lower != "decline":
                        return('``` Please input \'accept\' or \'decline\' in the accept_or_decline field.```')   
                else: 
                        if accept_or_decline_lower == "accept":
                                return('```' + character_name_b + ' has accepted your party invite.```')   
                        return('```' + character_name_b + ' has declined your party invite.```')
        return('``` One of the character names do not exist.```')

#Sends a party invite request to character_name_b from character_name_a.
#Convert the character names to lowercase and check if each user exists in the charactersheets table.
#If users do not exist, return False, if they do, return true.
def request_guild_invite(character_name_a, character_name_b, guild_name):
    if(calc.validate_fields(character_name_a) == True and  calc.validate_fields(character_name_b) == True):
        character_a = calc.verify_player_exists(character_name_a)
        character_b = calc.verify_player_exists(character_name_b)
        guild_a = calc.verify_guild_exists(guild_name)
        approver_a = calc.check_guild_approvers(character_name_a, guild_name)
        guild_name_lower = guild_name.lower()
        if character_a == True and character_b == True:
                if guild_a == True:
                        if approver_a == True:
                                return('```' + character_name_a + ' sent a guild invite to ' + character_name_b + '.```') 
                        else:
                                return('```' + character_name_a + ' is not an approver for the guild: ' + guild_name_lower + '```')
                return('```The guild name you input does not exist.```') 
        return('```One of the character names do not exist.```') 

def accept_or_decline_guild_invite(character_name_a, character_name_b, guild_name, accept_or_decline):
    if(calc.validate_fields(character_name_a) == True and  calc.validate_fields(character_name_b) == True):
        character_a = calc.verify_player_exists(character_name_a)
        character_b = calc.verify_player_exists(character_name_b)
        guild_a = calc.verify_guild_exists(guild_name)
        if character_a == True and character_b == True:
                if guild_a == True:
                       accept_or_decline_lower = accept_or_decline.lower()
                if accept_or_decline_lower != "accept" and accept_or_decline_lower != "decline":
                        return('``` Please input \'accept\' or \'decline\' in the accept_or_decline field.```')   
                else: 
                        if accept_or_decline_lower == "accept":
                                add_to_guild = calc.add_to_guild(character_name_b, guild_name)
                                if add_to_guild == True:
                                        return('```' + character_name_b + ' has accepted your guild invite.```')   
                                else:
                                        return('``` Something went wrong adding the user to the guild. ```')
                        return('```' + character_name_b + ' has declined your party invite.```')
        return('``` One of the character names do not exist.```')