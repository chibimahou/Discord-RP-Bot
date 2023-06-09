import sqlite3

try:
    sqliteConnection = sqlite3.connect('mobspawn.db')
    cursor = sqliteConnection.cursor()
    print("Successfully Connected to SQLite")

    sqlite_insert_query = """INSERT INTO mobs
                          (name, type, rarity, drops)
                           VALUES 
                          ('frenzy boar', 'beast', 'common','raw boar prok,boar tusk,boar hide,boar blood')"""

    count = cursor.execute(sqlite_insert_query)
    sqlite_insert_query = """INSERT INTO mobs
                          (name, type, rarity, drops)
                           VALUES 
                          ('dire wolf', 'beast', 'common','wolf pelt,wolf fangs,wolf eye,wolf meat')"""

    count = cursor.execute(sqlite_insert_query)
    sqlite_insert_query = """INSERT INTO mobs
                          (name, type, rarity, drops)
                           VALUES 
                          ('large nepenthes', 'plant', 'uncommon','nepenthes seeds,nepenthes nectar,nepenthes extract,nepenthes vine')"""

    count = cursor.execute(sqlite_insert_query)
    sqlite_insert_query = """INSERT INTO mobs
                          (name, type, rarity, drops)
                           VALUES 
                          ('little nepenthes', 'plant', 'common','nepenthes seeds,nepenthes nectar,nepenthes extract,nepenthes vine')"""
    count = cursor.execute(sqlite_insert_query)
    sqlite_insert_query = """INSERT INTO mobs
                          (name, type, rarity, drops)
                           VALUES 
                          ('scavenger toad', 'amphinian', 'common','toad poison,toad eggs,toad raw meat')"""
    count = cursor.execute(sqlite_insert_query)
    sqliteConnection.commit()
    
    sqlite_insert_query = """INSERT INTO mobs
                          (name, type, rarity, drops)
                           VALUES 
                          ('cow', 'beast', 'common','cow hide,cow meat,cow milk,cow bell')"""
    count = cursor.execute(sqlite_insert_query)
    sqliteConnection.commit()
    
    sqlite_insert_query = """INSERT INTO mobs
                          (name, type, rarity, drops)
                           VALUES 
                          ('white tailed buck', 'beast', 'common','deer antlers,deer meat,deer pelt,deer hooves')"""
    count = cursor.execute(sqlite_insert_query)
    sqliteConnection.commit()
    
    sqlite_insert_query = """INSERT INTO mobs
                          (name, type, rarity, drops)
                           VALUES 
                          ('mountain troll', 'humanoid', 'common','troll hair,troll claws,troll bone')"""
    count = cursor.execute(sqlite_insert_query)
    sqliteConnection.commit()
    
    sqlite_insert_query = """INSERT INTO mobs
                          (name, type, rarity, drops)
                           VALUES 
                          ('goat', 'beast', 'common','goat wool,goat milk,goat hide')"""
    count = cursor.execute(sqlite_insert_query)
    sqliteConnection.commit()
    
    sqlite_insert_query = """INSERT INTO mobs
                          (name, type, rarity, drops)
                           VALUES 
                          ('goblin', 'humaniod', 'common','goblin ear,goblin cloth')"""
    count = cursor.execute(sqlite_insert_query)
    sqliteConnection.commit()
    
    sqlite_insert_query = """INSERT INTO mobs
                          (name, type, rarity, drops)
                           VALUES 
                          ('bat', 'beast', 'common','bat wings, bat fangs, small hp potion')"""
    count = cursor.execute(sqlite_insert_query)
    sqliteConnection.commit()

    sqlite_insert_query = """INSERT INTO mobs
                          (name, type, rarity, drops)
                           VALUES 
                          ('giant beetle', 'insect', 'common','')"""
    count = cursor.execute(sqlite_insert_query)
    sqliteConnection.commit()

    sqlite_insert_query = """INSERT INTO mobs
                          (name, type, rarity, drops)
                           VALUES 
                          ('skeleton gladiator', 'humanoid', 'common','bronze med helm,  wood(Can be used for firemaking or construction), iron ingot')"""
    count = cursor.execute(sqlite_insert_query)
    sqliteConnection.commit()

    sqlite_insert_query = """INSERT INTO mobs
                          (name, type, rarity, drops)
                           VALUES 
                          ('giant spider', 'arachnid', 'common','')"""
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
