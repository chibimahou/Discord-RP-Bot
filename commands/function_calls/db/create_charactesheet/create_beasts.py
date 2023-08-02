#Create Table

import sqlite3

try:
    sqliteConnection = sqlite3.connect('beasts.db')
    cursor = sqliteConnection.cursor()
    print("Successfully Connected to SQLite")

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
        uv_spd varchar(4), uv_dex varchar(4), players_name varchar(50), players_tag varchar(50), unique_identifier varchar(50));"""
    
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
