import discord
import sqlite3
import array
import random
import math
import function_calls.inventory as inv
import function_calls.skills as ski
import function_calls.experience as exp
import function_calls.col as col
import function_calls.stats as sta
import function_calls.calc as calc
import function_calls.trade as tra
import function_calls.help as help
from discord.ext import commands
from discord import app_commands
from discord.utils import get

def check_location(location):
    location_lower = location.lower()
    sqliteConnection = sqlite3.connect('mobspawn.db')
    cursor = sqliteConnection.cursor()
    query = """SELECT 
            * 
            FROM 
                location
                WHERE
                    area = ?;"""
    location_exists = cursor.execute(query, (location_lower,)).fetchall()
    print(len(location_exists))
    if(len(location_exists) == 0):
        return False
    else:
        return True

def spawn(floor, area):
    if(calc.validate_fields(floor) == True and  calc.validate_fields(area) == True):
        area_lower = area.lower()
        sqliteConnection = sqlite3.connect('mobspawn.db')
        sqliteConnection2 = sqlite3.connect('sessions.db')
        cursor = sqliteConnection.cursor()
        cursor2 = sqliteConnection2.cursor()
        monster_spawns = cursor.execute("SELECT spawns from Location WHERE floor = " + floor + " AND area = '" + area_lower + "'").fetchall()
        spawns= str(monster_spawns[0][0])
        monster_array = calc.remove_white_spaces_around_commas(spawns)
        monster_array_length = len(monster_array) - 1
        print(monster_array_length)
        print(monster_array[0])
        print(monster_array[1])
        random_monster = random.randint(0, monster_array_length)
        print(random_monster)
        monster_information = cursor.execute("""SELECT 
                                                    mobs.name, stats.hp, stats.str, 
                                                    stats.dex, stats.spe, 
                                                    mob_descriptions.mob_description, 
                                                    mobs.drops, stats.def, stats.max_hp, 
                                                    stats.max_str, stats.max_def, stats.max_spe, 
                                                    stats.max_dex, stats.col, stats.xp, 
                                                    stats.max_xp, stats.beginner_level, 
                                                    stats.max_level FROM mobs 
                                                    INNER JOIN 
                                                        stats 
                                                        INNER JOIN 
                                                            mob_descriptions 
                                                            ON 
                                                                mobs.name = stats.name 
                                                                AND 
                                                                    mobs.name = mob_descriptions.name 
                                                                    WHERE 
                                                                        mobs.name = '""" + monster_array[random_monster] + 
                                                                        """'""").fetchall()
        cursor.close()
        return monster_information

def mob_drops(character_name, mob_name, number_defeated, discord_tag):
  if(calc.verify_account(character_name, discord_tag)):     
    if(calc.validate_fields(character_name) == True and  calc.validate_fields(mob_name) == True, calc.validate_fields(number_defeated) == True):
        sqliteConnection = sqlite3.connect('mobspawn.db')
        character_name_lower = character_name.lower()
        mob_name_lower = mob_name.lower()
        cursor = sqliteConnection.cursor()
        monster_spawns = cursor.execute("SELECT drops from mobs WHERE name = '" + mob_name_lower + "'").fetchall()
        if len(monster_spawns) != 0:
            drops_array = calc.remove_white_spaces_around_commas(monster_spawns[0][0])
            temp = 0
            random_item = []
            items_added = ""
            monster_drop_total = len(drops_array)
            for temp in range(monster_drop_total):
                random_item.append(drops_array[random.randrange(0, monster_drop_total)])
            for temp in range(len(random_item) - 1):
                if(temp == len(random_item) - 1):
                    items_added = items_added + random_item[temp]
                    inv.add_inventory(character_name, random_item[temp], discord_tag)
                else:
                    items_added = str(items_added) + str(random_item[temp]) + ", "
                    inv.add_inventory(character_name, random_item[temp], discord_tag)                   
        cursor.close()
        return('```items: ' + items_added + ' were successfully added to your inventory.```')
  else:
        return('``` This account is not linked to this discord account. Please log into the proper account, or reach out to a moderator to switch accounts if you do not have access to that account. ```')

