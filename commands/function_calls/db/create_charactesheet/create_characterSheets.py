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
        proficiencySkills varchar(20), equipment varchar(200), currentWeaponEquipped varchar(50),
        col int, experience int, level int, str int, def int, spd int, dex int, cha int,
        playerStatus varchar (20), battle_status varchar (20),
        party_id varchar(50), discord_tag varchar (100), unique_key varchar(100));"""

    count = cursor.execute(sqlite_insert_query)

    sqlite_insert_query = """CREATE TABLE 
        experience(level int PRIMARY KEY, experience int);"""

    count = cursor.execute(sqlite_insert_query)

    sqlite_insert_query = """CREATE TABLE 
        guilds(guild_name VARCHAR(50) PRIMARY KEY, 
        guild_description VARCHAR(200), guild_approvers VARCHAR(200), 
        guild_member_count int);"""
    
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
