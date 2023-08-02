import discord
import sqlite3
import os
import re
import function_calls.calc as calc
import function_calls.query.query as que
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
        sqliteConnection = sqlite3.connect('equipment.db')
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
        sqliteConnection = sqlite3.connect('equipment.db')
        cursor = sqliteConnection.cursor()
        field_to_update_lower = field_to_update.lower()
        updated_value_lower = updated_value.lower()
        character_name_lower = character_name.lower()
        character_information = cursor.execute("UPDATE items SET " + field_to_update + " = '" + updated_value + "';")    
        sqliteConnection.commit()
        cursor.close()

        return('``` Character: ' + character_name_lower + ' had the field: ' + field_to_update_lower + ' updated to: ' + updated_value_lower + '.```')
    return('``` You have input an invalid character```')

def remove_item_from_server(item_catagory, item_name, item_description, item_rarity, dropped_by):
        sqliteConnection = sqlite3.connect('equipment.db')
        cursor = sqliteConnection.cursor()
        item_catagory_lower = item_catagory.lower()
        item_name_lower = item_name.lower()
        item_description_lower = item_description.lower()
        item_rarity_lower = item_rarity.lower()
        dropped_by_lower = dropped_by.lower()
        character_information = cursor.execute("DELETE FROM items WHERE item = '" + item_name_lower + "';")
        sqliteConnection.commit()
        cursor.close()
        return('``` Item:: ' + item_name_lower + ' has been removed to the game.```')

def add_weapon_to_server(weapon_name, weapon_description, weapon_rarity, how_to_obtain, base_power, additional_effects, crit_chance, weapon_material, weapon_attack_type, catagory):
        sqliteConnection = sqlite3.connect('equipment.db')
        cursor = sqliteConnection.cursor()
        weapon_name_lower = weapon_name.lower()
        weapon_description_lower = weapon_description.lower()
        weapon_rarity_lower = weapon_rarity.lower()
        character_information = cursor.execute("INSERT INTO weapons(weapon_name, weapon_description, weapon_rarity, how_to_obtain, base_power, additional_effects, crit_chance, weapon_material, weapon_attack_type, catagory) VALUES ('" + str(weapon_name_lower) + "','" + str(weapon_description) + "','" + str(weapon_rarity_lower) + "','" + str(how_to_obtain) + "','" + str(base_power) + "','" + str(additional_effects) + "','" + str(crit_chance) + "','" + str(weapon_material) + "','" + str(weapon_attack_type) + "','" + str(catagory) + "')")     
        sqliteConnection.commit()
        cursor.close()
        return('``` Weapon: ' + weapon_name_lower + ' has been added to the game.```')

def remove_weapon_from_server(weapon_name):
        sqliteConnection = sqlite3.connect('equipment.db')
        cursor = sqliteConnection.cursor()
        weapon_name_lower = weapon_name.lower()
        character_information = cursor.execute("DELETE FROM weapons WHERE weapon_name = '" + weapon_name_lower + "';")
        sqliteConnection.commit()
        cursor.close()
        return('``` Weapon: ' + weapon_name_lower + ' has been removed to the game.```')
        
def add_armor_to_server(armor_name, armor_description, armor_rarity, how_to_obtain, base_defense, additional_effects, armor_material, catagory):
        sqliteConnection = sqlite3.connect('equipment.db')
        cursor = sqliteConnection.cursor()
        armor_name_lower = armor_name.lower()
        armor_description_lower = armor_description.lower()
        armor_rarity_lower = armor_rarity.lower()
        character_information = cursor.execute("""INSERT INTO 
                                                        armor
                                                                (armor_name, armor_description, 
                                                                armor_rarity, how_to_obtain, 
                                                                base_defense, additional_effects, 
                                                                armor_material, catagory) 
                                                                VALUES 
                                                                        ('""" + str(armor_name_lower) + """','""" + 
                                                                        str(armor_description_lower) + """','""" +
                                                                        str(armor_rarity_lower) + """','""" + 
                                                                        str(how_to_obtain) + """','""" + 
                                                                        str(base_defense) + """','""" +                                                                         
                                                                        str(additional_effects) + """','""" + 
                                                                        str(armor_material) + """','""" + 
                                                                        str(catagory) + """')""")     
        sqliteConnection.commit()
        cursor.close()
        return('``` armor: ' + armor_name_lower + ' has been added to the game.```')

def remove_armor_from_server(armor_name):
        sqliteConnection = sqlite3.connect('equipment.db')
        cursor = sqliteConnection.cursor()
        armor_name_lower = armor_name.lower()
        character_information = cursor.execute("DELETE FROM armor WHERE armor_name = '" + armor_name_lower + "';")
        sqliteConnection.commit()
        cursor.close()
        return('``` armor: ' + armor_name_lower + ' has been removed to the game.```')

def add_blacksmithing_material_to_server(material_name, material_description, material_rarity, how_to_obtain, location, difficulty, processing_type, processed_into, catagory):
        sqliteConnection = sqlite3.connect('equipment.db')
        cursor = sqliteConnection.cursor()
        material_name_lower = material_name.lower()
        material_description_lower = material_description.lower()
        material_rarity_lower = material_rarity.lower()
        how_to_obtain_lower = how_to_obtain.lower()
        location_lower = location.lower()
        processing_type_lower = processing_type.lower()
        processed_into_lower = processed_into.lower()
        catagory_lower = catagory.lower()
        query = que.add_blacksmithing_material_to_server_equipment()
        cursor.execute(query, (material_name_lower, material_description_lower,
                               material_rarity_lower, how_to_obtain_lower, location_lower,
                               difficulty, processing_type_lower, processed_into_lower,
                               catagory_lower))   
        sqliteConnection.commit()
        cursor.close()
        sqliteConnection.close()
        return('``` material: ' + material_name_lower + ' has been added to the game.```')

def remove_blacksmithing_material_from_server(material_name):
        sqliteConnection = sqlite3.connect('equipment.db')
        cursor = sqliteConnection.cursor()
        material_name_lower = material_name.lower()
        query = que.remove_blacksmithing_material_from_server_equipment()
        cursor.execute(query, (material_name_lower))
        sqliteConnection.commit()
        cursor.close()
        return('``` material: ' + material_name_lower + ' has been removed to the game.```')
             
def add_proficiency_skill_to_server(skill_name, skill_description, skill_effects, skill_type):
        sqliteConnection = sqlite3.connect('equipment.db')
        cursor = sqliteConnection.cursor()
        skill_name_lower = skill_name.lower()
        skill_type_lower = skill_type.lower()
        character_information = cursor.execute("INSERT INTO proficiency_skills(skill_name, skill_description, skill_effects, skill_type) VALUES ('" + skill_name_lower + "','" + skill_description + "','" + skill_effects + "','" + skill_type_lower + "')")    
        sqliteConnection.commit()
        cursor.close()
        return('``` Item:: ' + skill_name_lower + ' has been added to the game.```')

def remove_proficiency_skill_from_server(skill_name):
        sqliteConnection = sqlite3.connect('equipment.db')
        cursor = sqliteConnection.cursor()
        skill_name_lower = skill_name.lower()
        character_information = cursor.execute("DELETE FROM proficiency_skills WHERE skill_name = '" + skill_name_lower + "';")
        sqliteConnection.commit()
        cursor.close()
        return('``` Proficiency skill: ' + skill_name_lower + ' has been removed to the game.```')

def add_unique_skill_to_server(item_catagory, item_name, item_description, item_rarity, dropped_by):
        sqliteConnection = sqlite3.connect('equipment.db')
        cursor = sqliteConnection.cursor()
        item_catagory_lower = item_catagory.lower()
        item_name_lower = item_name.lower()
        item_description_lower = item_description.lower()
        item_rarity_lower = item_rarity.lower()
        dropped_by_lower = dropped_by.lower()
        character_information = cursor.execute("DELETE FROM unique_skills(catagory, item, item_description, rarity, droppedBy) VALUES ('" + item_catagory_lower + "','" + item_name_lower + "','" + item_description_lower + "','" + item_rarity_lower + "','" + dropped_by_lower + "'" + ")")    
        sqliteConnection.commit()
        cursor.close()
        return('``` Item:: ' + item_name + ' has been added to the game.```')

def remove_unique_skill_from_server(item_catagory, item_name, item_description, item_rarity, dropped_by):
        sqliteConnection = sqlite3.connect('equipment.db')
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
        sqliteConnection = sqlite3.connect('mobspawn.db')
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
        sqliteConnection = sqlite3.connect('mobspawn.db')
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
        sqliteConnection = sqlite3.connect('mobspawn.db')
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
        sqliteConnection = sqlite3.connect('mobspawn.db')
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
    
def add_beasts_to_server(beasts_name, base_level, base_hp,
                        base_str, base_def, base_spd, 
                        base_dex, hp_growth_rate, 
                        str_growth_rate, def_growth_rate, 
                        spd_growth_rate, dex_growth_rate, 
                        beasts_description):
        sqliteConnection = sqlite3.connect('beasts.db')
        cursor = sqliteConnection.cursor()
        beasts_name_lower = beasts_name.lower()
        query = """INSERT INTO beastdb(beasts_name, base_level,
                        base_hp, base_str, base_def, base_spd, 
                        base_dex, hp_growth_rate, 
                        str_growth_rate, def_growth_rate, 
                        spd_growth_rate, dex_growth_rate, 
                        beasts_description) 
                        VALUES 
                                (?,?,?,?,?,?,?,?,?,?,?,?,?)""" 
        cursor.execute(query, (beasts_name, base_level, base_hp,
                       base_str, base_def, base_spd, 
                       base_dex, hp_growth_rate, 
                       str_growth_rate, def_growth_rate, 
                       spd_growth_rate, dex_growth_rate, 
                       beasts_description))
                    
        sqliteConnection.commit()
        cursor.close()
        sqliteConnection.close()
        return('``` beast: ' + beasts_name_lower + ' has been added to the game.```')

def remove_beasts_from_server(beasts_name):
    if(calc.validate_fields(beasts_name) == True):
        beasts_name_lower = beasts_name.lower()
        sqliteConnection = sqlite3.connect('beasts.db')
        cursor = sqliteConnection.cursor()
        query = "DELETE FROM beastdb WHERE beasts_name = ?;"
        cursor.execute(query, beasts_name_lower)
        sqliteConnection.commit()
        cursor.close()
        sqliteConnection.close()

        return('``` beast: ' + beasts_name_lower + ' was deleted from the server.```')
     
def remove_beasts_from_player(beasts_nickname):
    if(calc.validate_fields(beasts_nickname) == True):
        beasts_nickname_lower = beasts_nickname.lower()
        sqliteConnection = sqlite3.connect('beasts.db')
        cursor = sqliteConnection.cursor()
        query = "DELETE FROM characters_beast WHERE beasts_nickname = ? AND character_name;"
        cursor.execute(query, beasts_nickname_lower)
        sqliteConnection.commit()
        cursor.close()
        sqliteConnection.close()

        return('``` beast: ' + beasts_nickname_lower + ' was deleted from the server.```')
    
def add_fish_to_server(name, description, location, rarity, how_to_obtain, difficulty):
    if(calc.validate_fields(name) == True):
        name_lower = name.lower()
        description_lower = description.lower()
        location_lower = location.lower()
        rarity_lower = rarity.lower()
        how_to_obtain_lower = how_to_obtain.lower()
        sqliteConnection = sqlite3.connect('equipment.db')
        cursor = sqliteConnection.cursor()
        query = """INSERT INTO fishdb(name, description, rarity, how_to_obtain, location, difficulty)
                   VALUES
                        (?,?,?,?,?,?);"""
        cursor.execute(query, (name_lower, description_lower, rarity_lower, how_to_obtain_lower, location_lower, difficulty))
        sqliteConnection.commit()
        cursor.close()
        sqliteConnection.close()

        return('``` fish: ' + name_lower + ' has been added to ' + location_lower + '.```')
