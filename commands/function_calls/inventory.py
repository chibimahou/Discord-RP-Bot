import discord
import sqlite3
import os
import re
import function_calls.calc as calc
from discord.ext import commands
from discord import app_commands
from discord.utils import get

def add_inventory(character_name, items_to_add, discord_tag):
    if(calc.verify_account(character_name, discord_tag)):     
        if(calc.validate_fields(character_name) == True and  calc.validate_fields(items_to_add) == True):
            sqliteConnection = sqlite3.connect('characterSheet.db')
            cursor = sqliteConnection.cursor()
            character_inventory = cursor.execute("SELECT inventory FROM charactersheets WHERE nickname = '" + character_name + "'").fetchall()       
            items_to_add_lower = items_to_add.lower()            
            old_inventory = calc.remove_white_spaces_around_commas(character_inventory[0][0])
            old_inventory_length = len(old_inventory)
            new_inventory = ""
            item_found = 0
            temp = 0
            for temp in range(old_inventory_length):
                print(str(temp) + " " + str(old_inventory_length))
                if old_inventory[temp].split(":")[0] != items_to_add_lower and temp < old_inventory_length - 1:
                    print(str(old_inventory[temp].split(":")[0]) + " " + str(items_to_add_lower))
                    new_inventory = new_inventory + old_inventory[temp] + ","                    
                elif old_inventory[temp].split(":")[0] != items_to_add_lower and temp == old_inventory_length - 1:
                    print(str(old_inventory[temp].split(":")[0]) + " " + str(items_to_add_lower))
                    new_inventory = new_inventory + old_inventory[temp]                    
                elif old_inventory[temp].split(":")[0] == items_to_add_lower and temp < old_inventory_length - 1:
                    item_found = 1
                    print(str(old_inventory[temp].split(":")[0]) + " " + str(items_to_add_lower)) 
                    items_added = int(old_inventory[temp].split(":")[1]) + 1
                    new_inventory = new_inventory + str(old_inventory[temp].split(":")[0]) + ":" + str(items_added) + ","
                else:
                    item_found = 1
                    print(str(old_inventory[temp].split(":")[0]) + " " + str(items_to_add_lower))
                    items_added = int(old_inventory[temp].split(":")[1]) + 1
                    new_inventory = new_inventory + str(old_inventory[temp ].split(":")[0]) + ":" + str(items_added)
            if item_found != 1:
                    new_inventory = new_inventory + "," +  items_to_add_lower + ":1 "                     
            cursor.execute("UPDATE charactersheets SET inventory = '" + new_inventory + "' WHERE nickname = '" + character_name + "'").fetchall()
            sqliteConnection.commit()
            character_information = cursor.execute("SELECT inventory FROM charactersheets WHERE nickname = '" + character_name + "'").fetchall()       
            sqliteConnection.commit()
            cursor.close()

            return ('```' + items_to_add + ' has been successfully added to your inventory. ' + '```')
        else:
            return ('``` Sorry, The fields you input were invalid, please check them and try again.```')
    else:
        return ('```This character does not exist.```') 

def remove_inventory(character_name, items_to_remove, discord_tag):
    if(calc.verify_account(character_name, discord_tag)):     
        if(calc.validate_fields(character_name) == True and  calc.validate_fields(items_to_remove) == True):
            sqliteConnection = sqlite3.connect('characterSheet.db')
            cursor = sqliteConnection.cursor()
            character_inventory = cursor.execute("SELECT inventory FROM charactersheets WHERE nickname = '" + character_name + "'").fetchall()       
            old_inventory = calc.remove_white_spaces_around_commas(str(character_inventory[0][0]))
            old_inventory_length = len(old_inventory)
            items_to_remove_lower = items_to_remove.lower()
            new_inventory = ""
            temp = 0
            temp2 = 0
            print(str(temp) + " " + str(old_inventory_length))
            for temp in range(old_inventory_length):
                print(str(temp) + " " + str(old_inventory_length))
                if str(old_inventory[temp].split(":")[0]) != items_to_remove_lower and temp < old_inventory_length - 1:
                    new_inventory = new_inventory + old_inventory[temp] + ","
                elif str(old_inventory[temp].split(":")[0]) != items_to_remove_lower and temp == old_inventory_length - 1:
                    new_inventory = new_inventory + old_inventory[temp]
                elif str(old_inventory[temp].split(":")[0]) == items_to_remove_lower and temp < old_inventory_length - 1:
                    if int(old_inventory[temp].split(":")[1]) > 1:
                        item_removed = int(old_inventory[temp].split(":")[1]) - 1
                        new_inventory = new_inventory + str(old_inventory[temp].split(":")[0]) + ":" + str(item_removed) + ","                    
                else:
                    if int(old_inventory[temp].split(":")[1]) > 1:
                        item_removed = int(old_inventory[temp].split(":")[1]) - 1
                        new_inventory = new_inventory + str(old_inventory[temp].split(":")[0]) + ":" + str(item_removed)                    
                    else:
                        new_inventory = new_inventory[:-1]
            try:

                cursor.execute("UPDATE charactersheets SET inventory = '" + new_inventory + "' WHERE nickname = '" + character_name + "'").fetchall()
                sqliteConnection.commit()
                character_information = cursor.execute("SELECT inventory FROM charactersheets WHERE nickname = '" + character_name + "'").fetchall()       
                sqliteConnection.commit()
                cursor.close()

                return ('```' + items_to_remove + ' has been successfully removed from your inventory. ' + '```')
            except:
                cursor.close()
                return ('``` Sorry, ' + items_to_remove + ' is not in your inventory. ' + '```')
        else:
            return ('``` Sorry, The fields you input were invalid, please check them and try again.```')
    else:
        return ('```This character does not exist.```') 

def inventory(character_name):
    if(calc.validate_fields(character_name) == True):
        sqliteConnection = sqlite3.connect('characterSheet.db')
        cursor = sqliteConnection.cursor()
        character_information = cursor.execute("SELECT inventory FROM charactersheets WHERE nickname = '" + character_name + "'").fetchall()
        cursor.close()
        character_inventory = character_information[0][0]
        print(character_inventory)

        return character_inventory

def check_inventory_for_item(character_name, item_to_check):
    if(calc.validate_fields(character_name) == True and  calc.validate_fields(item_to_check) == True):
        character_inventory = inventory(character_name)
        item_to_check_lower = item_to_check.lower()
        current_inventory = calc.remove_white_spaces_around_commas(character_inventory)
        inventory_size = len(current_inventory)
        temp = 0
        for temp in range(inventory_size):
            print(character_inventory[temp] + " item to check: " + item_to_check_lower)
            if(current_inventory[temp] == item_to_check):
                return True
        return False
