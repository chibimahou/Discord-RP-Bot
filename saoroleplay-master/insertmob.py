import sqlite3

try:
    sqliteConnection = sqlite3.connect('mobspawn.db')
    cursor = sqliteConnection.cursor()
    print("Successfully Connected to SQLite")

    sqlite_insert_query = """INSERT INTO mobs
                          (name, type, rarity, drops)
                           VALUES 
                          ('Frenzy Boar', 'beast', 'common','1')"""

    count = cursor.execute(sqlite_insert_query)
    sqlite_insert_query = """INSERT INTO mobs
                          (name, type, rarity, drops)
                           VALUES 
                          ('Dire Wolf', 'beast', 'common','1')"""

    count = cursor.execute(sqlite_insert_query)
    sqlite_insert_query = """INSERT INTO mobs
                          (name, type, rarity, drops)
                           VALUES 
                          ('Large Nepents', 'plant', 'uncommon','1')"""

    count = cursor.execute(sqlite_insert_query)
    sqlite_insert_query = """INSERT INTO mobs
                          (name, type, rarity, drops)
                           VALUES 
                          ('Litte Nepents', 'plant', 'common','1')"""
    count = cursor.execute(sqlite_insert_query)
    sqlite_insert_query = """INSERT INTO mobs
                          (name, type, rarity, drops)
                           VALUES 
                          ('Scavenger Toad', 'amphinian', 'common','1')"""
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
