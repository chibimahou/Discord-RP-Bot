import discord
import sqlite3
import os
import re
import math as mat
import function_calls.calc as calc
from discord.ext import commands
from discord import app_commands
from discord.utils import get

def add_stats(character_name, stat, points_to_add, discord_tag):
        if(calc.verify_account(character_name, discord_tag)):
            sqliteConnection = sqlite3.connect('characterSheet.db')
            cursor = sqliteConnection.cursor()
            stat_lower = stat.lower()
            character_name_lower = character_name.lower()
            character_current_stat = cursor.execute("SELECT " + stat_lower + " FROM charactersheets WHERE nickname = '" + character_name_lower + "';").fetchall()
            print('prev stat: ' + str(character_current_stat[0][0]) + ' points_to_add: ' + str(points_to_add))
            new_stat = str(character_current_stat[0][0] + int(points_to_add))
            cursor.execute("UPDATE charactersheets SET " + stat_lower + " = '" + new_stat + "' WHERE nickname = '" + character_name_lower + "';").fetchall()
            sqliteConnection.commit()
            cursor.close()      
            return('```' + 'Your new ' + stat_lower + ' is: ' + new_stat + '.```')
        else:
            return('``` This account is not linked to this discord account. Please log into the proper account, or reach out to a moderator to switch accounts if you do not have access to that account. ```')

def remove_stats(character_name, stat, points_to_remove, discord_tag):
        if(calc.verify_account(character_name, discord_tag)):         
            sqliteConnection = sqlite3.connect('characterSheet.db')
            cursor = sqliteConnection.cursor()
            stat_lower = stat.lower()
            character_name_lower = character_name.lower()
            character_current_stat = cursor.execute("SELECT " + stat_lower + " FROM charactersheets WHERE nickname = '" + character_name_lower + "'").fetchall()
            previous_stat = character_current_stat[0][0]
            print('prev stat: ' + str(previous_stat) + ' points_to_remove: ' + str(points_to_remove))

            new_stat = str(previous_stat - int(points_to_remove))
            cursor.execute("UPDATE charactersheets SET " + stat_lower + " = '" + new_stat + "' WHERE nickname = '" + character_name_lower + "'").fetchall()
            sqliteConnection.commit()
            cursor.close()

            return('```' + 'Your new ' + stat_lower + ' is: ' + new_stat + '.```')
        else:
            return('``` This account is not linked to this discord account. Please log into the proper account, or reach out to a moderator to switch accounts if you do not have access to that account. ```')


def check_character(character_name, discord_tag):
        if(calc.verify_account(character_name, discord_tag)):     
            if(calc.validate_fields(character_name) == True):
                sqliteConnection = sqlite3.connect('characterSheet.db')
                cursor = sqliteConnection.cursor()
                character_information = cursor.execute("SELECT firstName, lastName, height, size, age, skillList, inventory, bio, guild, class, playerColor, birthday, nickname, uniqueSkills, proficiencySkills, equipment, col, experience, level, str, def, spd, playerStatus, dex FROM charactersheets WHERE nickname = '" + character_name.lower() + "'").fetchall()
                first_name = str(character_information[0][0])
                last_name = str(character_information[0][1])
                height = str(character_information[0][2])
                size = str(character_information[0][3])
                age = str(character_information[0][4])
                skill_list = str(character_information[0][5])
                inventory = str(character_information[0][6])
                bio = str(character_information[0][7])
                guild = str(character_information[0][8])
                player_class = str(character_information[0][9])
                player_color = str(character_information[0][10])
                birthday = str(character_information[0][11])
                nickname = str(character_information[0][12])
                unique_skills = str(character_information[0][13])
                proficiency_skills = str(character_information[0][14])
                current_weapon = str(character_information[0][15])
                col = str(character_information[0][16])
                exp = str(character_information[0][17])
                level = str(character_information[0][18])
                strength = str(character_information[0][19])
                defense = str(character_information[0][20])
                speed = str(character_information[0][21])
                player_status = str(character_information[0][22])
                dex = str(character_information[0][23])
                height_escape_characters_2 = height.replace('..', '\"')
                height_escape_characters_1 = height_escape_characters_2.replace('.', '\'')

                cursor.close()
                return("""```real name:                    ** """ + first_name + """ """ + last_name + """ **\nheight:                       ** """ + height_escape_characters_1 + """ **
                \nsize:                         ** """ + size  + """ **\nage:                          ** """ + age + """ **\nbirthday:                     ** """ + birthday + """ **\nbio:                          ** """ + bio + """ **
                \nusername:                     ** """ + nickname + """ **                            cursor color: ** """ + player_color + """ **
                \nlevel:                        ** """ + level + """ **\nexperience:                   ** """ +  exp + """ **\nstr: ** """ + strength + """ ** def: ** """ + defense + """ **spd: ** """ + speed + """ **  dex: ** """ + dex + """ **                   col: ** """ + col +  """ **
                \nclass:                        ** """ + player_class + """ **
                \ncurrently equipped weapon:    ** """ + current_weapon + """ **\nstatus:                       ** """ + player_status + """ **
                \nguild:                        ** """ + guild + """ **\nsword arts:\n\n** """ + skill_list + """ **\n\nunique skills:\n\n** """ +  unique_skills + """**
                \nProficiency Skills:\n\n** """ + proficiency_skills + """ **\n\ninventory:\n\n** """ + inventory + """ **```""")
        else:
            return('``` This account is not linked to this discord account. Please log into the proper account, or reach out to a moderator to switch accounts if you do not have access to that account. ```')

def add_character(first_name, last_name, ingame_name, height, physique,  age, birthday, bio, level, discord_tag):
    if(calc.validate_fields(first_name) == True and  calc.validate_fields(last_name) == True and  calc.validate_fields(ingame_name) == True and  calc.validate_fields_commas(height) == True and  calc.validate_fields(physique) == True and  calc.validate_fields(age) == True and  calc.validate_fields_commas(birthday) == True and  calc.validate_fields_commas(bio) == True and  calc.validate_fields(level) == True):
        sqliteConnection = sqlite3.connect('characterSheet.db')
        cursor = sqliteConnection.cursor()
        ingame_name_lower = ingame_name.lower()
        values = [first_name.lower(), last_name.lower(), ingame_name_lower, str(discord_tag)]
        unique_key = calc.generate_key(values)
        height_escape_characters = height.replace('\'', '.')
        height_escape_characters2 = height_escape_characters.replace('\"', '..')
        print(unique_key)
        character_information = cursor.execute("INSERT INTO charactersheets(firstName, lastName, nickname, height, size, age, birthday, playerStatus, guild, class, skillList, uniqueSkills, equipment, proficiencySkills, playerColor, inventory, bio, col, experience, level, str, def, spd, dex, discord_tag, unique_key, party_id) VALUES ('" + first_name + "','" + last_name + "','" + ingame_name_lower + "','" + height_escape_characters2 + "','" + physique + "','" + age + "','" + birthday + "','normal','guild','class','','unique skills','bronze one handed sword', 'one handed sword:1', 'green', 'herb:1,bronze one handed sword:1','" + bio + "','100','0','" + level + "','5','5','5','5'" + ", '" + str(discord_tag) + "', '" + unique_key + "', '\"\"')")
        sqliteConnection.commit()
        cursor.close()

        return('``` Character: ' + ingame_name_lower + ' was created. Welcome to Sword Art Online!```')

def stat_screen(character_name):
    if(calc.validate_fields(character_name) == True):
        sqliteConnection = sqlite3.connect('characterSheet.db')
        cursor = sqliteConnection.cursor()
        character_information = cursor.execute("SELECT str, def, spd, dex FROM charactersheets WHERE nickname = '" + character_name + "'").fetchall()
        cursor.close()
        return('```str: ' + str(character_information[0][0]) + '\ndef: ' + str(character_information[0][1]) + '\nspd: ' + str(character_information[0][2]) + '\ndex: ' + str(character_information[0][3]) + '```')
