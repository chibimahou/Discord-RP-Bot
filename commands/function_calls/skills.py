import discord
import sqlite3
import os
import re
import function_calls.calc as calc
from discord.ext import commands
from discord import app_commands
from discord.utils import get

def add_skills(character_name, skill_name):
    if(calc.validate_fields(character_name) == True and  calc.validate_fields(skill_name) == True):
        sqliteConnection = sqlite3.connect('characterSheet.db')
        cursor = sqliteConnection.cursor()
        character_skills = cursor.execute("SELECT skilllist FROM characterSheets WHERE nickname = '" + character_name + "'").fetchall()
        skill_name_lower = skill_name.lower()
        old_skills = str(character_skills[0][0]).split(",")
        old_skills_length = len(old_skills)
        new_skills = ""
        temp = 0
        for temp in range(old_skills_length):
                if old_skills[temp] != skill_name_lower and temp < old_skills_length - 1:
                       new_skills = new_skills + old_skills[temp] + "," 
                elif old_skills[temp] != skill_name_lower and temp == old_skills_length - 1:
                       new_skills = new_skills + old_skills[temp] + "," 
                       new_skills = new_skills + skill_name_lower
                else:
                       return('```' + 'The skill: ' + skill_name_lower + ' is already in your skill list.' + '```')

        cursor.execute("UPDATE charactersheets SET skilllist = '" + new_skills + "' WHERE nickname = '" + character_name + "'").fetchall()
        sqliteConnection.commit()
        return('```' + 'The skill: ' + skill_name_lower + ' has been added. Your new skill list is: \n\n' + new_skills + '```')

def remove_skills(character_name, skill_name):
    if(calc.validate_fields(character_name) == True and  calc.validate_fields(skill_name) == True):
        sqliteConnection = sqlite3.connect('characterSheet.db')
        cursor = sqliteConnection.cursor()
        character_skills = cursor.execute("SELECT skilllist FROM characterSheets WHERE nickname = '" + character_name + "'").fetchall()
        skill_name_lower = skill_name.lower()
        old_skills = str(character_skills[0][0]).split(",")
        old_skills_length = len(old_skills)
        new_skills = ""
        temp = 0
        for temp in range(old_skills_length):
                if old_skills[temp] != skill_name_lower and temp < old_skills_length - 1:
                       new_skills = new_skills + old_skills[temp] + "," 
                elif old_skills[temp] != skill_name_lower and temp == old_skills_length:
                        new_skills = new_skills + old_skills[temp]
                        return('```' + 'The skill: ' + skill_name_lower + ' does not exist.' + '```')
                elif old_skills[temp] == skill_name_lower and temp != old_skills_length - 1:
                        new_skills = new_skills + ""
                else:
                        new_skills = new_skills[:-1]
        cursor.execute("UPDATE charactersheets SET skilllist = '" + new_skills + "' WHERE nickname = '" + character_name + "'").fetchall()
        sqliteConnection.commit()
        return('```' + 'The skill: ' + skill_name_lower + ' has been removed. Your new skill list is: \n\n' + new_skills + '```')

def check_skill(skill_name):
    if(calc.validate_fields(skill_name) == True):
        skill_name_lower = skill_name.lower()
        sqliteConnection = sqlite3.connect('characterSheet.db')
        cursor = sqliteConnection.cursor()
        character_skills = cursor.execute("SELECT skill_description, skill_effects FROM proficiency_skills WHERE skill_name = '" + skill_name_lower + "'").fetchall()
        return('```' + skill_name_lower + '\n\n' + character_skills[0][0] + '\n\n' + character_skills[0][1] + '```')

#Adds a proficiency skill.
#Checks if skill exists in the database, if it does, get the callers character sheet.
#Remove commas and adds all skills to an array. After, check each value in a for loop
# and add them into a new array. If the skill names match, add it to the array and return True.  
#if not, return False. If the skill does not exist in the database, return False.
def add_proficiency_skills(character_name, skill_name, discord_tag):
    if(calc.verify_account(character_name, discord_tag)):     
        if(calc.validate_fields(character_name) == True and  calc.validate_fields(skill_name) == True):
            sqliteConnection = sqlite3.connect('characterSheet.db')
            cursor = sqliteConnection.cursor()
            character_inventory = cursor.execute("SELECT proficiencySkills FROM charactersheets WHERE nickname = '" + character_name + "'").fetchall()       
            old_inventory = calc.remove_white_spaces_around_commas(character_inventory[0][0])
            old_inventory_length = len(old_inventory)
            skill_name_lower = skill_name.lower()
            new_inventory = ""
            temp = 0
            for temp in range(old_inventory_length):
                if old_inventory[temp].split(":")[0] == skill_name_lower:
                        cursor.close()
                        return('```This skill is already in your proficiency skill list. ```')
                new_inventory = new_inventory + old_inventory[temp] + ","

            temp2 = 0
            try:
                item_exists = cursor.execute("SELECT skill_name FROM proficiency_skills WHERE skill_name = '" + skill_name_lower + "'").fetchall()
                item_exist_count = item_exists.__len__()
                if item_exist_count != 0:     
                        for temp2 in range(old_inventory_length): 
                                        if temp2 != old_inventory_length - 1:
                                                temp = temp + 1
                                        else:
                                                new_inventory = new_inventory + skill_name_lower + ":1"
                else:
                        return ('``` Sorry, ' + skill_name + ' does not exist. ' + '```')
                cursor.execute("UPDATE charactersheets SET proficiencySkills = '" + new_inventory + "' WHERE nickname = '" + character_name + "'").fetchall()
                sqliteConnection.commit()
                cursor.close()

                return ('```' + skill_name + ' has been successfully added to your inventory. ' + '```')
            except:
                return ('``` Sorry, an error occured.```')
        else:
            return ('``` Sorry, The fields you input were invalid, please check them and try again.```')
    else:
        return ('```This character does not exist.```') 


def remove_proficiency_skills(character_name, skill_name, discord_tag):
    if(calc.verify_account(character_name, discord_tag)):     
        if(calc.validate_fields(character_name) == True and  calc.validate_fields(skill_name) == True):
            sqliteConnection = sqlite3.connect('characterSheet.db')
            cursor = sqliteConnection.cursor()
            character_inventory = cursor.execute("SELECT proficiencySkills FROM charactersheets WHERE nickname = '" + character_name + "'").fetchall()       
            old_inventory = calc.remove_white_spaces_around_commas(character_inventory[0][0])
            old_inventory_length = len(old_inventory)
            new_items = calc.remove_white_spaces_around_commas(skill_name)
            new_items_length = len(new_items)
            skill_name_lower = skill_name.lower()
            new_inventory = ""
            temp = 0
            item_not_found = 0
            temp2 = 0
            try:
                item_exists = cursor.execute("SELECT skill_name FROM proficiency_skills WHERE skill_name = '" + skill_name_lower + "'").fetchall()
                item_exist_count = item_exists.__len__()
                for temp in range(old_inventory_length):
                        if old_inventory[temp].split(":")[0] != skill_name_lower and temp < old_inventory_length - 1:
                            new_inventory = new_inventory + old_inventory[temp] + ","
                            item_not_found = item_not_found + 1 
                        elif old_inventory[temp].split(":")[0] != skill_name_lower and temp == old_inventory_length - 1:
                            new_inventory = new_inventory + old_inventory[temp]
                            item_not_found = item_not_found + 1                         
                        elif old_inventory[temp].split(":")[0] == skill_name_lower and temp < old_inventory_length - 1:
                            temp2 = temp2 + 1
                        else:
                            new_inventory = new_inventory[:-1]
                if item_not_found == old_inventory_length:
                        cursor.close()
                        return('```This skill is not in your proficiency skill list. ```')
                cursor.execute("UPDATE charactersheets SET proficiencySkills = '" + new_inventory + "' WHERE nickname = '" + character_name + "'").fetchall()
                sqliteConnection.commit()
                cursor.close()

                return ('```' + skill_name + ' has been successfully removed from your inventory. ' + '```')
            except:
                return ('``` Sorry, an error occured.```')
        else:
            return ('``` Sorry, The fields you input were invalid, please check them and try again.```')
    else:
        return ('```This character does not exist.```')

def add_proficiency_level(character_name, skill_name, points_to_add, discord_tag):
    if(calc.verify_account(character_name, discord_tag)):     
        if(calc.validate_fields(character_name) == True and  calc.validate_fields(skill_name) == True):
            sqliteConnection = sqlite3.connect('characterSheet.db')
            cursor = sqliteConnection.cursor()
            character_inventory = cursor.execute("SELECT proficiencySkills FROM charactersheets WHERE nickname = '" + character_name + "'").fetchall()       
            old_inventory = calc.remove_white_spaces_around_commas(character_inventory[0][0])
            old_inventory_length = len(old_inventory)
            skill_name_lower = skill_name.lower()
            new_inventory = ""
            temp = 0
            for temp in range(old_inventory_length):
                        if old_inventory[temp].split(":")[0] == skill_name_lower and temp < old_inventory_length - 1:
                                new_skill = old_inventory[temp].split(":")
                                new_proficiency_level = int(new_skill[1]) + int(points_to_add)
                                new_inventory = new_inventory + new_skill[0] + ":" + str(new_proficiency_level) + ","
                        elif old_inventory[temp].split(":")[0] != skill_name_lower and temp < old_inventory_length - 1:
                                new_inventory = new_inventory + old_inventory[temp] + ","
                        elif old_inventory[temp].split(":")[0] == skill_name_lower and temp == old_inventory_length - 1:
                                new_skill = old_inventory[temp].split(":")
                                new_proficiency_level = int(new_skill[1]) + int(points_to_add)
                                new_inventory = new_inventory + new_skill[0] + ":" + str(new_proficiency_level)                             
                        else:
                                new_inventory = new_inventory + old_inventory[temp]
            cursor.execute("UPDATE charactersheets SET proficiencySkills = '" + new_inventory + "' WHERE nickname = '" + character_name + "'").fetchall()
            sqliteConnection.commit()
            cursor.close()            
            return ('```You have added: ' + str(points_to_add) + ' points to your: ' + str(skill_name) + ' skill.```')
        else:
            return ('``` Sorry, The fields you input were invalid, please check them and try again.```')
    else:
        return ('```This character does not exist.```')