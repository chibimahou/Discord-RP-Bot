        #Create Table

import sqlite3

try:
    sqliteConnection = sqlite3.connect('mobspawn.db')
    cursor = sqliteConnection.cursor()
    print("Successfully Connected to SQLite")

    sqlite_insert_query = """CREATE TABLE Location
                                (id AUTOINCRIMENT primary key, 
                                floor INTEGER, area varchar(70), 
                                spawns varchar(1000));"""
    count = cursor.execute(sqlite_insert_query)

    sqliteConnection.commit()

    sqlite_insert_query = """CREATE TABLE mob_descriptions
                                (name varchar(70) PRIMARY KEY, 
                                mob_description varchar(1000));"""
    count = cursor.execute(sqlite_insert_query)

    sqliteConnection.commit()

    sqlite_insert_query = """CREATE TABLE mobs
                                (name varchar(70) primary key, 
                                type varchar(70), rarity varchar(70), 
                                drops varchar(70));"""
    count = cursor.execute(sqlite_insert_query)

    sqliteConnection.commit()

    sqlite_insert_query = """CREATE TABLE stats
                                (name VARCHAR(50) primary key, HP INTENGER, 
                                STR INTENGER, SPE INTENGER, DEX INTEGER, 
                                DEF INTEGER, beginner_level INTEGER, col int, 
                                xp int, max_hp int, max_str int, 
                                max_spe int, max_dex int, max_def int, 
                                max_level INTEGER, max_xp int);"""
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