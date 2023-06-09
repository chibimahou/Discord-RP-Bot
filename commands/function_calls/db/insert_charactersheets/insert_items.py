#Insert Data into Table

import sqlite3

try:

    #1
    sqliteConnection = sqlite3.connect('characterSheet.db')
    cursor = sqliteConnection.cursor()
    print("Successfully Connected to SQLite")
    sqlite_insert_query = "INSERT INTO items (catagory, item, item_description, rarity, droppedby) VALUES ('medicinal','herb','A Herb said to provide basic recovery values.','Common', 'boar,little nephities')"
    count = cursor.execute(sqlite_insert_query)
    sqliteConnection.commit()

    sqlite_insert_query = "INSERT INTO items (catagory, item, item_description, rarity, droppedby) VALUES ('crafting','bronze ingot','An Ingot used for crafting Bronze equipment.','Common', 'refine bronze ore')"
    count = cursor.execute(sqlite_insert_query)
    
    sqliteConnection.commit()

    sqlite_insert_query = "INSERT INTO items (catagory, item, item_description, rarity, droppedby) VALUES ('material','wolf pelt','An Ingot used for crafting Bronze equipment.','Common', 'drop')"
    count = cursor.execute(sqlite_insert_query)
    
    sqliteConnection.commit()

    sqlite_insert_query = "INSERT INTO items (catagory, item, item_description, rarity, droppedby) VALUES ('material','wolf fang','An Ingot used for crafting Bronze equipment.','Common', 'drop')"
    count = cursor.execute(sqlite_insert_query)
    
    sqliteConnection.commit()

    sqlite_insert_query = "INSERT INTO items (catagory, item, item_description, rarity, droppedby) VALUES ('ingredient','wolf meat','An Ingot used for crafting Bronze equipment.','Common', 'drop')"
    count = cursor.execute(sqlite_insert_query)
    
    sqliteConnection.commit()

    sqlite_insert_query = "INSERT INTO items (catagory, item, item_description, rarity, droppedby) VALUES ('ingredient','raw boar pork','An Ingot used for crafting Bronze equipment.','Common', 'drop')"
    count = cursor.execute(sqlite_insert_query)
    
    sqliteConnection.commit()

    sqlite_insert_query = "INSERT INTO items (catagory, item, item_description, rarity, droppedby) VALUES ('material','boar tusk','An Ingot used for crafting Bronze equipment.','Common', 'drop')"
    count = cursor.execute(sqlite_insert_query)
    
    sqliteConnection.commit()

    sqlite_insert_query = "INSERT INTO items (catagory, item, item_description, rarity, droppedby) VALUES ('material','boar hide','An Ingot used for crafting Bronze equipment.','Common', 'drop')"
    count = cursor.execute(sqlite_insert_query)
    
    sqliteConnection.commit()

    sqlite_insert_query = "INSERT INTO items (catagory, item, item_description, rarity, droppedby) VALUES ('material','boar blood','An Ingot used for crafting Bronze equipment.','Common', 'drop')"
    count = cursor.execute(sqlite_insert_query)
    
    sqliteConnection.commit()

    sqlite_insert_query = "INSERT INTO items (catagory, item, item_description, rarity, droppedby) VALUES ('ingredient','nepenthes seeds','An Ingot used for crafting Bronze equipment.','Common', 'drop')"
    count = cursor.execute(sqlite_insert_query)
    
    sqliteConnection.commit()

    sqlite_insert_query = "INSERT INTO items (catagory, item, item_description, rarity, droppedby) VALUES ('ingredient','nepenthes nectar','An Ingot used for crafting Bronze equipment.','Common', 'drop')"
    count = cursor.execute(sqlite_insert_query)
    
    sqliteConnection.commit()

    sqlite_insert_query = "INSERT INTO items (catagory, item, item_description, rarity, droppedby) VALUES ('ingredient','nepenthes extract','An Ingot used for crafting Bronze equipment.','Common', 'drop')"
    count = cursor.execute(sqlite_insert_query)
    
    sqliteConnection.commit()

    sqlite_insert_query = "INSERT INTO items (catagory, item, item_description, rarity, droppedby) VALUES ('ingredient','nepenthes vine','An Ingot used for crafting Bronze equipment.','Common', 'drop')"
    count = cursor.execute(sqlite_insert_query)
    
    sqliteConnection.commit()

    sqlite_insert_query = "INSERT INTO items (catagory, item, item_description, rarity, droppedby) VALUES ('ingredient','toad poison','An Ingot used for crafting Bronze equipment.','Common', 'drop')"
    count = cursor.execute(sqlite_insert_query)
    
    sqliteConnection.commit()

    sqlite_insert_query = "INSERT INTO items (catagory, item, item_description, rarity, droppedby) VALUES ('ingredient','toad eggs','An Ingot used for crafting Bronze equipment.','Common', 'drop')"
    count = cursor.execute(sqlite_insert_query)
    
    sqliteConnection.commit()

    sqlite_insert_query = "INSERT INTO items (catagory, item, item_description, rarity, droppedby) VALUES ('ingredient','toad raw meat','An Ingot used for crafting Bronze equipment.','Common', 'drop')"
    count = cursor.execute(sqlite_insert_query)
    
    sqliteConnection.commit()

    sqlite_insert_query = "INSERT INTO items (catagory, item, item_description, rarity, droppedby) VALUES ('ingredient','cow hide','An Ingot used for crafting Bronze equipment.','Common', 'drop')"
    count = cursor.execute(sqlite_insert_query)
    
    sqliteConnection.commit()

    sqlite_insert_query = "INSERT INTO items (catagory, item, item_description, rarity, droppedby) VALUES ('ingredient','cow meat','An Ingot used for crafting Bronze equipment.','Common', 'drop')"
    count = cursor.execute(sqlite_insert_query)
    
    sqliteConnection.commit()

    sqlite_insert_query = "INSERT INTO items (catagory, item, item_description, rarity, droppedby) VALUES ('ingredient','cow milk','An Ingot used for crafting Bronze equipment.','Common', 'drop')"
    count = cursor.execute(sqlite_insert_query)
    
    sqliteConnection.commit()

    sqlite_insert_query = "INSERT INTO items (catagory, item, item_description, rarity, droppedby) VALUES ('ingredient','cow bell','An Ingot used for crafting Bronze equipment.','Common', 'drop')"
    count = cursor.execute(sqlite_insert_query)
    
    sqliteConnection.commit()

    sqlite_insert_query = "INSERT INTO items (catagory, item, item_description, rarity, droppedby) VALUES ('ingredient','deer antlers','An Ingot used for crafting Bronze equipment.','Common', 'drop')"
    count = cursor.execute(sqlite_insert_query)
    
    sqliteConnection.commit()

    sqlite_insert_query = "INSERT INTO items (catagory, item, item_description, rarity, droppedby) VALUES ('ingredient','deer meat','An Ingot used for crafting Bronze equipment.','Common', 'drop')"
    count = cursor.execute(sqlite_insert_query)
    
    sqliteConnection.commit()

    sqlite_insert_query = "INSERT INTO items (catagory, item, item_description, rarity, droppedby) VALUES ('ingredient','deer pelt','An Ingot used for crafting Bronze equipment.','Common', 'drop')"
    count = cursor.execute(sqlite_insert_query)
    
    sqliteConnection.commit()

    sqlite_insert_query = "INSERT INTO items (catagory, item, item_description, rarity, droppedby) VALUES ('ingredient','deer hooves','An Ingot used for crafting Bronze equipment.','Common', 'drop')"
    count = cursor.execute(sqlite_insert_query)
    
    sqliteConnection.commit()

    sqlite_insert_query = "INSERT INTO items (catagory, item, item_description, rarity, droppedby) VALUES ('ingredient','troll hair','An Ingot used for crafting Bronze equipment.','Common', 'drop')"
    count = cursor.execute(sqlite_insert_query)
    
    sqliteConnection.commit()

    sqlite_insert_query = "INSERT INTO items (catagory, item, item_description, rarity, droppedby) VALUES ('ingredient','troll claws','An Ingot used for crafting Bronze equipment.','Common', 'drop')"
    count = cursor.execute(sqlite_insert_query)
    
    sqliteConnection.commit()

    sqlite_insert_query = "INSERT INTO items (catagory, item, item_description, rarity, droppedby) VALUES ('ingredient','troll bone','An Ingot used for crafting Bronze equipment.','Common', 'drop')"
    count = cursor.execute(sqlite_insert_query)
    
    sqliteConnection.commit()

    sqlite_insert_query = "INSERT INTO items (catagory, item, item_description, rarity, droppedby) VALUES ('ingredient','goat wool','An Ingot used for crafting Bronze equipment.','Common', 'drop')"
    count = cursor.execute(sqlite_insert_query)
    
    sqliteConnection.commit()

    sqlite_insert_query = "INSERT INTO items (catagory, item, item_description, rarity, droppedby) VALUES ('ingredient','goat milk','An Ingot used for crafting Bronze equipment.','Common', 'drop')"
    count = cursor.execute(sqlite_insert_query)
    
    sqliteConnection.commit()

    sqlite_insert_query = "INSERT INTO items (catagory, item, item_description, rarity, droppedby) VALUES ('ingredient','goat hide','An Ingot used for crafting Bronze equipment.','Common', 'drop')"
    count = cursor.execute(sqlite_insert_query)
    
    sqliteConnection.commit()

    sqlite_insert_query = "INSERT INTO items (catagory, item, item_description, rarity, droppedby) VALUES ('ingredient','goblin ear','An Ingot used for crafting Bronze equipment.','Common', 'drop')"
    count = cursor.execute(sqlite_insert_query)
    
    sqliteConnection.commit()

    sqlite_insert_query = "INSERT INTO items (catagory, item, item_description, rarity, droppedby) VALUES ('ingredient','goblin cloth','An Ingot used for crafting Bronze equipment.','Common', 'drop')"
    count = cursor.execute(sqlite_insert_query)
    
    sqliteConnection.commit()

    sqlite_insert_query = "INSERT INTO items (catagory, item, item_description, rarity, droppedby) VALUES ('ingredient','bat wings','An Ingot used for crafting Bronze equipment.','Common', 'drop')"
    count = cursor.execute(sqlite_insert_query)
    
    sqliteConnection.commit()

    sqlite_insert_query = "INSERT INTO items (catagory, item, item_description, rarity, droppedby) VALUES ('ingredient','bat fangs','An Ingot used for crafting Bronze equipment.','Common', 'drop')"
    count = cursor.execute(sqlite_insert_query)
    
    sqliteConnection.commit()

    sqlite_insert_query = "INSERT INTO items (catagory, item, item_description, rarity, droppedby) VALUES ('ingredient','small hp potion','An Ingot used for crafting Bronze equipment.','Common', 'drop')"
    count = cursor.execute(sqlite_insert_query)
    
    sqliteConnection.commit()

    sqlite_insert_query = "INSERT INTO items (catagory, item, item_description, rarity, droppedby) VALUES ('ingredient','bronze med helm','An Ingot used for crafting Bronze equipment.','Common', 'drop')"
    count = cursor.execute(sqlite_insert_query)
    
    sqliteConnection.commit()

    sqlite_insert_query = "INSERT INTO items (catagory, item, item_description, rarity, droppedby) VALUES ('ingredient','wood','An Ingot used for crafting Bronze equipment.','Common', 'drop')"
    count = cursor.execute(sqlite_insert_query)
    
    sqliteConnection.commit()

    sqlite_insert_query = "INSERT INTO items (catagory, item, item_description, rarity, droppedby) VALUES ('ingredient','iron ingot','An Ingot used for crafting Bronze equipment.','Common', 'drop')"
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
