import discord
import sqlite3
import os
import re
import function_calls.calc as calc
import function_calls.query.query as que
from discord.ext import commands
from discord import app_commands
from discord.utils import get

def check_item(item):
        if(calc.validate_fields(item) == True):
            item_lower = item.lower()
            sqliteConnection = sqlite3.connect('equipment.db')
            cursor = sqliteConnection.cursor()
            query = que.check_item_exists_equipment()
            item_exists = cursor.execute(query, (item_lower, item_lower, item_lower, item_lower)).fetchone()       
            print(item_exists[0])
            if(len(item_exists) == 0):
                cursor.close()
                sqliteConnection.close()
                return "```Sorry, the item " + item_lower + " does not exist.```"
            else:
                if(item_exists[0] == "items"):
                    query = que.check_item_equipment()
                    item_description = cursor.execute(query, (item_lower, )).fetchone()
                    results = """```
** """ + item_description[0] + """ **
                    
** Rarity:       """ + item_description[2] + """ **
** Obtained by:  """ + item_description[3] + """ **
                    
** Description ** 
    """ + item_description[1] + """```"""
                    
                elif(item_exists[0] == "weapons"):
                    query = que.check_weapon_equipment()
                    item_description = cursor.execute(query, (item_lower, )).fetchone()
                    results = """```
** """ + item_description[0] + """ ** 
                    
** Rarity:      """ + item_description[2] + """ **
** Obtained by: """ + item_description[3] + """ **
** Attack:      """ + item_description[4] + """ **
** Effects:     """ + item_description[5] + """ **
** Crit Chance: """ + item_description[6] + """ **
** Material:    """ + item_description[7] + """ **  
** Attack Type: """ + item_description[8] + """ **
** Catagory:    """ + item_description[9] + """ **
                    
** Description ** 
    """ + item_description[1] + """```"""
                    
                elif(item_exists[0] == "fishdb"):
                    query = que.check_fish_equipment()
                    item_description = cursor.execute(query, (item_lower, )).fetchone()
                    results = """```
** """ + item_description[0] + """ ** 
                    
** Rarity:      """ + item_description[2] + """ **
** Obtained by: """ + item_description[3] + """ **
** location:    """ + item_description[4] + """ **
** Difficulty:  """ + item_description[5] + """ **
                    
** Description **
    """ + item_description[1] + """```"""
                    
                else:
                    query = que.check_armor_equipment()
                    item_description = cursor.execute(query, (item_lower, )).fetchone()
                    results = """```
** """ + item_description[0] + """ ** 
                    
** Rarity:      """ + item_description[2] + """ **
** Obtained by: """ + item_description[3] + """ **
** Defense:     """ + item_description[4] + """ **
** Effects:     """ + item_description[5] + """ **
** Material:    """ + item_description[6] + """ **
** Catagory:    """ + item_description[7] + """ **
                    
** Description **
    """ + item_description[1] + """```"""                   
                cursor.close()
                sqliteConnection.close()

                return results
        else:
            return ('``` Sorry, The fields you input were invalid, please check them and try again.```')

    
def item_exists(item):
            if(calc.validate_fields(item) == True):
                item_lower = item.lower()
                sqliteConnection = sqlite3.connect('equipment.db')
                cursor = sqliteConnection.cursor()
                query = que.check_item_exists_equipment()
                item_exists = cursor.execute(query, (item_lower, item_lower, item_lower, item_lower)).fetchone()       
                print(item_exists[0])
                if(len(item_exists) == 0):
                    cursor.close()
                    sqliteConnection.close()
                    return False
                else:
                    return True