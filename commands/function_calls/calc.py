import discord
import sqlite3
import array
import random
import re
import math
import function_calls.inventory as inv
import function_calls.skills as ski
import function_calls.experience as exp
import function_calls.col as col
import function_calls.stats as sta
import function_calls.calc as mat
import function_calls.trade as tra
import function_calls.help as help
from discord.ext import commands
from discord import app_commands
from discord.utils import get


def seperate_string_to_array(string_to_seperate):
        new_string = str(string_to_seperate).split(",")
        return new_string

def remove_white_spaces_around_commas(string_to_remove_white_spaces):
        string_with_no_white_spaces = string_to_remove_white_spaces.replace(" ,", ",")
        string_with_no_white_spaces = string_to_remove_white_spaces.replace(", ", ",") 
        string_with_no_white_spaces_array = seperate_string_to_array(string_with_no_white_spaces)
        return string_with_no_white_spaces_array

def get_player_stats(character_name):
        sqliteConnection = sqlite3.connect('characterSheet.db')
        cursor = sqliteConnection.cursor()
        character_information = cursor.execute("SELECT str, def, spd FROM charactersheets WHERE nickname = '" + character_name + "'").fetchall()
        stats = [character_information[0][0], character_information[0][1], character_information[0][2]]
        str(character_information).format()
        return stats

def add_to_guild(character_name, guild_name):
        sqliteConnection = sqlite3.connect('characterSheet.db')
        cursor = sqliteConnection.cursor()
        cursor.execute("UPDATE charactersheets SET guild = '" + guild_name + "' WHERE nickname = '" + character_name + "'").fetchall()
        return True

def verify_player_exists(character_name):
        character_name_lower = character_name.lower()
        sqliteConnection = sqlite3.connect('characterSheet.db')
        cursor = sqliteConnection.cursor()
        character_in_table = cursor.execute("SELECT nickname FROM charactersheets WHERE nickname = '" + character_name_lower + "';").fetchall()
        if len(character_in_table) < 1:
                return(False)
        sqliteConnection.commit()
        cursor.close()  
        return(True)

def verify_guild_exists(guild_name):
        guild_name_lower = guild_name.lower()
        sqliteConnection = sqlite3.connect('characterSheet.db')
        cursor = sqliteConnection.cursor()
        character_in_table = cursor.execute("SELECT guild_name FROM guilds WHERE guild_name = '" + guild_name_lower + "';").fetchall()
        if len(character_in_table) < 1:
                return(False)
        return(True)

def check_guild_approvers(approver_name, guild_name):
        guild_name_lower = guild_name.lower()
        sqliteConnection = sqlite3.connect('characterSheet.db')
        cursor = sqliteConnection.cursor()
        character_in_table = cursor.execute("SELECT guild_approvers FROM guilds WHERE guild_name = '" + guild_name_lower + "';").fetchall()
        approver_array = remove_white_spaces_around_commas(character_in_table[0][0])

        temp = 0
        for temp in range(len(approver_array)):
                if approver_array[temp] == approver_name:
                        return(True)
        return(False)
        
def check_for_bleed():
        bleed_success = random.randint(0,100)
        return(bleed_success)

def get_character_information(character_name):
        sqliteConnection = sqlite3.connect('characterSheet.db')
        cursor = sqliteConnection.cursor()
        character_information = cursor.execute("SELECT firstName, lastName, height, size, age, skillList, inventory, bio, guild, class, playerColor, birthday, nickname, uniqueSkills, proficiencySkills, currentWeaponEquipped, col, experience, level, str, def, spd, playerStatus, batt_status FROM charactersheets WHERE nickname = '" + character_name + "'").fetchall()
        return(character_information)

def item_exists(item_name):
        item_name_lower = item_name.lower()
        sqliteConnection = sqlite3.connect('characterSheet.db')
        cursor = sqliteConnection.cursor()
        character_information = cursor.execute("SELECT item FROM items WHERE item = '" + item_name_lower + "'").fetchall()
        if len(character_information) != 1:
                return(False)
        else:
                return(True)

def weapon_exists(weapon_name):
        weapon_name_lower = weapon_name.lower()
        sqliteConnection = sqlite3.connect('characterSheet.db')
        cursor = sqliteConnection.cursor()
        character_information = cursor.execute("SELECT weapon_name FROM weapons WHERE weapon_name = '" + weapon_name_lower + "'").fetchall()
        if len(character_information) != 1:
                return(False)
        else:
                return(True)

def armor_exists(armor_name):
        armor_name_lower = armor_name.lower()
        sqliteConnection = sqlite3.connect('characterSheet.db')
        cursor = sqliteConnection.cursor()
        character_information = cursor.execute("SELECT armor_name FROM armor WHERE armor_name = '" + armor_name_lower + "'").fetchall()
        if len(character_information) != 1:
                return(False)
        else:
                return(True)

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
                     return (True)
        return(False)

def skill_damage_calculation(offense_a, weapon_value_a, skill_a, graze_reduction, material_modifier_a, defense_b, armor_value_b, skill_reduction_b, material_modifier_b, crit_modifier):
        if int(defense_b) <= 10:
                defense_modifier = 1.0
                total_damage_reduction = math.ceil((float(defense_modifier) * (float(armor_value_b) + float(skill_reduction_b)) * float(material_modifier_b)))
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
                total_damage_reduction = math.ceil((float(defense_modifier) * (float(armor_value_b) + float(skill_reduction_b)) * float(material_modifier_b)))
        if int(offense_a) <= 10:
                offense_modifier = 1.0
                total_damage = math.ceil((float(offense_modifier) * (float(weapon_value_a) + float(skill_a)) * float(material_modifier_a)))
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
                
                total_damage = math.ceil((float(offense_modifier) * (float(weapon_value_a) + float(skill_a)) * float(material_modifier_a)))

        damage_dealt = math.ceil((total_damage - total_damage_reduction) * float(crit_modifier))
        total_reduction = math.ceil(((100 - graze_reduction) / 100) * damage_dealt)

        graze_damage_reduction = math.ceil(total_reduction)
        return(graze_damage_reduction)

def slash_damage_calculation(offense_a, weapon_value_a, graze_reduction, material_modifier_a, defense_b, armor_value_b, material_modifier_b, crit_modifier):
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

    return False