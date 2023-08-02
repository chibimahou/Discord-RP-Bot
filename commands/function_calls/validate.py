import discord
import sqlite3
import os
import re
import function_calls.calc as calc
import function_calls.query.query as que
from discord.ext import commands
from discord import app_commands
from discord.utils import get
    
def item_exists(item):
            if(calc.validate_fields(item) == True):
                item_lower = item.lower()
                sqliteConnection = sqlite3.connect('equipment.db')
                cursor = sqliteConnection.cursor()
                query = que.check_item_exists_equipment()
                item_exists = cursor.execute(query, (item_lower, item_lower, item_lower, item_lower, item_lower)).fetchone()       
                print(item_exists[0])
                if(len(item_exists) == 0):
                    cursor.close()
                    sqliteConnection.close()
                    return False
                else:
                    cursor.close()
                    sqliteConnection.close()
                    return True
                
def get_blacksmithing_material(item_lower):
        sqliteConnection = sqlite3.connect('equipment.db')
        cursor = sqliteConnection.cursor()
        query = que.check_blacksmithing_material_equipment()
        results = cursor.execute(query, (item_lower, )).fetchone()
        cursor.close()
        sqliteConnection.close()
        return results
                
def get_players_skills(skill_name_lower, character_name_lower, discord_tag):
        sqliteConnection = sqlite3.connect('characterSheet.db')
        cursor = sqliteConnection.cursor()
        query = """SELECT 
                        proficiencySkills 
                        FROM 
                                charactersheets
                                WHERE 
                                        nickname = ? 
                                        AND 
                                                discord_tag = ?;"""
        character_information = cursor.execute(query, (character_name_lower, discord_tag)).fetchone()
        print("skill" + character_information[0])
        proficiency_skills = character_information[0].split(',')  
        print(proficiency_skills)              
        results = calc.get_proficiency(proficiency_skills, skill_name_lower)
        cursor.close()
        sqliteConnection.close()
        return results
       