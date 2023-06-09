#Create Table

import sqlite3

try:
    sqliteConnection = sqlite3.connect('characterSheet.db')
    cursor = sqliteConnection.cursor()
    print("Successfully Connected to SQLite")

    sqlite_insert_query = """
        CREATE TABLE 
        charactersheets(ID int AUTOINCRIMENT PRIMARY KEY, firstName varchar(30), 
        lastName varchar(30), height varchar(30), size varchar(30), 
        age varchar(2), skillList varchar(100), inventory varchar(100), 
        bio varchar(1000), guild varchar(20), class varchar(20), playerColor varchar(6), 
        birthday varchar(20), nickname varchar(20), uniqueSkills varchar(20), 
        proficiencySkills varchar(20), equipment varchar(200), col int, 
        experience int, level int, str int, def int, spd int, dex int, 
        playerStatus varchar (20), battle_status varchar (20), discord_tag varchar (100));"""

    count = cursor.execute(sqlite_insert_query)

    sqlite_insert_query = """CREATE TABLE 
        experience(level int PRIMARY KEY, experience int);"""

    count = cursor.execute(sqlite_insert_query)

    sqlite_insert_query = """CREATE TABLE 
        guilds(guild_name VARCHAR(50) PRIMARY KEY, 
        guild_description VARCHAR(200), guild_approvers VARCHAR(200), 
        guild_member_count int);"""

    count = cursor.execute(sqlite_insert_query)

    sqlite_insert_query = """CREATE TABLE 
        items(ID int AUTOINCRIMENT, catagory VARCHAR, 
        item VARCHAR, item_description VARCHAR, rarity VARCHAR, droppedby VARCHAR);"""

    count = cursor.execute(sqlite_insert_query)

    sqlite_insert_query = """CREATE TABLE 
        proficiency_skills(skill_name VARCHAR(20) PRIMARY KEY, 
        skill_description VARCHAR(200), skill_effects VARCHAR(200), 
        skill_type VARCHAR(20));"""

    count = cursor.execute(sqlite_insert_query)

    sqlite_insert_query = """CREATE TABLE sword_skills(
        skill_name VARCHAR(20) PRIMARY KEY, 
        skill_description VARCHAR(200), 
        skill_hits int, 
        skill_effects VARCHAR(200), 
        skill_type VARCHAR(20), 
        skill_power int, 
        skill_requirements VARCHAR(100));"""

    count = cursor.execute(sqlite_insert_query)

    sqlite_insert_query = """CREATE TABLE unique_skills(
        skill_name VARCHAR(20) PRIMARY KEY, 
        skill_description VARCHAR(200),    
        skill_requirements VARCHAR(100));"""
    count = cursor.execute(sqlite_insert_query)

    sqlite_insert_query = """CREATE TABLE weapons(weapon_name VARCHAR(100) PRIMARY KEY,
        weapon_description VARCHAR(200), 
        weapon_rarity VARCHAR(20), 
        how_to_obtain VARCHAR(200),
        base_power VARCHAR(10),
        additional_effects VARCHAR(200),
        crit_chance VARCHAR(10),
        weapon_material VARCHAR(20),
        weapon_attack_type VARCHAR(3),
        catagory VARCHAR(20));"""

    count = cursor.execute(sqlite_insert_query)

    sqlite_insert_query = """CREATE TABLE armor(armor_name VARCHAR(100) PRIMARY KEY,
        armor_description VARCHAR(200), 
        armor_rarity VARCHAR(20), 
        how_to_obtain VARCHAR(200),
        base_defense VARCHAR(10),
        additional_effects VARCHAR(200),
        armor_material VARCHAR(20),
        catagory VARCHAR(20));"""

    count = cursor.execute(sqlite_insert_query)

#Petdb database instantiation.
#Contains a list of tamable beasts and their base stat values
    sqlite_insert_query = """CREATE TABLE 
        beastdb(beasts_name varchar(50) PRIMARY KEY, base_level varchar(4), base_hp varchar(4), base_str varchar(4), 
        base_def varchar(4), base_spd varchar(4), base_dex varchar(4), hp_growth_rate varchar(4), 
        str_growth_rate varchar(4), def_growth_rate varchar(4), 
        spd_growth_rate varchar(4), dex_growth_rate varchar(4), beasts_description varchar(500));"""
    count = cursor.execute(sqlite_insert_query)

#Petdb database instantiation.
#Contains a list of tamable beasts and their base stat values
    sqlite_insert_query = """CREATE TABLE 
        characters_beasts(pet_name varchar(50), pet_nickname varchar(50), 
        level varchar(4), hp varchar(4), str varchar(4), 
        def varchar(4), spd varchar(4), dex varchar(4), uv_hp varchar(4), 
        uv_str varchar(4), uv_def varchar(4), 
        uv_spd varchar(4), uv_dex varchar(4), players_tag varchar(50), unique_identifier varchar(50));"""
    
    count = cursor.execute(sqlite_insert_query)
    sqliteConnection.commit()
    print("Record inserted successfully into SqliteDb_developers table ", cursor.rowcount)
    cursor.close()

except sqlite3.Error as error:
    print("Failed to insert data into sqlite table", error)
finally:
    if sqliteConnection:
        sqliteConnection.close()
        print("The SQLite connection is closed")
