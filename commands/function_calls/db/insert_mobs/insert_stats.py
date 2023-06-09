import sqlite3

try:
    sqliteConnection = sqlite3.connect('mobspawn.db')
    cursor = sqliteConnection.cursor()
    print("Successfully Connected to SQLite")

    sqlite_insert_query = """INSERT INTO stats
                          (name, HP, STR, SPE, AGI, DEX, DEF, beginner_level, max_level)
                           VALUES 
                          ('frenzy boar', 20, 20, 1, 1, 1, 5, 1, 4)"""

    count = cursor.execute(sqlite_insert_query)
    sqliteConnection.commit()

    sqlite_insert_query = """INSERT INTO stats
                          (name, HP, STR, SPE, AGI, DEX, DEF, beginner_level, max_level)
                           VALUES 
                          ('dire wolf', 20, 25, 2, 1, 3, 3, 3, 8)"""

    count = cursor.execute(sqlite_insert_query)    
    sqliteConnection.commit()

    sqlite_insert_query = """INSERT INTO stats
                          (name, HP, STR, SPE, AGI, DEX, DEF, beginner_level, max_level)
                           VALUES 
                          ('large nepenthes', 20, 20, 1, 1, 1, 5, 1, 4)"""

    count = cursor.execute(sqlite_insert_query)
    sqliteConnection.commit()

    sqlite_insert_query = """INSERT INTO stats
                          (name, HP, STR, SPE, AGI, DEX, DEF, beginner_level, max_level)
                           VALUES 
                          ('little nepenthes', 20, 25, 2, 1, 3, 3, 3, 8)"""

    count = cursor.execute(sqlite_insert_query)    
    sqliteConnection.commit()
    
    sqlite_insert_query = """INSERT INTO stats
                          (name, HP, STR, SPE, AGI, DEX, DEF, beginner_level, max_level)
                           VALUES 
                          ('scavenger toad', 20, 20, 1, 1, 1, 5, 1, 4)"""

    count = cursor.execute(sqlite_insert_query)
    sqliteConnection.commit()

    sqlite_insert_query = """INSERT INTO stats
                          (name, HP, STR, SPE, AGI, DEX, DEF, beginner_level, max_level)
                           VALUES 
                          ('cow', 20, 25, 2, 1, 3, 3, 3, 8)"""

    count = cursor.execute(sqlite_insert_query)    
    sqliteConnection.commit()
    
    sqlite_insert_query = """INSERT INTO stats
                          (name, HP, STR, SPE, AGI, DEX, DEF, beginner_level, max_level)
                           VALUES 
                          ('white tailed buck', 20, 20, 1, 1, 1, 5, 1, 4)"""

    count = cursor.execute(sqlite_insert_query)
    sqliteConnection.commit()

    sqlite_insert_query = """INSERT INTO stats
                          (name, HP, STR, SPE, AGI, DEX, DEF, beginner_level, max_level)
                           VALUES 
                          ('mountain troll', 20, 25, 2, 1, 3, 3, 3, 8)"""

    count = cursor.execute(sqlite_insert_query)    
    sqliteConnection.commit()

    sqlite_insert_query = """INSERT INTO stats
                          (name, HP, STR, SPE, AGI, DEX, DEF, beginner_level, max_level)
                           VALUES 
                          ('goat', 20, 25, 2, 1, 3, 3, 3, 8)"""

    count = cursor.execute(sqlite_insert_query)    
    sqliteConnection.commit()

    sqlite_insert_query = """INSERT INTO stats
                          (name, HP, STR, SPE, AGI, DEX, DEF, beginner_level, max_level)
                           VALUES 
                          ('goblin', 20, 25, 2, 1, 3, 3, 3, 8)"""

    count = cursor.execute(sqlite_insert_query)    
    sqliteConnection.commit()

    sqlite_insert_query = """INSERT INTO stats
                          (name, HP, STR, SPE, AGI, DEX, DEF, beginner_level, max_level)
                           VALUES 
                          ('bat', 20, 25, 2, 1, 3, 3, 3, 8)"""

    count = cursor.execute(sqlite_insert_query)    
    sqliteConnection.commit()

    sqlite_insert_query = """INSERT INTO stats
                          (name, HP, STR, SPE, AGI, DEX, DEF, beginner_level, max_level)
                           VALUES 
                          ('giant beetle', 20, 25, 2, 1, 3, 3, 3, 8)"""

    count = cursor.execute(sqlite_insert_query)    
    sqliteConnection.commit()

    sqlite_insert_query = """INSERT INTO stats
                          (name, HP, STR, SPE, AGI, DEX, DEF, beginner_level, max_level)
                           VALUES 
                          ('skeleton gladiator', 20, 25, 2, 1, 3, 3, 3, 8)"""

    count = cursor.execute(sqlite_insert_query)    
    sqliteConnection.commit()

    sqlite_insert_query = """INSERT INTO stats
                          (name, HP, STR, SPE, AGI, DEX, DEF, beginner_level, max_level)
                           VALUES 
                          ('giant spider', 20, 25, 2, 1, 3, 3, 3, 8)"""

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
