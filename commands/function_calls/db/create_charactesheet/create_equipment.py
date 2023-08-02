#Create Table

import sqlite3

try:
    sqliteConnection = sqlite3.connect('equipment.db')
    cursor = sqliteConnection.cursor()
    print("Successfully Connected to SQLite")

    sqlite_insert_query = """CREATE TABLE 
        items(
            ID int AUTOINCRIMENT, catagory VARCHAR, 
            item VARCHAR, item_description VARCHAR, rarity VARCHAR, droppedby VARCHAR);"""

    count = cursor.execute(sqlite_insert_query)
    
    sqlite_insert_query = """CREATE TABLE 
        ingredients(
            ID int AUTOINCRIMENT, item_name VARCHAR(20), item_description VARCHAR, 
            rarity VARCHAR, obtained VARCHAR, sweetness int, sourness int, saltines int, 
            bitterness int, umaminess int);"""

    count = cursor.execute(sqlite_insert_query)
    
    sqlite_insert_query = """CREATE TABLE 
        recipes(
            ID int AUTOINCRIMENT, item_name VARCHAR(20), item_description VARCHAR, 
            effect VARCHAR(100), rarity VARCHAR, difficulty int, ingredients VARCHAR(500), 
            sweetness int, sourness int, saltines int, bitterness int, umaminess int);"""

    count = cursor.execute(sqlite_insert_query)

    sqlite_insert_query = """CREATE TABLE 
        proficiency_skills(
            skill_name VARCHAR(20) PRIMARY KEY, 
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

    sqlite_insert_query = """CREATE TABLE fishdb(name VARCHAR(100) PRIMARY KEY,
        description VARCHAR(200), 
        rarity VARCHAR(20), 
        how_to_obtain VARCHAR(200),
        location VARCHAR(10),
        difficulty int);
        """
    count = cursor.execute(sqlite_insert_query)
   
    sqlite_insert_query = """CREATE TABLE blacksmithing_materials(name VARCHAR(100) PRIMARY KEY,
        description VARCHAR(200), 
        rarity VARCHAR(20), 
        how_to_obtain VARCHAR(200),
        location VARCHAR(10),
        difficulty int,
        processing_type varchar(50),
        processed_into varchar(50),
        catagory varchar(50));
        """

    count = cursor.execute(sqlite_insert_query)

    sqliteConnection.commit()
    print("Record inserted successfully into SqliteDb_developers table ", cursor.rowcount)
    cursor.close()
    sqliteConnection.close()

except sqlite3.Error as error:
    print("Failed to insert data into sqlite table", error)
finally:
    if sqliteConnection:
        sqliteConnection.close()
        print("The SQLite connection is closed")
