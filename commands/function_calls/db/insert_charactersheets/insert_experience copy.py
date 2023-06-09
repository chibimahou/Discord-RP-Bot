#Insert Data into Table

import sqlite3

try:
    sqliteConnection = sqlite3.connect('characterSheet.db')
    cursor = sqliteConnection.cursor()
    print("Successfully Connected to SQLite")

    sqlite_insert_query = """INSERT INTO experience
                          (level, experience)
                           VALUES 
                          (1,400)"""
    count = cursor.execute(sqlite_insert_query)
    sqliteConnection.commit()
    sqlite_insert_query = """INSERT INTO experience
                          (level, experience)
                           VALUES 
                          (2,1200)"""                     
    count = cursor.execute(sqlite_insert_query)
    sqliteConnection.commit()
    sqlite_insert_query = """INSERT INTO experience
                          (level, experience)
                           VALUES 
                          (3,2400)"""
    count = cursor.execute(sqlite_insert_query)
    sqliteConnection.commit() 
    sqlite_insert_query = """INSERT INTO experience
                          (level, experience)
                           VALUES 
                          (4,4800)"""
    count = cursor.execute(sqlite_insert_query)
    sqliteConnection.commit() 
    sqlite_insert_query = """INSERT INTO experience
                          (level, experience)
                           VALUES 
                          (5,9600)"""                                                   
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
