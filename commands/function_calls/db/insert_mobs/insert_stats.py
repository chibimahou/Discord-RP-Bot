import sqlite3

try:
    sqliteConnection = sqlite3.connect('mobspawn.db')
    cursor = sqliteConnection.cursor()
    print("Successfully Connected to SQLite")

    sqlite_insert_query = """INSERT INTO stats
                          (name, HP, STR, SPE, DEX, DEF, beginner_level, col, xp, max_hp, max_str, max_def, max_spe, max_dex, max_level, max_xp)
                           VALUES 
                          ('frenzy boar', 20, 20, 1, 1, 5, 1, 50, 20, 5000, 50, 50, 50, 50, 4, 500)"""

    count = cursor.execute(sqlite_insert_query)
    sqliteConnection.commit()

    sqlite_insert_query = """INSERT INTO stats
                          (name, HP, STR, SPE, DEX, DEF, beginner_level, col, xp, max_hp, max_str, max_def, max_spe, max_dex, max_level, max_xp)
                           VALUES 
                          ('dire wolf', 20, 25, 2, 3, 3, 3, 50, 20, 5000, 50, 50, 50, 50, 8, 500)"""

    count = cursor.execute(sqlite_insert_query)    
    sqliteConnection.commit()

    sqlite_insert_query = """INSERT INTO stats
                          (name, HP, STR, SPE, DEX, DEF, beginner_level, col, xp, max_hp, max_str, max_def, max_spe, max_dex, max_level, max_xp)
                           VALUES 
                          ('large nepenthes', 20, 20, 1, 1, 5, 1, 50, 20, 5000, 50, 50, 50, 50, 4, 500)"""

    count = cursor.execute(sqlite_insert_query)
    sqliteConnection.commit()

    sqlite_insert_query = """INSERT INTO stats
                          (name, HP, STR, SPE, DEX, DEF, beginner_level, col, xp, max_hp, max_str, max_def, max_spe, max_dex, max_level, max_xp)
                           VALUES 
                          ('little nepenthes', 20, 25, 2, 3, 3, 3, 50, 20, 5000, 50, 50, 50, 50, 8, 500)"""

    count = cursor.execute(sqlite_insert_query)    
    sqliteConnection.commit()
    
    sqlite_insert_query = """INSERT INTO stats
                          (name, HP, STR, SPE, DEX, DEF, beginner_level, col, xp, max_hp, max_str, max_def, max_spe, max_dex, max_level, max_xp)
                           VALUES 
                          ('scavenger toad', 20, 20, 1, 1, 5, 1, 50, 20, 5000, 50, 50, 50, 50, 4, 500)"""

    count = cursor.execute(sqlite_insert_query)
    sqliteConnection.commit()

    sqlite_insert_query = """INSERT INTO stats
                          (name, HP, STR, SPE, DEX, DEF, beginner_level, col, xp, max_hp, max_str, max_def, max_spe, max_dex, max_level, max_xp)
                           VALUES 
                          ('cow', 20, 25, 2, 3, 3, 3, 50, 20, 5000, 50, 50, 50, 50, 8, 500)"""

    count = cursor.execute(sqlite_insert_query)    
    sqliteConnection.commit()
    
    sqlite_insert_query = """INSERT INTO stats
                          (name, HP, STR, SPE, DEX, DEF, beginner_level, col, xp, max_hp, max_str, max_def, max_spe, max_dex, max_level, max_xp)
                           VALUES 
                          ('white tailed buck', 20, 20, 1, 1, 5, 1, 50, 20, 5000, 50, 50, 50, 50, 4, 500)"""

    count = cursor.execute(sqlite_insert_query)
    sqliteConnection.commit()

    sqlite_insert_query = """INSERT INTO stats
                          (name, HP, STR, SPE, DEX, DEF, beginner_level, col, xp, max_hp, max_str, max_def, max_spe, max_dex, max_level, max_xp)
                           VALUES 
                          ('mountain troll', 20, 25, 2, 3, 3, 3, 50, 20, 5000, 50, 50, 50, 50, 8, 500)"""

    count = cursor.execute(sqlite_insert_query)    
    sqliteConnection.commit()

    sqlite_insert_query = """INSERT INTO stats
                          (name, HP, STR, SPE, DEX, DEF, beginner_level, col, xp, max_hp, max_str, max_def, max_spe, max_dex, max_level, max_xp)
                           VALUES 
                          ('goat', 20, 25, 2, 3, 3, 3, 50, 20, 5000, 50, 50, 50, 50, 8, 500)"""

    count = cursor.execute(sqlite_insert_query)    
    sqliteConnection.commit()

    sqlite_insert_query = """INSERT INTO stats
                          (name, HP, STR, SPE, DEX, DEF, beginner_level, col, xp, max_hp, max_str, max_def, max_spe, max_dex, max_level, max_xp)
                           VALUES 
                          ('goblin', 20, 25, 2, 3, 3, 3, 50, 20, 5000, 50, 50, 50, 50, 8, 500)"""

    count = cursor.execute(sqlite_insert_query)    
    sqliteConnection.commit()

    sqlite_insert_query = """INSERT INTO stats
                          (name, HP, STR, SPE, DEX, DEF, beginner_level, col, xp, max_hp, max_str, max_def, max_spe, max_dex, max_level, max_xp)
                           VALUES 
                          ('bat', 20, 25, 2, 3, 3, 3, 50, 20, 5000, 50, 50, 50, 50, 8, 500)"""

    count = cursor.execute(sqlite_insert_query)    
    sqliteConnection.commit()

    sqlite_insert_query = """INSERT INTO stats
                          (name, HP, STR, SPE, DEX, DEF, beginner_level, col, xp, max_hp, max_str, max_def, max_spe, max_dex, max_level, max_xp)
                           VALUES 
                          ('giant beetle', 20, 25, 2, 3, 3, 3, 50, 20, 5000, 50, 50, 50, 50, 8, 500)"""

    count = cursor.execute(sqlite_insert_query)    
    sqliteConnection.commit()

    sqlite_insert_query = """INSERT INTO stats
                          (name, HP, STR, SPE, DEX, DEF, beginner_level, col, xp, max_hp, max_str, max_def, max_spe, max_dex, max_level, max_xp)
                           VALUES 
                          ('skeleton gladiator', 20, 25, 2, 3, 3, 3, 50, 20, 5000, 50, 50, 50, 50, 8, 500)"""

    count = cursor.execute(sqlite_insert_query)    
    sqliteConnection.commit()

    sqlite_insert_query = """INSERT INTO stats
                          (name, HP, STR, SPE, DEX, DEF, beginner_level, col, xp, max_hp, max_str, max_def, max_spe, max_dex, max_level, max_xp)
                           VALUES 
                          ('giant spider', 20, 25, 2, 3, 3, 3, 50, 20, 5000, 50, 50, 50, 50, 8, 500)"""

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
