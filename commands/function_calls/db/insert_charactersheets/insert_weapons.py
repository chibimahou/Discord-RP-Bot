#Insert Data into Table

import sqlite3

try:

    #1
    sqliteConnection = sqlite3.connect('characterSheet.db')
    cursor = sqliteConnection.cursor()
    print("Successfully Connected to SQLite")
    sqlite_insert_query = "INSERT INTO weapons (weapon_name, weapon_description, weapon_rarity, how_to_obtain, base_power, additional_effects, crit_chance, weapon_material, weapon_attack_type, catagory) VALUES ('bronze 1 handed sword','A one handed sword crafted using bronze. Its quality is rough.','common','blacksmithing, store', '10', 'none', '5', 'bronze', 'str', 'weapon')"
    count = cursor.execute(sqlite_insert_query)
    sqlite_insert_query = "INSERT INTO weapons (weapon_name, weapon_description, weapon_rarity, how_to_obtain, base_power, additional_effects, crit_chance, weapon_material, weapon_attack_type, catagory) VALUES ('bronze 2 handed sword','A two handed sword crafted using bronze. Its quality is rough.','common','blacksmithing, store', '12', '-2 speed, unable to equip shield', '0', 'bronze', 'str', 'weapon')"
    count = cursor.execute(sqlite_insert_query)
    sqlite_insert_query = "INSERT INTO weapons (weapon_name, weapon_description, weapon_rarity, how_to_obtain, base_power, additional_effects, crit_chance, weapon_material, weapon_attack_type, catagory) VALUES ('bronze mace','A one handed mace crafted using bronze. Its quality is rough.','common','blacksmithing, store', '10', 'none', '5', 'bronze', 'str', 'weapon')"
    count = cursor.execute(sqlite_insert_query)
    sqlite_insert_query = "INSERT INTO weapons (weapon_name, weapon_description, weapon_rarity, how_to_obtain, base_power, additional_effects, crit_chance, weapon_material, weapon_attack_type, catagory) VALUES ('bronze dagger','A dagger crafted using bronze. Its quality is rough.','common','blacksmithing, store', '8', '+2 dex', '10', 'bronze', 'str', 'weapon')"
    count = cursor.execute(sqlite_insert_query)
    sqlite_insert_query = "INSERT INTO weapons (weapon_name, weapon_description, weapon_rarity, how_to_obtain, base_power, additional_effects, crit_chance, weapon_material, weapon_attack_type, catagory) VALUES ('wooden longbow','A longbow crafted using low quality wood. Its quality is rough.','common','blacksmithing, store', '10', 'none', '5', 'bronze', 'dex', 'weapon')"
    count = cursor.execute(sqlite_insert_query)
    sqlite_insert_query = "INSERT INTO weapons (weapon_name, weapon_description, weapon_rarity, how_to_obtain, base_power, additional_effects, crit_chance, weapon_material, weapon_attack_type, catagory) VALUES ('wooden shortbow','A shortbow crafted using low quality wood. Its quality is rough.','common','blacksmithing, store', '12', '+2 spe', '0', 'bronze', 'dex', 'weapon')"
    count = cursor.execute(sqlite_insert_query)
    sqlite_insert_query = "INSERT INTO weapons (weapon_name, weapon_description, weapon_rarity, how_to_obtain, base_power, additional_effects, crit_chance, weapon_material, weapon_attack_type, catagory) VALUES ('anneal blade','A ceremonial one handed sword.','rare','quest', '15', 'none', '10', 'steel', 'str', 'weapon')"
    count = cursor.execute(sqlite_insert_query)
    sqlite_insert_query = "INSERT INTO weapons (weapon_name, weapon_description, weapon_rarity, how_to_obtain, base_power, additional_effects, crit_chance, weapon_material, weapon_attack_type, catagory) VALUES ('moonlight bow','A ceremonial longbow.','rare','quest', '12', 'none', '10', 'steel', 'dex', 'weapon')"
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
