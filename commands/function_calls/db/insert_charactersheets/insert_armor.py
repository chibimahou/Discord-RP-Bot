#Insert Data into Table

import sqlite3

try:

    #1
    sqliteConnection = sqlite3.connect('characterSheet.db')
    cursor = sqliteConnection.cursor()
    print("Successfully Connected to SQLite")
    sqlite_insert_query = "INSERT INTO armors (armor_name, armor_description, armor_rarity, how_to_obtain, base_defense, additional_effects, armor_material, catagory) VALUES ('bronze platebody','A one handed sword crafted using bronze. Its quality is rough.','common','blacksmithing, store', '2', '-2 dexterity', 'bronze', 'body')"
    count = cursor.execute(sqlite_insert_query)
    sqlite_insert_query = "INSERT INTO armors (armor_name, armor_description, armor_rarity, how_to_obtain, base_defense, additional_effects, armor_material, catagory) VALUES ('bronze platelegs','A two handed sword crafted using bronze. Its quality is rough.','common','blacksmithing, store', '1', '-1 dexterity, unable to equip shield', 'bronze', 'legs')"
    count = cursor.execute(sqlite_insert_query)
    sqlite_insert_query = "INSERT INTO armors (armor_name, armor_description, armor_rarity, how_to_obtain, base_defense, additional_effects, armor_material, catagory) VALUES ('bronze gauntlets','A one handed mace crafted using bronze. Its quality is rough.','common','blacksmithing, store', '1', '-1 dexterity', 'bronze', 'arms')"
    count = cursor.execute(sqlite_insert_query)
    sqlite_insert_query = "INSERT INTO armors (armor_name, armor_description, armor_rarity, how_to_obtain, base_defense, additional_effects, armor_material, catagory) VALUES ('bronze fullhelm','A dagger crafted using bronze. Its quality is rough.','common','blacksmithing, store', '1', '-1 dexterity', 'bronze', 'helm')"
    count = cursor.execute(sqlite_insert_query)
    sqlite_insert_query = "INSERT INTO armors (armor_name, armor_description, armor_rarity, how_to_obtain, base_defense, additional_effects, armor_material, catagory) VALUES ('bronze kiteshield','A longbow crafted using low quality wood. Its quality is rough.','common','blacksmithing, store', '2', '-2 dexterity', 'bronze', 'shield')"
    count = cursor.execute(sqlite_insert_query)
    sqlite_insert_query = "INSERT INTO armors (armor_name, armor_description, armor_rarity, how_to_obtain, base_defense, additional_effects, armor_material, catagory) VALUES ('bronze chainmail','A shortbow crafted using low quality wood. Its quality is rough.','common','blacksmithing, store', '1', 'none', 'bronze', 'body')"
    count = cursor.execute(sqlite_insert_query)
    sqlite_insert_query = "INSERT INTO armors (armor_name, armor_description, armor_rarity, how_to_obtain, base_defense, additional_effects, armor_material, catagory) VALUES ('bronze chianlegs','A ceremonial one handed sword.','rare','quest', '1', 'none', 'bronze', 'legs')"
    count = cursor.execute(sqlite_insert_query)
    sqlite_insert_query = "INSERT INTO armors (armor_name, armor_description, armor_rarity, how_to_obtain, base_defense, additional_effects, armor_material, catagory) VALUES ('bronze medhelm','A ceremonial longbow.','rare','quest', '1', 'none', 'bronze', 'helm')"
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
