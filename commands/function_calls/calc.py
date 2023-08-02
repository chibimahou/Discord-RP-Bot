import discord
import sqlite3
import array
import random
import re
import math
import hashlib
import pytz
from datetime import datetime, timedelta
import function_calls.inventory as inv
import function_calls.skills as ski
import function_calls.experience as exp
import function_calls.col as col
import function_calls.stats as sta
import function_calls.calc as mat
import function_calls.trade as tra
import function_calls.help as help
import function_calls.query.query as que
from discord.ext import commands
from discord import app_commands
from discord.utils import get

#Seperates a string to an array by ','.
#Returns seperated array, array[0] = fishing, array[1] = blacksmithing.
def seperate_string_to_array(string_to_seperate):
        new_string = str(string_to_seperate).split(",")
        return new_string

def concatenate_string(string_array, string_to_add_or_remove, add_or_remove):
        concat_string = ""
        count = 0
        if add_or_remove.lower() == "add":
                while(string_array):
                        if count == 0:
                                concat_string = string_array.pop(0)
                                count = 1
                        else:
                               print(string_array)
                               concat_string = concat_string + ", " + string_array.pop(0)
                concat_string = concat_string + ", " + string_to_add_or_remove
                return concat_string
        elif add_or_remove.lower() == "remove":
                while(string_array):
                        if count == 0:
                                string_value = string_array.pop(0)
                                if string_value != string_to_add_or_remove:
                                        concat_string = string_value
                                        count = 1
                        else:                    
                                string_value = string_array.pop(0)
                                if string_value != string_to_add_or_remove:
                                        concat_string = concat_string + ", " + string_to_add_or_remove    
                return concat_string
        else:
                return 1
#Removes white spaces around commas, I.E. (fishing, blacksmiting) to (fishing,blacksmithing).
#And seperates string to array by commas, I.E. (fishing,blacksmithing) to array[0] = fishing, array[1] = blacksmithing.
#Dependencies, seperate_string_to_array
#Returns seperated array, array[0] = fishing, array[1] = blacksmithing.
def remove_white_spaces_around_commas(string_to_remove_white_spaces):
        string_with_no_white_spaces = string_to_remove_white_spaces.replace(" ,", ",")
        string_with_no_white_spaces = string_to_remove_white_spaces.replace(", ", ",") 
        string_with_no_white_spaces_array = seperate_string_to_array(string_with_no_white_spaces)
        return string_with_no_white_spaces_array

#Get the players stats.
#Returns stats array (str, def, spd, dex, cha).
def get_player_stats(character_name):
        character_name_lower = character_name.lower()
        sqliteConnection = sqlite3.connect('characterSheet.db')
        cursor = sqliteConnection.cursor()
        query = que.get_players_stats_characters()
        character_information = cursor.execute(query, (character_name_lower,)).fetchone()
        stats = [character_information[0], character_information[1], character_information[2], character_information[3], character_information[4]]
        str(character_information).format()
        cursor.close()
        sqliteConnection.close()
        return stats

#Add player to guild.
#Returns boolean True if successful or False if unsuccessful.
def add_to_guild(character_name, guild_name):
        character_name_lower = character_name.lower()       
        guild_name_lower = guild_name.lower()
        sqliteConnection = sqlite3.connect('characterSheet.db')
        cursor = sqliteConnection.cursor()
        query = que.add_to_guild_characters()
        cursor.execute(query, (guild_name_lower, character_name_lower)).fetchone()
        sqliteConnection.commit()
        cursor.close()
        sqliteConnection.close()
        return True

#Verify player is in the server.
#Returns True if successful or False if unsuccessful.
def verify_player_exists(character_name):
        character_name_lower = character_name.lower()
        sqliteConnection = sqlite3.connect('characterSheet.db')
        cursor = sqliteConnection.cursor()
        query = que.get_player_characters()
        character_in_table = cursor.execute(query, (character_name_lower,)).fetchall()
        print(character_in_table)
        if character_in_table:
                print("Success")
                return(True)
        sqliteConnection.commit()
        cursor.close()
        print("Failure")  
        return(False)

#Verify if the guild is registered in the server.
#Returns True if successful or False if unsuccessful.
def verify_guild_exists(guild_name):
        guild_name_lower = guild_name.lower()
        sqliteConnection = sqlite3.connect('characterSheet.db')
        cursor = sqliteConnection.cursor()
        query = que.get_guild_characters()
        character_in_table = cursor.execute(query, (guild_name_lower,)).fetchone()
        if len(character_in_table) < 1:
                return(False)
        return(True)

#Get the approvers for a guild.
#Returns True if successful or False if unsuccessful.
def check_guild_approvers(approver_name, guild_name):
        approver_name_lower = approver_name.lower()
        guild_name_lower = guild_name.lower()
        sqliteConnection = sqlite3.connect('characterSheet.db')
        cursor = sqliteConnection.cursor()
        query = que.get_guild_approvers_characters()
        character_in_table = cursor.execute(query, (guild_name_lower,)).fetchone()
        approver_array = remove_white_spaces_around_commas(character_in_table[0][0])

        temp = 0
        for temp in range(len(approver_array)):
                if approver_array[temp] == approver_name_lower:
                        return(True)
        return(False)

#Checks what the success rate for a status ailment is.
#Returns random value from 0 - 100.     
def check_for_bleed():
        bleed_success = random.randint(0,100)
        return(bleed_success)

#Gets a players character information.
#Returns the players character information in an array.
def get_character_information(character_name):
        character_name_lower = character_name.lower()
        sqliteConnection = sqlite3.connect('characterSheet.db')
        cursor = sqliteConnection.cursor()
        query = que.get_all_player_fields_characters()
        character_information = cursor.execute(query, (character_name_lower,)).fetchone()
        return(character_information)

#Verifies that an item exists in the item database.
#Returns True if successful or False if unsuccessful.
def item_exists(item_name):
        item_name_lower = item_name.lower()
        sqliteConnection = sqlite3.connect('equipment.db')
        cursor = sqliteConnection.cursor()
        character_information = cursor.execute("SELECT item FROM items WHERE item = '" + item_name_lower + "'").fetchall()
        if len(character_information) != 1:
                return(False)
        else:
                return(True)

#Verifies that a weapon exixsts in the weapon database.
#Returns True if successful or False if unsuccessful.
def weapon_exists(weapon_name):
        weapon_name_lower = weapon_name.lower()
        sqliteConnection = sqlite3.connect('equipment.db')
        cursor = sqliteConnection.cursor()
        character_information = cursor.execute("SELECT weapon_name FROM weapons WHERE weapon_name = '" + weapon_name_lower + "'").fetchall()
        if len(character_information) != 1:
                return(False)
        else:
                return(True)

#Verifies that an armor exists in the armor database.
#Returns True if successful or False if unsuccessful.
def armor_exists(armor_name):
        armor_name_lower = armor_name.lower()
        sqliteConnection = sqlite3.connect('equipment.db')
        cursor = sqliteConnection.cursor()
        character_information = cursor.execute("SELECT armor_name FROM armor WHERE armor_name = '" + armor_name_lower + "'").fetchall()
        if len(character_information) != 1:
                return(False)
        else:
                return(True)


#Obtains the mobs stats based on the level differences.
#Returns an array of the mobs stats, Array(hp, str, def, dex, spe, xp)
def calc_mob_stats(base_level, base_hp, base_str, base_dex, base_spe, base_def, base_xp, max_hp, max_str, max_dex, max_spe, max_def, max_xp, max_level):
        total_increments = 5
        i = max_level - base_level
        values = []
        value = ((5 * (i)) / (total_increments)) / 5        
        mobs_hp = value * (max_hp - base_hp)
        values.append(mobs_hp)
        mobs_str = value * (max_str - base_str)
        values.append(mobs_str)
        mobs_def = value * (max_def - base_def)
        values.append(mobs_def)
        mobs_dex = value * (max_dex - base_dex)
        values.append(mobs_dex)
        mobs_spe = value * (max_spe - base_spe)
        values.append(mobs_spe)
        mobs_xp = value * (max_xp - base_xp)
        values.append(mobs_xp)
        print(values)
        return values

#Gets the proficiency skill and its level for a player.
#Returns an array of the proficiency skill and their level, array(skill_name, skill_level).
def get_proficiency(proficiency_skills, find_skill):
        for part in proficiency_skills:
                print(part + " = " + find_skill)
                result = str(part).split(':')
                if find_skill == result[0]:
                        print(result[0] + " " + result[1])
                        return result
        else:
                return False

#Verifies an account is linked to a discord account.
#Returns True if successful or False if unsuccessful.
def verify_account(character_name, discord_tag):
        sqliteConnection = sqlite3.connect('characterSheet.db')
        character_name_lower = character_name.lower()
        cursor = sqliteConnection.cursor()
        character_information = cursor.execute("SELECT discord_tag, nickname FROM charactersheets WHERE discord_tag = '" + str(discord_tag) + "'").fetchall()
        character_information_length = len(character_information)
        temp = 0
        for temp in range(character_information_length):
                if character_information[temp][0] != str(discord_tag) and character_name_lower != character_information[temp][1]:
                     temp2 = 0   
                if character_information[temp][0] != str(discord_tag) and character_name_lower == character_information[temp][1]:
                     return(False)
                if character_information[temp][0] == str(discord_tag) and character_name_lower != character_information[temp][1]:
                     temp2 = 0
                else:
                     cursor.close()
                     sqliteConnection.close()
                     return (True)
        cursor.close()
        sqliteConnection.close()
        return(False)

def skill_damage_calculation(offense_a, weapon_value_a, skill_a, graze_reduction, buffs_a, defense_b, armor_value_b, skill_reduction_b, buffs_b, crit_modifier):
        total_damage_reduction = math.ceil(float(defense_b) + float(armor_value_b) + float(skill_reduction_b) + float(buffs_b))
        total_damage = math.ceil(float(offense_a) + float(skill_a) + float(weapon_value_a) + float(buffs_a))
        damage_dealt = (total_damage - total_damage_reduction) * float(crit_modifier)
        total_reduction = math.ceil(((100 - graze_reduction) / 100) * damage_dealt)
        graze_damage_reduction = math.ceil(total_reduction)
        return(graze_damage_reduction)

def slash_damage_calculation(offense_a, weapon_value_a, graze_reduction, buffs_a, defense_b, armor_value_b, buffs_b, crit_modifier):
        total_damage_reduction = math.ceil(float(defense_b) + float(armor_value_b) + float(buffs_b))
        total_damage = math.ceil(float(offense_a) + float(weapon_value_a) + float(buffs_a))
        damage_dealt = (total_damage - total_damage_reduction) * float(crit_modifier)
        total_reduction = math.ceil(((100 - graze_reduction) / 100) * damage_dealt)
        graze_damage_reduction = math.ceil(total_reduction)
        return(graze_damage_reduction)

def beasts_slash_damage_calculation(offense_a, weapon_value_a, graze_reduction, material_modifier_a, defense_b, armor_value_b, material_modifier_b, crit_modifier):
        if int(defense_b) <= 10:
                defense_modifier = 1.0
                total_damage_reduction = math.ceil(float(defense_modifier) * float(armor_value_b) * float(material_modifier_b))
        else:
                defense_modifier = int(defense_b)/10
                if material_modifier_b + .5 < defense_modifier:
                        defense_modifier = material_modifier_b + .5
                elif material_modifier_b + .5 < defense_modifier:
                        defense_modifier = material_modifier_b + .5
                elif material_modifier_b + .5 >= defense_modifier:
                        defense_modifier = defense_modifier
                else:
                        defense_modifier = defense_modifier
                total_damage_reduction = math.ceil(float(defense_modifier) * float(armor_value_b) * float(material_modifier_b))
        if int(offense_a) <= 10:
                offense_modifier = 1.0
                total_damage = math.ceil(float(offense_modifier) * float(weapon_value_a) * float(material_modifier_a))
        else:
                offense_modifier = int(offense_a)/10
                if material_modifier_a + .5 < offense_modifier:
                        offense_modifier = material_modifier_a + .5
                elif material_modifier_a + .5 < offense_modifier:
                        offense_modifier = material_modifier_a + .5
                elif material_modifier_a + .5 >= offense_modifier:
                        offense_modifier = offense_modifier
                else:
                        offense_modifier = offense_modifier
 
                total_damage = math.ceil(float(offense_modifier) * float(weapon_value_a) * float(material_modifier_a))

        damage_dealt = (total_damage - total_damage_reduction) * float(crit_modifier)
        total_reduction = math.ceil(((100 - graze_reduction) / 100) * damage_dealt)
        graze_damage_reduction = math.ceil(total_reduction)
        return(graze_damage_reduction)

def check_material(material):
        material_lower = material.lower()
        if material_lower == 'bronze':
                return 1.0
        elif material_lower == 'iron':
                return 1.5
        elif material_lower == 'steel':
                return 2.0               
        elif material_lower == 'black steel':
                return 2.5               
        elif material_lower == 'carbon':
                return 3.0               
        elif material_lower == 'titanium':
                return 3.5               
        elif material_lower == 'silver':
                return 4.0               
        elif material_lower == 'tungsten':
                return 4.5              
        else:
                return('invalid')

def validate_fields(field_to_validate):
    return bool(re.search(r'^[a-zA-Z0-9 ]+$', field_to_validate))        

def validate_fields_commas(field_to_validate):
    return bool(re.search(r'^[a-zA-Z0-9.,!?/\'\" ]+$', field_to_validate))        

def is_allowed(member, allowed_roles):
    temp = 0
    while temp in range(len(member)):
        temp2 = 0
        while temp2 in range(len(allowed_roles)):
                if str(member[temp]).lower() in str(allowed_roles[temp2]).lower():
                    return True
                temp2 = temp2 + 1
        temp = temp + 1

def generate_key(strings):
    concatenated_string = ''.join(strings)
    hashed_key = hashlib.sha256(concatenated_string.encode()).hexdigest()
    return hashed_key
    return False

def create_invite_id(strings):
    concatenated_string = strings
    hashed_key = hashlib.sha256(concatenated_string.encode()).hexdigest()
    return hashed_key
    return False

def get_current_datetime():
        # Define the EST timezone
        est_tz = pytz.timezone('US/Eastern')

        # Get the current UTC time
        utc_now = datetime.utcnow()

        # Convert the UTC time to EST timezone
        est_now = utc_now.replace(tzinfo=pytz.utc).astimezone(est_tz)

        # Format the datetime in the format "YYYY-MM-DD HH:MM:SS"
        dateTime = est_now.strftime('%Y-%m-%d %H:%M:%S')

        print(dateTime)
        return dateTime