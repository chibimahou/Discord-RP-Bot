import discord
import sqlite3
import random
import os
import re
import math as mat
import function_calls.calc as calc
from discord.ext import commands
from discord import app_commands
from discord.utils import get

def add_beast(character_name, pet_name, pet_nickname, discord_tag):
        if(calc.verify_account(character_name, discord_tag)):
            sqliteConnection = sqlite3.connect('characterSheet.db')
            cursor = sqliteConnection.cursor()            
            pet_name_lower = pet_name.lower()
            pet_nickname_lower = pet_nickname.lower()
            pet_current_stat = cursor.execute("""SELECT 
                base_level, base_hp, base_str, base_def, base_spd, base_dex, 
                hp_growth_rate, str_growth_rate, def_growth_rate, spd_growth_rate, dex_growth_rate 
                FROM 
                    beastdb 
                    WHERE 
                        beasts_name = '""" + pet_name_lower + """';""").fetchall()
            if(pet_current_stat is not None):
                pet_uv_hp = random.randint(1,31)
                pet_uv_str = random.randint(1,31)
                pet_uv_def = random.randint(1,31)
                pet_uv_spd = random.randint(1,31)
                pet_uv_dex = random.randint(1,31)
                pet_base_lvl = pet_current_stat[0][0]
                pet_base_hp = pet_current_stat[0][1]
                pet_base_str = pet_current_stat[0][2]
                pet_base_def = pet_current_stat[0][3]
                pet_base_spd = pet_current_stat[0][4]
                pet_base_dex = pet_current_stat[0][5]
                str_pet_base_lvl = str(pet_base_lvl)
                str_pet_base_hp = str(pet_base_hp)
                str_pet_base_str = str(pet_base_str)
                str_pet_base_def = str(pet_base_def)
                str_pet_base_spd = str(pet_base_spd)
                str_pet_base_dex = str(pet_base_dex)
                str_pet_uv_hp = str(pet_uv_hp)
                str_pet_uv_str = str(pet_uv_str)
                str_pet_uv_def = str(pet_uv_def)
                str_pet_uv_spd = str(pet_uv_spd)
                str_pet_uv_dex = str(pet_uv_dex)
                str_discord_tag = str(discord_tag)
                
                combined_value = [pet_name_lower, str_pet_uv_hp, str_pet_uv_str, str_pet_uv_def, 
                                  str_pet_uv_spd, str_pet_uv_dex, str_discord_tag]
                key = calc.generate_key(combined_value)
                print(key)
                cursor.execute("""INSERT INTO 
                    characters_beasts
                        (pet_name, pet_nickname, level, hp, str, 
                        def, spd, dex, uv_hp, uv_str, uv_def, 
                        uv_spd, uv_dex, players_tag, unique_identifier) 
                        VALUES 
                            ('""" + pet_name_lower + """', '""" + pet_nickname_lower + 
                            """', '""" + str_pet_base_lvl + """', '""" + str_pet_base_hp + 
                            """', '""" + str_pet_base_str + """', '""" + str_pet_base_def + 
                            """', '""" + str_pet_base_spd + """', '""" + str_pet_base_dex + 
                            """', '""" + str_pet_uv_hp + """', '""" + str_pet_uv_str + 
                            """', '""" + str_pet_uv_def + """', '""" + str_pet_uv_spd + 
                            """', '""" + str_pet_uv_dex + """', '""" + str_discord_tag + 
                            """', '""" + key + """')""")
                sqliteConnection.commit()
                cursor.close()      
                return('```' + 'Your new pet ' + pet_name_lower + ' has been tamed.```')
            else:
                 return "There is no beast by this name."

        else:
            return('``` This account is not linked to this discord account. Please log into the proper account, or reach out to a moderator to switch accounts if you do not have access to that account. ```')

def check_pet(character_name, pet_name, discord_tag):
        if(calc.verify_account(character_name, discord_tag)):
            sqliteConnection = sqlite3.connect('characterSheet.db')
            cursor = sqliteConnection.cursor()
            character_name_lower = character_name.lower()
            pet = cursor.execute("""SELECT 
                pet_name, pet_nickname, pet_level, base_hp, base_str, 
                base_def, base_spd, base_dex 
                FROM 
                    characters_pet 
                    WHERE 
                        pet_name = '""" + pet_name + """' 
                        OR 
                            pet_nickname = '""" + pet_name + """'""").fetchall()
            pet_name = pet[0][0]
            pet_nickname = pet[0][1]
            pet_lvl = pet[0][2]
            pet_hp = pet[0][3]
            pet_str = pet[0][4]
            pet_def = pet[0][5]
            pet_spd = pet[0][6]
            pet_dex = pet[0][7]
            cursor.close()
            return("""```monster name: ** """ + pet_name + """ **
                \n** pet name ** """ + pet_nickname + """ **
                \n** level: """ + pet_lvl + """ **
                \n*** Stats ***
                \n** hp: """ + pet_hp + """ **
                \n** str: """ + pet_str + """ **
                \n** def: """ + pet_def + """ **
                \n** spd: """ + pet_spd + """ **
                \n** dex: """ + pet_dex + """ ** ```""")
        else:
            return('``` This account is not linked to this discord account. Please log into the proper account, or reach out to a moderator to switch accounts if you do not have access to that account. ```')


def level_up_pet(character_name, pet_nickname, levels, discord_tag):
        if(calc.verify_account(character_name, discord_tag)):     
            if(calc.validate_fields(character_name) == True):
                pet_name_lower = pet_nickname.lower()
                sqliteConnection = sqlite3.connect('characterSheet.db')
                cursor = sqliteConnection.cursor()
                pet = cursor.execute("""SELECT 
                    character_pet.pet_level, 
                    character_pet.base_hp, character_pet.base_str, 
                    character_pet.base_def, character_pet.base_spd, 
                    character_pet.base_dex, petdb.growth_hp, petdb.growth_str, 
                    petdb.growth_def, petdb.growth_spd, petdb.growth_dex,
                    petdb.hp, petdb.str, petdb.def, petdb.spd, petdb.dex 
                    FROM 
                        characters_pet INNER JOIN petdb 
                        ON 
                            character_pet.pet_name = petdb.pet_name 
                            WHERE 
                                pet_name = '""" + pet_name_lower + """' 
                                OR 
                                    pet_nickname = '""" + pet_name_lower + """'""").fetchall()
                pet_level = pet[0][0] - levels
                pet_hp_growth = pet[0][6]
                pet_str_growth = pet[0][7]
                pet_def_growth = pet[0][8]
                pet_spd_growth = pet[0][9]
                pet_dex_growth = pet[0][10]
                pet_uv_hp = pet[0][11]
                pet_uv_str = pet[0][12]
                pet_uv_def = pet[0][13]
                pet_uv_spd = pet[0][14]
                pet_uv_dex = pet[0][15]
                pet_base_hp = pet[0][16]
                pet_base_str = pet[0][17]
                pet_base_def = pet[0][18]
                pet_base_spd = pet[0][19]
                pet_base_dex = pet[0][20]

                pet_new_hp = (mat.floor(pet_level / pet_hp_growth)  + pet_base_hp) / ((( 100 - pet_uv_hp) / 100))
                pet_new_str = (mat.floor(pet_level / pet_str_growth)  + pet_base_str) / ((pet_uv_str / 100))
                pet_new_def = (mat.floor(pet_level / pet_def_growth)  + pet_base_def) / ((pet_uv_def / 100))
                pet_new_spd = (mat.floor(pet_level / pet_spd_growth)  + pet_base_spd) / ((pet_uv_spd / 100))
                pet_new_dex = (mat.floor(pet_level / pet_dex_growth)  + pet_base_dex) / ((pet_uv_dex / 100))
                cursor.execute("""UPDATE 
                    characters_pet 
                    SET 
                        pet_base_hp = '""" + pet_new_hp + """' 
                        , pet_base_str = '""" + pet_new_str + """'
                        , pet_base_def = '""" + pet_new_def + """'
                        , pet_base_spd = '""" + pet_new_spd + """'
                        , pet_base_dex = '""" + pet_new_dex + """'
                        , pet_level = '""" + pet_level + """'
                        WHERE 
                            player_tag = '""" + discord_tag + """' 
                            AND 
                                pet_nickname = '""" + pet_nickname + """'""")
                cursor.close()
                return('```Your pet has leveled up! hp: ' + pet_new_hp + ' str: ' + pet_new_str + ' def: ' + pet_new_def + ' spd: ' + pet_new_spd + ' dex: ' + pet_new_dex + '```')
            else:
                return('``` This account is not linked to this discord account. Please log into the proper account, or reach out to a moderator to switch accounts if you do not have access to that account. ```')

def level_down_pet(character_name, pet_nickname, levels, discord_tag):
        if(calc.verify_account(character_name, discord_tag)):     
            if(calc.validate_fields(character_name) == True):
                pet_name_lower = pet_nickname.lower()
                sqliteConnection = sqlite3.connect('characterSheet.db')
                cursor = sqliteConnection.cursor()
                pet = cursor.execute("""SELECT 
                    character_pet.pet_level, 
                    character_pet.base_hp, character_pet.base_str, 
                    character_pet.base_def, character_pet.base_spd, 
                    character_pet.base_dex, petdb.growth_hp, petdb.growth_str, 
                    petdb.growth_def, petdb.growth_spd, petdb.growth_dex,
                    petdb.hp, petdb.str, petdb.def, petdb.spd, petdb.dex 
                    FROM 
                        characters_pet INNER JOIN petdb 
                        ON 
                            character_pet.pet_name = petdb.pet_name 
                            WHERE 
                                pet_name = '""" + pet_name_lower + """' 
                                OR 
                                    pet_nickname = '""" + pet_name_lower + """'""").fetchall()
                pet_level = pet[0][0] - levels
                pet_hp_growth = pet[0][6]
                pet_str_growth = pet[0][7]
                pet_def_growth = pet[0][8]
                pet_spd_growth = pet[0][9]
                pet_dex_growth = pet[0][10]
                pet_uv_hp = pet[0][11]
                pet_uv_str = pet[0][12]
                pet_uv_def = pet[0][13]
                pet_uv_spd = pet[0][14]
                pet_uv_dex = pet[0][15]
                pet_base_hp = pet[0][16]
                pet_base_str = pet[0][17]
                pet_base_def = pet[0][18]
                pet_base_spd = pet[0][19]
                pet_base_dex = pet[0][20]

                pet_new_hp = (mat.floor(pet_level / pet_hp_growth)  + pet_base_hp) * ((pet_uv_hp / 100))
                pet_new_str = (mat.floor(pet_level / pet_str_growth)  + pet_base_str) * ((pet_uv_str / 100))
                pet_new_def = (mat.floor(pet_level / pet_def_growth)  + pet_base_def) * ((pet_uv_def / 100))
                pet_new_spd = (mat.floor(pet_level / pet_spd_growth)  + pet_base_spd) * ((pet_uv_spd / 100))
                pet_new_dex = (mat.floor(pet_level / pet_dex_growth)  + pet_base_dex) * ((pet_uv_dex / 100))
                cursor.execute("""UPDATE 
                    characters_pet 
                    SET 
                        pet_base_hp = '""" + pet_new_hp + """' 
                        , pet_base_str = '""" + pet_new_str + """'
                        , pet_base_def = '""" + pet_new_def + """'
                        , pet_base_spd = '""" + pet_new_spd + """'
                        , pet_base_dex = '""" + pet_new_dex + """'
                        , pet_level = '""" + pet_level - 1 + """'
                        WHERE 
                            player_tag = '""" + discord_tag + """' 
                            AND 
                                pet_nickname = '""" + pet_nickname + """'""")
                cursor.close()
                return('```Your pet has leveled down! hp: ' + pet_new_hp + ' str: ' + pet_new_str + ' def: ' + pet_new_def + ' spd: ' + pet_new_spd + ' dex: ' + pet_new_dex + '```')
            else:
                return('``` This account is not linked to this discord account. Please log into the proper account, or reach out to a moderator to switch accounts if you do not have access to that account. ```')

def stat_screen(character_name):
    if(calc.validate_fields(character_name) == True):
        sqliteConnection = sqlite3.connect('characterSheet.db')
        cursor = sqliteConnection.cursor()
        character_information = cursor.execute("SELECT str, def, spd, dex FROM charactersheets WHERE nickname = '" + character_name + "'").fetchall()
        cursor.close()
        return('```str: ' + str(character_information[0][0]) + '\ndef: ' + str(character_information[0][1]) + '\nspd: ' + str(character_information[0][2]) + '\ndex: ' + str(character_information[0][3]) + '```')
