import discord
import sqlite3
import os
import re
import function_calls.calc as calc
from discord.ext import commands
from discord import app_commands
from discord.utils import get

def add_experience(character_name, experience_to_add):
    if(calc.validate_fields(character_name) == True and  calc.validate_fields(experience_to_add) == True):
        sqliteConnection = sqlite3.connect('characterSheet.db')
        cursor = sqliteConnection.cursor()
        character_current_experience = cursor.execute("SELECT experience, level FROM charactersheets WHERE nickname = '" + character_name + "'").fetchall()
        experience = str(int(experience_to_add) + character_current_experience[0][0])
        level = character_current_experience[0][1]
        cursor.execute("UPDATE charactersheets SET experience = '" + experience + "' WHERE nickname = '" + character_name + "'").fetchall()
        sqliteConnection.commit()
        character_information = cursor.execute("SELECT charactersheets.level, charactersheets.experience, experience.experience FROM charactersheets INNER JOIN experience ON charactersheets.level = experience.level WHERE charactersheets.nickname = '" + character_name + "';").fetchall()
        print(str(character_information[0][1]) + " " + str(character_information[0][2]))
        if character_information[0][1] >= character_information[0][2]:
           level = str(level + 1)
           cursor.execute("UPDATE charactersheets SET level = '" + level + "' WHERE nickname = '" + character_name + "'").fetchall()
           sqliteConnection.commit()
           character_information = cursor.execute("SELECT charactersheets.level, charactersheets.experience, experience.experience FROM charactersheets INNER JOIN experience ON charactersheets.level = experience.level WHERE charactersheets.nickname = '" + character_name + "';").fetchall()
           new_level = str(level)
           character_experience_to_level = str(character_information[0][2] - character_information[0][1])
           return('```' + 'Congratulations, You leveled up! Your current level is: ' + new_level + '. You need ' + character_experience_to_level + ' experience to level up.```')

        else:
           character_level = str(character_information[0][0])
           character_experience_to_level = str(character_information[0][2] - character_information[0][1])
        return('```' + 'Your current level is: ' + character_level + '. You need ' + character_experience_to_level + ' experience to level up.```')
    else:
        return('```You input an invalid character. Please do not use special characters. ```')

def remove_experience(character_name, experience_to_remove):
    if(calc.validate_fields(character_name) == True and  calc.validate_fields(experience_to_remove) == True):
        sqliteConnection = sqlite3.connect('characterSheet.db')
        cursor = sqliteConnection.cursor()
        character_current_experience = cursor.execute("SELECT experience, level FROM charactersheets WHERE nickname = '" + character_name + "'").fetchall()
        experience = str(character_current_experience[0][0] - int(experience_to_remove))
        level = character_current_experience[0][1]
        last_level = str(character_current_experience[0][1] - 1)
        print("experience: " + str(experience) + " level: " + str(level) + " last level: " + str(last_level))
        cursor.execute("UPDATE charactersheets SET experience = '" + experience + "' WHERE nickname = '" + character_name + "'").fetchall()
        sqliteConnection.commit()
        character_information = cursor.execute("SELECT charactersheets.level, charactersheets.experience, experience.experience FROM charactersheets INNER JOIN experience ON charactersheets.level = experience.level WHERE nickname = '" + character_name + "';").fetchall()
        character_previous_level = cursor.execute("SELECT experience FROM experience WHERE level = " + last_level + "").fetchall()
        experience_to_level = character_previous_level[0][0]
        print("experience to level: " + str(experience_to_level) + "character_experience: " + str(character_information[0][1]))

        if character_information[0][1] < experience_to_level:
           level = str(level - 1)
           cursor.execute("UPDATE charactersheets SET level = '" + level + "' WHERE nickname = '" + character_name + "'").fetchall()
           sqliteConnection.commit()
           character_information = cursor.execute("SELECT charactersheets.level, charactersheets.experience, experience.experience FROM charactersheets INNER JOIN experience ON charactersheets.level = experience.level WHERE nickname = '" + character_name + "';").fetchall()
           new_level = str(level)
           character_experience_to_level = str(character_information[0][2] - character_information[0][1])
           print(str(character_information[0][2]) + " " + str(character_information[0][1]))
           print("new level: " + str(new_level) + " level: " + str(level) + " experience to level: " + str(character_experience_to_level))

           return('```' + 'Your level has been reduced. Your current level is: ' + new_level + '. You need ' + character_experience_to_level + ' experience to level up.```')
        else:
            character_level = str(character_information[0][0])
            character_experience_to_level = str(character_information[0][2] - character_information[0][1])
            return('```' + 'Your current level is: ' + character_level + '. You need ' + character_experience_to_level + ' experience to level up.```')
    else:
        return('```You input an invalid character. Please do not use special characters. ```')

def experience(character_name):
    if(calc.validate_fields(character_name) == True):
        sqliteConnection = sqlite3.connect('characterSheet.db')
        cursor = sqliteConnection.cursor()
        character_information = cursor.execute("SELECT charactersheets.level, charactersheets.experience, experience.experience FROM charactersheets INNER JOIN experience ON charactersheets.level = experience.level WHERE charactersheets.nickname = '" + character_name + "';").fetchall()
        character_level = str(character_information[0][0])
        character_experience_to_level = str(character_information[0][2] - character_information[0][1])

        return('```' + 'Your current level is: ' + character_level + '. You need ' + character_experience_to_level + ' experience to level up.```')
    else:
        return('```You input an invalid character. Please do not use special characters. ```')

