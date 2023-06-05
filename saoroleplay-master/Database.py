#Create Table

import sqlite3

try:
    sqliteConnection = sqlite3.connect('mobspawn.db')
    cursor = sqliteConnection.cursor()
    print("Successfully Connected to SQLite")

    sqlite_insert_query = """CREATE TABLE mobs(ID INTEGER primary key autoincrement, name varchar(70), type varchar(70), rarity varchar(70), Drops varchar(70));"""

    count = cursor.execute(sqlite_insert_query)
    sqlite_insert_query = """CREATE TABLE stats(ID INTEGER primary key autoincrement, HP INTENGER, STR INTENGER, SPE INTENGER, AGI INTENGER);"""

    count = cursor.execute(sqlite_insert_query)
    sqlite_insert_query = """CREATE TABLE Location(Floor INTEGER, area varchar(70), spawns varchar(70));"""

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
