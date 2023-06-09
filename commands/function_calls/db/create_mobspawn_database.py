#Create Table

import sqlite3

try:
    sqliteConnection = sqlite3.connect('mobspawn.db')
    cursor = sqliteConnection.cursor()
    print("Successfully Connected to SQLite")

#Mobs database instantiation.
#Contains mob information.
    sqlite_insert_query = """CREATE TABLE 
        mobs(ID INTEGER primary key autoincrement, name varchar(70), 
        type varchar(70), rarity varchar(70), Drops varchar(70));"""

    count = cursor.execute(sqlite_insert_query)
#Stats database instantiation.
#Contains the stats of mobs.
    sqlite_insert_query = """CREATE TABLE 
        stats(ID INTEGER primary key autoincrement, HP INTENGER, 
        STR INTENGER, SPE INTENGER, AGI INTENGER);"""

    count = cursor.execute(sqlite_insert_query)
#Location database instantiation.
#Contains floor areas and monster spawns in those areas.
    sqlite_insert_query = """CREATE TABLE 
        Location(Floor INTEGER, area varchar(70), spawns varchar(70));"""
    count = cursor.execute(sqlite_insert_query)

#Petdb database instantiation.
#Contains a list of tamable beasts and their base stat values
    sqlite_insert_query = """CREATE TABLE 
        petdb(pet_name varchar(50), base_level INTEGER, base_hp int, base_str int, 
        base_def int, base_spd int, base_dex int, hp_growth_rate int, 
        str_growth_rate int, def_growth_rate int, 
        spd_growth_rate int, dex_growth_rate int, pet_description varchar(500));"""
    count = cursor.execute(sqlite_insert_query)

#Petdb database instantiation.
#Contains a list of tamable beasts and their base stat values
    sqlite_insert_query = """CREATE TABLE 
        characters_beasts(pet_name, varchar(50), pet_nickname varchar(50), 
        level INTEGER, hp int, str int, 
        def int, spd int, dex int, uv_hp int, 
        uv_str int, uv_def int, 
        uv_spd int, uv_dex int, players_tag varchar(50), unique_identifier varchar(100));"""
    
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
