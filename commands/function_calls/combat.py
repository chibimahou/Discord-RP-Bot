import discord
import sqlite3
import os
import re
import math
import function_calls.calc as calc
from discord.ext import commands
from discord import app_commands
from discord.utils import get

def combat(character_name_a, character_name_b, skill_use, weapon_name, skill_a, ailment, armor_value_b, skill_reduction_b, material_modifier_b):
    if(calc.validate_fields(skill_use) == True and calc.validate_fields(character_name_a) == True and calc.validate_fields(character_name_b) == True and calc.validate_fields(skill_a) == True and calc.validate_fields(ailment) == True and calc.validate_fields_commas(weapon_name) == True and  calc.validate_fields(armor_value_b) == True and calc.validate_fields(skill_reduction_b) == True and  calc.validate_fields_commas(material_modifier_b) == True):
        weapon_name_lower = weapon_name.lower()
        character_name_a_lower = character_name_a.lower()
        character_name_b_lower = character_name_b.lower()
        sqliteConnection = sqlite3.connect('characterSheet.db')
        cursor = sqliteConnection.cursor()
        weapon_stats = cursor.execute("SELECT base_power, crit_chance, weapon_material, weapon_attack_type FROM weapons WHERE weapon_name = '" + weapon_name_lower + "'").fetchall()       
        character_a_stats = cursor.execute("SELECT str, dex FROM charactersheets WHERE nickname = '" + character_name_a_lower + "'").fetchall()               
        character_b_stats = cursor.execute("SELECT def, dex FROM charactersheets WHERE nickname = '" + character_name_b_lower + "'").fetchall()               
        if(weapon_stats[0][3].lower() == 'str'):
            offense_a = character_a_stats[0][0]
        else:
            offense_a = character_a_stats[0][1]
        defense_b = character_b_stats[0][0]
        dex_b = character_b_stats[0][1]
        if(len(weapon_stats) != 0):
            material_modifier_a = calc.check_material(weapon_stats[0][2])
            weapon_value_a = weapon_stats[0][0]
            crit_chance_a = weapon_stats[0][1]
        else:
            cursor.close()   
            return('```Weapon does not exist. ```')
        old_inventory = calc.remove_white_spaces_around_commas(weapon_stats[0][0]) 
        skill_use_lower = skill_use.lower()
        ailment_lower = ailment.lower()
        check_graze = calc.check_for_bleed()
        check_crit = calc.check_for_bleed()
        results = ""
        if(ailment_lower == "poison"):
            check_poison = calc.check_for_bleed()
        elif(ailment_lower == "bleed"):
            check_bleed = calc.check_for_bleed()
       
        print(str(check_crit) + " " + str(100 - int(crit_chance_a)))
        chance_for_crit = 100 - int(crit_chance_a)
        if check_crit >= chance_for_crit:
            results = results + "```You landed a critical hit!``` "
            crit_modifier = 1.5
        else:
            crit_modifier = 1 
        
        graze_dex = math.ceil((int(dex_b) / 10) * 5)
        if graze_dex > 40 and skill_use_lower == 'yes':
            graze_dex = 40
        elif graze_dex > 15 and skill_use_lower == 'no':
            graze_dex = 15
        graze_reduction = 90 - graze_dex
        if check_graze >= graze_reduction:
            results = results + "```You were grazed!``` "
            total_graze_reduction = 100 - check_graze
        else:
            total_graze_reduction = 1
        if skill_use_lower == 'yes':
            damage_dealt = calc.skill_damage_calculation(offense_a, weapon_value_a, skill_a, total_graze_reduction, material_modifier_a, defense_b, armor_value_b, skill_reduction_b, material_modifier_b, crit_modifier)
            if check_graze >= graze_reduction:
                results = results + '```You dealt: ' + str(damage_dealt) + ' skill damage.```'
            else:
                results = results + '```You dealt: ' + str(damage_dealt) + ' skill damage.```'   
            cursor.close()                
            return(results)
        else:
            damage_dealt = calc.slash_damage_calculation(offense_a, weapon_value_a, total_graze_reduction, material_modifier_a, defense_b, armor_value_b, material_modifier_b, crit_modifier)
            if check_graze >= graze_reduction:
                results = results + '```You dealt: ' + str(damage_dealt) + ' skill damage.```'
            else:
                results = '```You dealt: ' + str(damage_dealt) + ' skill damage.```' 
            cursor.close()                    
            return(results)
    else:
        return('```You input an invalid character. Please do not use special characters. ```')

def mob_combat(character_name_a, mob_name, skill_use, weapon_name, skill_a, ailment):
    if(calc.validate_fields(skill_use) == True and calc.validate_fields(character_name_a) == True and calc.validate_fields(mob_name) == True and calc.validate_fields(skill_a) == True and calc.validate_fields(ailment) == True and calc.validate_fields_commas(weapon_name) == True):
        weapon_name_lower = weapon_name.lower()
        character_name_a_lower = character_name_a.lower()
        mob_name_b_lower = mob_name.lower()
        armor_value_b = '1'
        skill_reduction_b = '1'
        material_modifier_b = '1'
        sqliteConnection = sqlite3.connect('characterSheet.db')
        cursor = sqliteConnection.cursor()
        sqliteConnection2 = sqlite3.connect('mobspawn.db')
        cursor2 = sqliteConnection2.cursor()
        weapon_stats = cursor.execute("SELECT base_power, crit_chance, weapon_material, weapon_attack_type FROM weapons WHERE weapon_name = '" + weapon_name_lower + "'").fetchall()       
        character_a_stats = cursor.execute("SELECT str, dex FROM charactersheets WHERE nickname = '" + character_name_a_lower + "'").fetchall()               
        mob_b_stats = cursor2.execute("SELECT DEF, DEX FROM stats WHERE name = '" + mob_name_b_lower + "'").fetchall()               
        if(weapon_stats[0][3].lower() == 'str'):
            offense_a = character_a_stats[0][0]
        else:
            offense_a = character_a_stats[0][1]
        defense_b = mob_b_stats[0][0]
        dex_b = mob_b_stats[0][1]
        if(len(weapon_stats) != 0):
            material_modifier_a = calc.check_material(weapon_stats[0][2])
            weapon_value_a = weapon_stats[0][0]
            crit_chance_a = weapon_stats[0][1]
        else:
            cursor2.close()
            cursor.close()   
            return('```Weapon does not exist. ```')
        old_inventory = calc.remove_white_spaces_around_commas(weapon_stats[0][0]) 
        skill_use_lower = skill_use.lower()
        ailment_lower = ailment.lower()
        check_graze = calc.check_for_bleed()
        check_crit = calc.check_for_bleed()
        results = "```"
        if(ailment_lower == "poison"):
            check_poison = calc.check_for_bleed()
        check_bleed = calc.check_for_bleed()
        if check_bleed >= 90:
            results = results + "You inflicted bleed on the " + mob_name_b_lower + "!\n\n"
        print(str(check_crit) + " " + str(100 - int(crit_chance_a)))
        chance_for_crit = 100 - int(crit_chance_a)
        if check_crit >= chance_for_crit:
            results = results + "You landed a critical hit! \n\n"
            crit_modifier = 1.5
        else:
            crit_modifier = 1 
        
        graze_dex = math.ceil((int(dex_b) / 10) * 5)
        if graze_dex > 40 and skill_use_lower == 'yes':
            graze_dex = 40
        elif graze_dex > 15 and skill_use_lower == 'no':
            graze_dex = 15
        graze_reduction = 90 - graze_dex
        if check_graze >= graze_reduction:
            results = results + "You grazed the " + mob_name_b_lower + "!\n\n"
            total_graze_reduction = 100 - check_graze
        else:
            total_graze_reduction = 1
        if skill_use_lower == 'yes':
            damage_dealt = calc.skill_damage_calculation(offense_a, weapon_value_a, skill_a, total_graze_reduction, material_modifier_a, defense_b, armor_value_b, skill_reduction_b, material_modifier_b, crit_modifier)
            if check_graze >= graze_reduction:
                results = results + 'You dealt: ' + str(damage_dealt) + ' skill damage.```'
            else:
                results = results + 'You dealt: ' + str(damage_dealt) + ' skill damage.```' 
            cursor2.close()
            cursor.close()               
            return(results)
        else:
            damage_dealt = calc.slash_damage_calculation(offense_a, weapon_value_a, total_graze_reduction, material_modifier_a, defense_b, armor_value_b, material_modifier_b, crit_modifier)
            if check_graze >= graze_reduction:
                results = results + 'You dealt: ' + str(damage_dealt) + ' skill damage.```'
            else:
                results = results + 'You dealt: ' + str(damage_dealt) + ' skill damage.```' 
            cursor2.close()
            cursor.close()                    
            return(results)
    else:
        return('```You input an invalid character. Please do not use special characters. ```')

def request_duel(character_name_a, character_name_b, type_of_duel):
    if(calc.validate_fields(character_name_a) == True and  calc.validate_fields(character_name_b) == True and  calc.validate_fields(type_of_duel) == True):
        character_a = calc.verify_player_exists(character_name_a)
        character_b = calc.verify_player_exists(character_name_b)
        type_of_duel_no_spaces = calc.remove_white_spaces_around_commas(type_of_duel)
        type_of_duel_lower = type_of_duel_no_spaces[0].lower()
        print(str(type_of_duel_lower))
        if character_a == True and character_b == True:
            if(type_of_duel_lower == 'half loss'):
                return('```' + character_name_a + ' has sent ' + character_name_b + ' a duel request.\n\n Type of duel: Half Loss \n\n Use the command \'/accept_or_decline_duel_invite to reply.\'```')   
            elif(type_of_duel_lower == 'first strike'):
                return('```' + character_name_a + ' has sent ' + character_name_b + ' a duel request.\n\n Type of duel: first strike \n\n Use the command \'/accept_or_decline_duel_invite to reply.\'```')
            elif(type_of_duel_lower == 'total loss'):
                return('```' + character_name_a + ' has sent ' + character_name_b + ' a duel request.\n\n Type of duel: total Loss \n\n Use the command \'/accept_or_decline_duel_invite to reply.\'```')
            else:
                return('``` You did not input a valid duel type. Please use: \n\n half loss, first strike or total loss. ```')
        return('```One of the character nmames do not exist.```')
    else:
        return('```You input an invalid character. Please do not use special characters. ```')

def accept_or_decline_duel_invite(character_name_a, character_name_b, accept_or_decline):
    if(calc.validate_fields(character_name_a) == True and  calc.validate_fields(character_name_b) == True and  calc.validate_fields(accept_or_decline) == True):
        character_a = calc.verify_player_exists(character_name_a)
        character_b = calc.verify_player_exists(character_name_b)
        if character_a == True and character_b == True:
                accept_or_decline_lower = accept_or_decline.lower()
                if accept_or_decline_lower != "accept" and accept_or_decline_lower != "decline":
                        return('``` Please input \'accept\' or \'decline\' in the accept_or_decline field.```')   
                else: 
                        if accept_or_decline_lower == "accept":
                                return('```' + character_name_b + ' has accepted your duel invite.```')   
                        return('```' + character_name_b + ' has declined your duel invite.```')
        return('``` One of the character names do not exist.```')
    else:
        return('```You input an invalid character. Please do not use special characters. ```')
