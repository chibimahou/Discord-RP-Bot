import discord
import sqlite3
import random
import os
import re
import math as mat
import function_calls.calc as calc
import function_calls.query.query as que
from discord.ext import commands
from discord import app_commands
from discord.utils import get

def add_beast(character_name, pet_name, pet_nickname, discord_tag):
        if(calc.verify_account(character_name, discord_tag)):
            sqliteConnection = sqlite3.connect('beasts.db')
            cursor = sqliteConnection.cursor()            
            pet_name_lower = pet_name.lower()
            pet_nickname_lower = pet_nickname.lower()
            query = que.check_beast_beastdb()
            print(query)
            pet_current_stat = cursor.execute(query, (pet_name_lower,)).fetchall()
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
                query = que.add_beast_characters_beasts()
                print(query)
                cursor.execute(query, (pet_name_lower, pet_nickname_lower, str_pet_base_lvl, 
                                       str_pet_base_hp, str_pet_base_str, str_pet_base_def, 
                                       str_pet_base_spd, str_pet_base_dex, str_pet_uv_hp,
                                       str_pet_uv_str, str_pet_uv_def, str_pet_uv_spd,
                                       str_pet_uv_dex, str_discord_tag, key))
                sqliteConnection.commit()
                cursor.close()      
                return('```' + 'Your new pet ' + pet_name_lower + ' has been tamed.```')
            else:
                 return "There is no beast by this name."

        else:
            return('``` This account is not linked to this discord account. Please log into the proper account, or reach out to a moderator to switch accounts if you do not have access to that account. ```')

def check_beast(character_name, beasts_nickname, discord_tag):
        if(calc.verify_account(character_name, discord_tag)):
            sqliteConnection = sqlite3.connect('beasts.db')
            cursor = sqliteConnection.cursor()
            character_name_lower = character_name.lower()
            beasts_nickname_lower = beasts_nickname.lower()
            query =  que.check_beast_characters_beasts()
            beasts = cursor.execute(query, (beasts_nickname_lower, discord_tag)).fetchall()
            beasts_name = beasts[0][0]
            beasts_nickname = beasts[0][1]
            beasts_lvl = beasts[0][2]
            beasts_hp = beasts[0][3]
            beasts_str = beasts[0][4]
            beasts_def = beasts[0][5]
            beasts_spd = beasts[0][6]
            beasts_dex = beasts[0][7]
            cursor.close()
            return("""```monster name: ** """ + beasts_name + """ **
                \n** beasts name ** """ + beasts_nickname + """ **
                \n** level: """ + beasts_lvl + """ **
                \n*** Stats ***
                \n** hp: """ + beasts_hp + """ **
                \n** str: """ + beasts_str + """ **
                \n** def: """ + beasts_def + """ **
                \n** spd: """ + beasts_spd + """ **
                \n** dex: """ + beasts_dex + """ ** ```""")
        else:
            return('``` This account is not linked to this discord account. Please log into the proper account, or reach out to a moderator to switch accounts if you do not have access to that account. ```')


def level_up_pet(character_name, beasts_nickname, levels, discord_tag):
        if(calc.verify_account(character_name, discord_tag)):     
            if(calc.validate_fields(character_name) == True):
                beasts_nickname_lower = beasts_nickname.lower()
                sqliteConnection = sqlite3.connect('beasts.db')
                cursor = sqliteConnection.cursor()
                query = que.compare_beast_stats_characters_beasts()
                pet = cursor.execute(query, (beasts_nickname_lower,)).fetchall()
                pet_level = int(pet[0][0]) + int(levels)
                pet_current_hp = int(pet[0][1])
                pet_current_str = int(pet[0][2])
                pet_current_def = int(pet[0][3])
                pet_current_spd = int(pet[0][4])
                pet_current_dex = int(pet[0][5])
                pet_hp_growth = int(pet[0][6])
                pet_str_growth = int(pet[0][7])
                pet_def_growth = int(pet[0][8])
                pet_spd_growth = int(pet[0][9])
                pet_dex_growth = int(pet[0][10])
                pet_base_hp = int(pet[0][11])
                pet_base_str = int(pet[0][12])
                pet_base_def = int(pet[0][13])
                pet_base_spd = int(pet[0][14])
                pet_base_dex = int(pet[0][15])

                pet_new_level = str(pet_level)
                pet_new_hp = str(mat.floor(((pet_level / pet_hp_growth)  + pet_base_hp) / (((100 - pet_current_hp) / 100))))
                pet_new_str = str(mat.floor(((pet_level / pet_str_growth)  + pet_base_str) / (((100 - pet_current_str) / 100))))
                pet_new_def = str(mat.floor(((pet_level / pet_def_growth)  + pet_base_def) / (((100 - pet_current_def) / 100))))
                pet_new_spd = str(mat.floor(((pet_level / pet_spd_growth)  + pet_base_spd) / (((100 - pet_current_spd) / 100))))
                pet_new_dex = str(mat.floor(((pet_level / pet_dex_growth)  + pet_base_dex) / (((100 - pet_current_dex) / 100))))
                query = que.level_up_and_down_beast_characters_beasts()
                cursor.execute(query, (pet_new_level, pet_new_hp, pet_new_str, pet_new_def, pet_new_spd, 
                                       pet_new_dex, discord_tag, 
                                       beasts_nickname_lower))
                sqliteConnection.commit()
                cursor.close()
                sqliteConnection.close()
                return('```Your pet has leveled up! current level: ' + pet_new_level + ' hp: ' + pet_new_hp + ' str: ' + pet_new_str + ' def: ' + pet_new_def + ' spd: ' + pet_new_spd + ' dex: ' + pet_new_dex + '```')
            else:
                return('``` This account is not linked to this discord account. Please log into the proper account, or reach out to a moderator to switch accounts if you do not have access to that account. ```')

def level_down_pet(character_name, beasts_nickname, levels, discord_tag):
        if(calc.verify_account(character_name, discord_tag)):     
            if(calc.validate_fields(character_name) == True):
                beasts_nickname_lower = beasts_nickname.lower()
                sqliteConnection = sqlite3.connect('beasts.db')
                cursor = sqliteConnection.cursor()
                query = que.compare_beast_stats_characters_beasts()
                pet = cursor.execute(query, (beasts_nickname_lower,)).fetchall()
                pet_level = int(pet[0][0]) - int(levels)
                pet_current_hp = int(pet[0][1])
                pet_current_str = int(pet[0][2])
                pet_current_def = int(pet[0][3])
                pet_current_spd = int(pet[0][4])
                pet_current_dex = int(pet[0][5])
                pet_hp_growth = int(pet[0][6])
                pet_str_growth = int(pet[0][7])
                pet_def_growth = int(pet[0][8])
                pet_spd_growth = int(pet[0][9])
                pet_dex_growth = int(pet[0][10])
                pet_base_hp = int(pet[0][11])
                pet_base_str = int(pet[0][12])
                pet_base_def = int(pet[0][13])
                pet_base_spd = int(pet[0][14])
                pet_base_dex = int(pet[0][15])

                pet_new_level = str(pet_level)
                if(pet_level == 1):
                    pet_new_hp = str(pet_base_hp)
                    pet_new_str = str(pet_base_str)
                    pet_new_def = str(pet_base_def)
                    pet_new_spd = str(pet_base_spd)
                    pet_new_dex = str(pet_base_dex)  
                else:      
                    pet_new_hp = str(mat.floor(((pet_level / pet_hp_growth)  + pet_base_hp) / (((100 - pet_current_hp) / 100))))
                    pet_new_str = str(mat.floor(((pet_level / pet_str_growth)  + pet_base_str) / (((100 - pet_current_str) / 100))))
                    pet_new_def = str(mat.floor(((pet_level / pet_def_growth)  + pet_base_def) / (((100 - pet_current_def) / 100))))
                    pet_new_spd = str(mat.floor(((pet_level / pet_spd_growth)  + pet_base_spd) / (((100 - pet_current_spd) / 100))))
                    pet_new_dex = str(mat.floor(((pet_level / pet_dex_growth)  + pet_base_dex) / (((100 - pet_current_dex) / 100))))
                query = que.level_up_and_down_beast_characters_beasts()
                print(discord_tag)
                cursor.execute(query, (pet_new_level, pet_new_hp, pet_new_str, pet_new_def, pet_new_spd, 
                                       pet_new_dex, discord_tag, 
                                       beasts_nickname_lower))
                sqliteConnection.commit()
                cursor.close()
                sqliteConnection.close()
                return('```Your pet has leveled down! current level: ' + pet_new_level + ' hp: ' + pet_new_hp + ' str: ' + pet_new_str + ' def: ' + pet_new_def + ' spd: ' + pet_new_spd + ' dex: ' + pet_new_dex + '```')
            else:
                return('``` This account is not linked to this discord account. Please log into the proper account, or reach out to a moderator to switch accounts if you do not have access to that account. ```')
