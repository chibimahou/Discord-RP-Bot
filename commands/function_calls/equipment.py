import discord
import sqlite3
import os
import re
import function_calls.calc as calc
from discord.ext import commands
from discord import app_commands
from discord.utils import get

def add_equipment(character_name, equipment_to_equip):
    if(calc.validate_fields(character_name) == True and  calc.validate_fields(equipment_to_equip) == True):
        sqliteConnection = sqlite3.connect('characterSheet.db')
        cursor = sqliteConnection.cursor()
        character_current_stat = cursor.execute("SELECT equipment FROM charactersheets WHERE nickname = '" + character_name + "'").fetchall()
        equipment = calc.remove_white_spaces_around_commas(character_current_stat[0][0])
        new_equipment = ""
        temp = 0
#Check if the equipment you want to equip exists in the database.
        character_equipment = cursor.execute("SELECT catagory FROM armor WHERE armor_name = '" + equipment_to_equip.lower() + "'").fetchall()
        if len(character_equipment) != 1:
            character_equipment = cursor.execute("SELECT catagory FROM weapons WHERE weapon_name = '" + equipment_to_equip.lower() + "'").fetchall()
            if len(character_equipment) != 1:
                return('```The equipment you want to equip does not exist. ```')
            else:
                item_to_equip_catagory = character_current_stat[0][0]
        else:
            item_to_equip_catagory = character_current_stat[0][0]
#Check the catagory for each item currently equipped.
        for temp in range(len(equipment)):
            character_equipment = cursor.execute("SELECT armor_name, catagory FROM armor WHERE armor_name = '" + equipment[temp].lower() + "'").fetchall()
            if len(character_equipment) != 1:
                character_equipment = cursor.execute("SELECT weapon_name, catagory FROM weapons WHERE weapon_name = '" + equipment[temp].lower() + "'").fetchall()
                if len(character_equipment) != 1:
                    return('```Something went wrong with your currently equipment. ```')                    
                else:
                    if character_equipment[0][1] == item_to_equip_catagory:
                        new_equipment = new_equipment + equipment_to_equip.lower() + ','


        new_col_ammount = str(previous_col + int(col_to_add))
        cursor.execute("UPDATE charactersheets SET col = '" + new_col_ammount + "' WHERE nickname = '" + character_name + "'").fetchall()
        sqliteConnection.commit()
        return('```' + 'Your new col ammount is: ' + new_col_ammount + '.```')
    else:
        return('```You input an invalid character. Please do not use special characters. ```')

def remove_col(character_name, col_to_remove):
    if(calc.validate_fields(character_name) == True and  calc.validate_fields(col_to_remove) == True):
        sqliteConnection = sqlite3.connect('characterSheet.db')
        cursor = sqliteConnection.cursor()
        character_current_stat = cursor.execute("SELECT col FROM charactersheets WHERE nickname = '" + character_name + "'").fetchall()
        previous_col = character_current_stat[0][0]
        new_col_ammount = str(previous_col - int(col_to_remove))
        cursor.execute("UPDATE charactersheets SET col = '" + new_col_ammount + "' WHERE nickname   = '" + character_name + "'").fetchall()
        sqliteConnection.commit()
        return('```' + 'Your new col ammount is: ' + new_col_ammount + '.```')
    else:
        return('```You input an invalid character. Please do not use special characters. ```')