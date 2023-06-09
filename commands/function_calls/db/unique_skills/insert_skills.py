#Insert Data into Table

import sqlite3

try:

    #1
    sqliteConnection = sqlite3.connect('characterSheet.db')
    cursor = sqliteConnection.cursor()
    print("Successfully Connected to SQLite")
    sqlite_insert_query = "INSERT INTO items (catagory, item, item_description, rarity, droppedby) VALUES ('Medicinal','Herb','A Herb said to provide basic recovery values.','Common', 'Boar,Little Nephities')"
    sqlite_insert_query = "INSERT INTO items (catagory, item, item_description, rarity, droppedby) VALUES ('Crafting','Bronze Ingot','An Ingot used for crafting Bronze equipment.','Common', 'Refine Bronze Ore')"

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
