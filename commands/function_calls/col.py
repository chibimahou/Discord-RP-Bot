import discord
import sqlite3
import os
import re
import function_calls.calc as calc
from discord.ext import commands
from discord import app_commands
from discord.utils import get

def check_col(character_name, col_to_trade):
    if(calc.validate_fields(character_name) == True and  calc.validate_fields(col_to_trade) == True):
        sqliteConnection = sqlite3.connect('characterSheet.db')
        cursor = sqliteConnection.cursor()
        character_current_stat = cursor.execute("SELECT col FROM charactersheets WHERE nickname = '" + character_name + "'").fetchall()
        previous_col = character_current_stat[0][0]
        print(str(previous_col) + " - " + col_to_trade)
        if(previous_col - int(col_to_trade) > 0):
            return True
        else:
            return False
    else:
        return False
    
def add_col(character_name, col_to_add):
    if(calc.validate_fields(character_name) == True and  calc.validate_fields(col_to_add) == True):
        sqliteConnection = sqlite3.connect('characterSheet.db')
        cursor = sqliteConnection.cursor()
        character_current_stat = cursor.execute("SELECT col FROM charactersheets WHERE nickname = '" + character_name + "'").fetchall()
        previous_col = character_current_stat[0][0]
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
        if(int(previous_col) - int(col_to_remove) < 0):
            return '```You do not have ' + str(col_to_remove) + ' col in your inventory.```'
        else:
            new_col_ammount = str(previous_col - int(col_to_remove))
            cursor.execute("UPDATE charactersheets SET col = '" + new_col_ammount + "' WHERE nickname   = '" + character_name + "'").fetchall()
            sqliteConnection.commit()
            return('```' + 'Your new col ammount is: ' + new_col_ammount + '.```')
    else:
        return('```You input an invalid character. Please do not use special characters. ```')
    
def add_col_trade(character_name, col_to_add):
    if(calc.validate_fields(character_name) == True and  calc.validate_fields(col_to_add) == True):
        sqliteConnection = sqlite3.connect('characterSheet.db')
        cursor = sqliteConnection.cursor()
        character_current_stat = cursor.execute("SELECT col FROM charactersheets WHERE nickname = '" + character_name + "'").fetchall()
        previous_col = character_current_stat[0][0]
        new_col_ammount = str(previous_col + int(col_to_add))
        cursor.execute("UPDATE charactersheets SET col = '" + new_col_ammount + "' WHERE nickname = '" + character_name + "'").fetchall()
        sqliteConnection.commit()
        return True
    else:
        return False
    
def remove_col_trade(character_name, col_to_remove):
    if(calc.validate_fields(character_name) == True and  calc.validate_fields(col_to_remove) == True):
        sqliteConnection = sqlite3.connect('characterSheet.db')
        cursor = sqliteConnection.cursor()
        character_current_stat = cursor.execute("SELECT col FROM charactersheets WHERE nickname = '" + character_name + "'").fetchall()
        previous_col = character_current_stat[0][0]
        if(int(previous_col) - int(col_to_remove) < 0):
            return False
        else:
            new_col_ammount = str(previous_col - int(col_to_remove))
            cursor.execute("UPDATE charactersheets SET col = '" + new_col_ammount + "' WHERE nickname   = '" + character_name + "'").fetchall()
            sqliteConnection.commit()
            return True
    else:
        return False