import discord
import sqlite3
import os
import re
import function_calls.calc as calc
from discord.ext import commands
from discord import app_commands
from discord.utils import get

def add_character_to_server(first_name, last_name, ingame_name, height, physique,  age, birthday, bio, level, skillList, inventory, guild, character_class, player_color, unique_skills, proficiency_skills, col, experience, strength, defense, speed, dexterity, player_status):
    if(calc.validate_fields(first_name) == True and  calc.validate_fields(last_name) == True and  calc.validate_fields(ingame_name) == True and  calc.validate_fields_commas(height) == True and  calc.validate_fields(physique) == True and  calc.validate_fields(age) == True and  calc.validate_fields_commas(birthday) == True and  calc.validate_fields(bio) == True and  calc.validate_fields(level) == True):
        sqliteConnection = sqlite3.connect('characterSheet.db')
        cursor = sqliteConnection.cursor()
        ingame_name_lower = ingame_name.lower()
        height_escape_characters_1 = height.replace('\'', '.')
        height_escape_characters_2 = height_escape_characters_1.replace('\"', '..')
        print(height_escape_characters_1, height_escape_characters_2)
        character_information = cursor.execute("INSERT INTO charactersheets(firstName, lastName, nickname, height, size, age, birthday, playerStatus, guild, class, skillList, uniqueSkills, currentWeaponEquipped, proficiencySkills, playerColor, inventory, bio, col, experience, level, str, def, spd, dex) VALUES ('" + first_name + "','" + last_name + "','" + ingame_name_lower + "','" + height_escape_characters_2 + "','" + physique + "','" + age + "','" + birthday + "','" + player_status + "', '" + guild + "', '" + character_class + "', '" + skillList + "', '" + unique_skills + "', 'None', '" + proficiency_skills + "', '" + player_color + "', '" + inventory + "','" + bio + "', '" + col + "', '" + experience + "', '" + level + "', '" + strength + "', '" + speed + "', '" + defense + "', '" + dexterity + "'" + ")")    
        sqliteConnection.commit()
        cursor.close()

        return('``` Character: ' + ingame_name_lower + ' was created. Welcome to Sword Art Online!```')
    return('``` You have input an invalid character```')

def update_character_in_server(character_name, field_to_update, updated_value):
    if(calc.validate_fields(field_to_update) and calc.validate_fields(updated_value)):
        sqliteConnection = sqlite3.connect('characterSheet.db')
        cursor = sqliteConnection.cursor()
        field_to_update_lower = field_to_update.lower()
        updated_value_lower = updated_value.lower()
        character_name_lower = character_name.lower()
        character_information = cursor.execute("UPDATE charactersheets SET " + field_to_update + " = " + updated_value + " WHERE nickname = " + character_name_lower + ";")    
        sqliteConnection.commit()
        cursor.close()

        return('``` Character: ' + character_name_lower + ' had the field: ' + field_to_update_lower + ' updated to: ' + updated_value_lower + '.```')
    return('``` You have input an invalid character```')

def remove_character_from_server(ingame_name):
    if(calc.validate_fields(ingame_name) == True):
        sqliteConnection = sqlite3.connect('characterSheet.db')
        cursor = sqliteConnection.cursor()
        ingame_name_lower = ingame_name.lower()
        character_information = cursor.execute("DELETE FROM charactersheets WHERE nickname = '" + ingame_name_lower + "';")
        sqliteConnection.commit()
        cursor.close()

        return('``` Character: ' + ingame_name_lower + ' was deleted from SAO.```')

def add_item_to_server(item_catagory, item_name, item_description, item_rarity, dropped_by):
        sqliteConnection = sqlite3.connect('characterSheet.db')
        cursor = sqliteConnection.cursor()
        item_catagory_lower = item_catagory.lower()
        item_name_lower = item_name.lower()
        item_description_lower = item_description.lower()
        item_rarity_lower = item_rarity.lower()
        dropped_by_lower = dropped_by.lower()
        character_information = cursor.execute("INSERT INTO items(catagory, item, item_description, rarity, droppedBy) VALUES ('" + item_catagory_lower + "','" + item_name_lower + "','" + item_description_lower + "','" + item_rarity_lower + "','" + dropped_by_lower + "'" + ")")    
        sqliteConnection.commit()
        cursor.close()
        return('``` Item:: ' + item_name + ' has been added to the game.```')

def update_item_in_server(character_name, field_to_update, updated_value):
    if(calc.validate_fields(field_to_update) and calc.validate_fields(updated_value)):
        sqliteConnection = sqlite3.connect('characterSheet.db')
        cursor = sqliteConnection.cursor()
        field_to_update_lower = field_to_update.lower()
        updated_value_lower = updated_value.lower()
        character_name_lower = character_name.lower()
        character_information = cursor.execute("UPDATE charactersheets SET " + field_to_update + " = '" + updated_value + "';")    
        sqliteConnection.commit()
        cursor.close()

        return('``` Character: ' + character_name_lower + ' had the field: ' + field_to_update_lower + ' updated to: ' + updated_value_lower + '.```')
    return('``` You have input an invalid character```')

def remove_item_from_server(item_catagory, item_name, item_description, item_rarity, dropped_by):
        sqliteConnection = sqlite3.connect('characterSheet.db')
        cursor = sqliteConnection.cursor()
        item_catagory_lower = item_catagory.lower()
        item_name_lower = item_name.lower()
        item_description_lower = item_description.lower()
        item_rarity_lower = item_rarity.lower()
        dropped_by_lower = dropped_by.lower()
        character_information = cursor.execute("DELETE FROM items WHERE item = '" + item_name_lower + "';")
        sqliteConnection.commit()
        cursor.close()
        return('``` Item:: ' + item_name + ' has been removed to the game.```')

def add_weapon_to_server(weapon_name, weapon_description, weapon_rarity, how_to_obtain, base_power, additional_effects, crit_chance, weapon_material, weapon_attack_type, catagory):
        sqliteConnection = sqlite3.connect('characterSheet.db')
        cursor = sqliteConnection.cursor()
        weapon_name_lower = weapon_name.lower()
        weapon_description_lower = weapon_description.lower()
        weapon_rarity_lower = weapon_rarity.lower()
        character_information = cursor.execute("INSERT INTO weapons(weapon_name, weapon_description, weapon_rarity, how_to_obtain, base_power, additional_effects, crit_chance, weapon_material, weapon_attack_type, catagory) VALUES ('" + str(weapon_name_lower) + "','" + str(weapon_description) + "','" + str(weapon_rarity_lower) + "','" + str(how_to_obtain) + "','" + str(base_power) + "','" + str(additional_effects) + "','" + str(crit_chance) + "','" + str(weapon_material) + "','" + str(weapon_attack_type) + "','" + str(catagory) + "')")     
        sqliteConnection.commit()
        cursor.close()
        return('``` Weapon: ' + weapon_name + ' has been added to the game.```')

def remove_weapon_from_server(weapon_name):
        sqliteConnection = sqlite3.connect('characterSheet.db')
        cursor = sqliteConnection.cursor()
        weapon_name_lower = weapon_name.lower()
        character_information = cursor.execute("DELETE FROM weapons WHERE item = '" + weapon_name_lower + "';")
        sqliteConnection.commit()
        cursor.close()
        return('``` Weapon: ' + weapon_name + ' has been removed to the game.```')
        
def add_proficiency_skill_to_server(skill_name, skill_description, skill_effects, skill_type):
        sqliteConnection = sqlite3.connect('characterSheet.db')
        cursor = sqliteConnection.cursor()
        skill_name_lower = skill_name.lower()
        skill_type_lower = skill_type.lower()
        character_information = cursor.execute("INSERT INTO proficiency_skills(skill_name, skill_description, skill_effects, skill_type) VALUES ('" + skill_name_lower + "','" + skill_description + "','" + skill_effects + "','" + skill_type_lower + "')")    
        sqliteConnection.commit()
        cursor.close()
        return('``` Item:: ' + skill_name + ' has been added to the game.```')

def remove_proficiency_skill_from_server(skill_name):
        sqliteConnection = sqlite3.connect('characterSheet.db')
        cursor = sqliteConnection.cursor()
        skill_name_lower = skill_name.lower()
        character_information = cursor.execute("DELETE FROM proficiency_skills WHERE skill_name = '" + skill_name_lower + "';")
        sqliteConnection.commit()
        cursor.close()
        return('``` Proficiency skill: ' + skill_name_lower + ' has been removed to the game.```')

def add_unique_skill_to_server(item_catagory, item_name, item_description, item_rarity, dropped_by):
        sqliteConnection = sqlite3.connect('characterSheet.db')
        cursor = sqliteConnection.cursor()
        item_catagory_lower = item_catagory.lower()
        item_name_lower = item_name.lower()
        item_description_lower = item_description.lower()
        item_rarity_lower = item_rarity.lower()
        dropped_by_lower = dropped_by.lower()
        character_information = cursor.execute("DELETE FROM items(catagory, item, item_description, rarity, droppedBy) VALUES ('" + item_catagory_lower + "','" + item_name_lower + "','" + item_description_lower + "','" + item_rarity_lower + "','" + dropped_by_lower + "'" + ")")    
        sqliteConnection.commit()
        cursor.close()
        return('``` Item:: ' + item_name + ' has been added to the game.```')

def remove_unique_skill_from_server(item_catagory, item_name, item_description, item_rarity, dropped_by):
        sqliteConnection = sqlite3.connect('characterSheet.db')
        cursor = sqliteConnection.cursor()
        item_catagory_lower = item_catagory.lower()
        item_name_lower = item_name.lower()
        item_description_lower = item_description.lower()
        item_rarity_lower = item_rarity.lower()
        dropped_by_lower = dropped_by.lower()
        character_information = cursor.execute("DELETE FROM items WHERE item = '" + item_name_lower + "';")
        sqliteConnection.commit()
        cursor.close()
        return('``` Item:: ' + item_name + ' has been removed to the game.```')

def add_mobs_to_server(item_catagory, item_name, item_description, item_rarity, dropped_by):
        sqliteConnection = sqlite3.connect('characterSheet.db')
        cursor = sqliteConnection.cursor()
        item_catagory_lower = item_catagory.lower()
        item_name_lower = item_name.lower()
        item_description_lower = item_description.lower()
        item_rarity_lower = item_rarity.lower()
        dropped_by_lower = dropped_by.lower()
        character_information = cursor.execute("DELETE FROM items(catagory, item, item_description, rarity, droppedBy) VALUES ('" + item_catagory_lower + "','" + item_name_lower + "','" + item_description_lower + "','" + item_rarity_lower + "','" + dropped_by_lower + "'" + ")")    
        sqliteConnection.commit()
        cursor.close()
        return('``` Item:: ' + item_name + ' has been added to the game.```')

def remove_mobs_from_server(item_catagory, item_name, item_description, item_rarity, dropped_by):
        sqliteConnection = sqlite3.connect('characterSheet.db')
        cursor = sqliteConnection.cursor()
        item_catagory_lower = item_catagory.lower()
        item_name_lower = item_name.lower()
        item_description_lower = item_description.lower()
        item_rarity_lower = item_rarity.lower()
        dropped_by_lower = dropped_by.lower()
        character_information = cursor.execute("DELETE FROM items WHERE item = '" + item_name_lower + "';")
        sqliteConnection.commit()
        cursor.close()
        return('``` Item:: ' + item_name + ' has been removed to the game.```')

def add_locations_to_server(name, type, rarity, drops, mob_description, floor, area):
        sqliteConnection = sqlite3.connect('characterSheet.db')
        cursor = sqliteConnection.cursor()
        name_lower = name.lower()
        type_lower = type.lower()
        rarity_lower = rarity.lower()
        drops_lower = drops.lower()
        area_lower = area.lower()
        character_information = cursor.execute("INSERT INTO mobs(name, type, rarity, drops) VALUES ('" + name_lower + "','" + type_lower + "','" + rarity_lower + "','" + drops_lower + "')")    
        sqliteConnection.commit()
        character_information = cursor.execute("INSERT INTO mob_descriptions(name, mob_description) VALUES ('" + name_lower + "','" + mob_description + "')")    
        sqliteConnection.commit() 
        character_information = cursor.execute("SELECT floor, area, spawns FROM Location WHERE floor = '" + floor + "' AND area = '" + area_lower + "'")    
        if len(character_information) != 0:
            spawns = calc.remove_white_spaces_around_commas(character_information[0][2])
            new_spawns = ""
            temp = 0
            for temp in range(len(character_information)):
                if temp < len(character_information) - 1:
                    new_spawns = str(new_spawns) + str(spawns[temp]) + ','
                else:
                    new_spawns = str(new_spawns) + str(name_lower)
            character_information = cursor.execute("UPDATE charactersheets SET spawns = '" + new_spawns + "';")    
        else:
            return('```area is not valid. ```')
        cursor.close()
        return('``` mob: ' + name + ' has been added to the game.```')

def remove_locations_from_server(item_catagory, item_name, item_description, item_rarity, dropped_by):
        sqliteConnection = sqlite3.connect('characterSheet.db')
        cursor = sqliteConnection.cursor()
        item_catagory_lower = item_catagory.lower()
        item_name_lower = item_name.lower()
        item_description_lower = item_description.lower()
        item_rarity_lower = item_rarity.lower()
        dropped_by_lower = dropped_by.lower()
        character_information = cursor.execute("DELETE FROM items WHERE item = '" + item_name_lower + "';")
        sqliteConnection.commit()
        cursor.close()
        return('``` Item:: ' + item_name + ' has been removed to the game.```')

def remove_character(ingame_name):
    if(calc.validate_fields(ingame_name) == True):
        sqliteConnection = sqlite3.connect('characterSheet.db')
        cursor = sqliteConnection.cursor()
        ingame_name_lower = ingame_name.lower()
        character_information = cursor.execute("DELETE FROM charactersheets WHERE nickname = '" + ingame_name_lower + "';")
        sqliteConnection.commit()
        cursor.close()

        return('``` Character: ' + ingame_name_lower + ' was deleted from SAO.```')

