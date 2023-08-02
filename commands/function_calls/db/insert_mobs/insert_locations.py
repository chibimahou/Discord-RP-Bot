import sqlite3

try:
    sqliteConnection = sqlite3.connect('mobspawn.db')
    cursor = sqliteConnection.cursor()
    print("Successfully Connected to SQLite")

    sqlite_insert_query = """INSERT INTO Location
                          (floor, area, spawns)
                           VALUES 
                          (1, 'western fields' , 'frenzy boar,dire wolf')"""

    count = cursor.execute(sqlite_insert_query)  
    sqliteConnection.commit()

    sqlite_insert_query = """INSERT INTO Location
                          (floor, area, spawns)
                           VALUES 
                          (1, 'tranquil lake' , 'frenzy boar,dire wolf')"""

    count = cursor.execute(sqlite_insert_query)  
    sqliteConnection.commit()

    sqlite_insert_query  = """INSERT INTO Location
                       (floor, area, spawns)
                          Values
                        (1, 'eastern plains', 'cow,white tailed buck')"""

    count = cursor.execute(sqlite_insert_query)
    sqliteConnection.commit()

    sqlite_insert_query  = """INSERT INTO Location
                       (floor, area, spawns)
                          Values
                        (1, 'western forest', 'large nepenthes,little nepenthes,scavenger toad')"""

    count = cursor.execute(sqlite_insert_query)
    sqliteConnection.commit()

    sqlite_insert_query  = """INSERT INTO Location
                       (floor, area, spawns)
                          Values
                        (1, 'eastern mountains', 'mountain troll,goat')"""

    count = cursor.execute(sqlite_insert_query)
    sqliteConnection.commit()

    sqlite_insert_query  = """INSERT INTO Location
                       (floor, area, spawns)
                          Values
                        (1, 'dungeon', 'goblin,bat,giant beetle,skeleton gladiator,giant spider')"""

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
