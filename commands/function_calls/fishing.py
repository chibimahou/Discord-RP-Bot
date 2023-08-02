import random
import discord
import sqlite3
import os
import re
import math as mat
import function_calls.calc as calc
from discord.ext import commands
from discord import app_commands
from discord.utils import get

class fishing:
    def __init__(self):
         self.fishes_caught = ""
         
    def catch_fishing(self, character_name, location, discord_tag):
            if(calc.verify_account(character_name, discord_tag)):
                sqliteConnection = sqlite3.connect('equipment.db')
                sqliteConnection2 = sqlite3.connect('characterSheet.db')
                sqliteConnection3 = sqlite3.connect('mobspawn.db')
                cursor = sqliteConnection.cursor()
                cursor2 = sqliteConnection2.cursor()       
                cursor3 = sqliteConnection3.cursor()                 
                character_name_lower = character_name.lower()
                location_lower = location.lower()
                query = """SELECT 
                    proficiencySkills 
                    FROM 
                        charactersheets
                        WHERE 
                            nickname = ? 
                            AND 
                                discord_tag = ?;"""
                character_information = cursor2.execute(query, (character_name_lower, discord_tag)).fetchall()
                print(character_information[0][0])
                proficiency_skills = character_information[0][0].split(',')  
                print(proficiency_skills)              
                fishing_proficiency = calc.get_proficiency(proficiency_skills, 'fishing')
                query3 = """SELECT
                    area
                    FROM
                        location
                        WHERE area = ?;"""
                map = cursor3.execute(query3, (location_lower,)).fetchall()
                area = str(map[0][0])
                print(area)
                query2 = """SELECT 
                    name, difficulty
                    FROM 
                        fishdb
                        WHERE
                            location = ?
                            AND
                                difficulty <= ?
                                ORDER BY
                                    RANDOM() """
                fish = cursor.execute(query2, (area, int(fishing_proficiency[1]))).fetchall()
                chance_to_catch = random.randint(1, 100)
                fish_escape_value = random.randint(1, 100)
                print(fish[0][1])            
                print(fishing_proficiency[1])            
                if(chance_to_catch + (int(fishing_proficiency[1]) - int(fish[0][1])) > fish_escape_value):
                    self.fishes_caught = self.fishes_caught + fish[0][0]
                    print("Caught fish: " + self.fishes_caught)
                    results = "Success! You have caught a: " + fish[0][0] + "!"
                else:
                    results = "The fish got away!"

                cursor.close()
                cursor2.close()      
                cursor3.close()  
                sqliteConnection.close()     
                sqliteConnection2.close()        
                sqliteConnection3.close()        
    
                return('```' + results + '```')
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


    def check_fish(location):
            location_lower = location.lower()
            sqliteConnection = sqlite3.connect('equipment.db')
            cursor = sqliteConnection.cursor()
            query = """SELECT 
                    * 
                    FROM 
                        fishdb
                        WHERE
                            location = ?;"""
            fish_in_area = cursor.execute(query, (location_lower,)).fetchall()
            print(str(fish_in_area))
            return("fish in " + location_lower + ": " + str(fish_in_area))

        
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
            height_escape_characters = height.replace('\'', '.')
            height_escape_characters2 = height_escape_characters.replace('\"', '..')
            print(str(height_escape_characters2))
            character_information = cursor.execute("INSERT INTO charactersheets(firstName, lastName, nickname, height, size, age, birthday, playerStatus, guild, class, skillList, uniqueSkills, equipment, proficiencySkills, playerColor, inventory, bio, col, experience, level, str, def, spd, dex, discord_tag) VALUES ('" + first_name + "','" + last_name + "','" + ingame_name_lower + "','" + height_escape_characters2 + "','" + physique + "','" + age + "','" + birthday + "','normal','guild','class','','unique skills','bronze one handed sword', 'one handed sword:1', 'green', 'herb:1,bronze one handed sword:1','" + bio + "','100','0','" + level + "','5','5','5','5'" + ", '" + str(discord_tag) + "')")
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
