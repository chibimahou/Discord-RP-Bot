#Create Table

import sqlite3

try:
    sqliteConnection = sqlite3.connect('sessions.db')
    cursor = sqliteConnection.cursor()
    print("Successfully Connected to SQLite")

    sqlite_insert_query = """CREATE TABLE combat_sesion(
                            session_id int AUTOINCRIMENT PRIMARY KEY, 
                            session_type VARCHAR(20)
                            );"""

    count = cursor.execute(sqlite_insert_query)

    sqlite_insert_query = """CREATE TABLE players (
                            player_id INTEGER PRIMARY KEY,
                            session_id INTEGER,
                            player_name VARCHAR(20)
                            );"""

    count = cursor.execute(sqlite_insert_query)

    sqlite_insert_query = """CREATE TABLE Mobs (
                            mob_id INTEGER PRIMARY KEY,
                            session_id INTEGER,
                            mob_name VARCHAR(20)
                            );"""

    count = cursor.execute(sqlite_insert_query)

    sqlite_insert_query = """CREATE TABLE party(
                            party_id VARCHAR(20) PRIMARY KEY, 
                            party_members VARCHAR(120),
                            party_name varchar(50),
                            party_count int);"""
    count = cursor.execute( sqlite_insert_query)

    sqlite_insert_query = """CREATE TABLE invites(
                            invite_id VARCHAR(20) PRIMARY KEY, 
                            inviter VARCHAR(20),
                            invitee VARCHAR(20),
                            party_id VARCHAR(20),
                            expired DATE);"""
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
