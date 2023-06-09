#Insert Data into Table

import sqlite3

try:

    #1
    sqliteConnection = sqlite3.connect('characterSheet.db')
    cursor = sqliteConnection.cursor()
    print("Successfully Connected to SQLite")
    sqlite_insert_query = "INSERT INTO proficiency_skills (skill_name, skill_description, skill_effects, skill_type) VALUES ('fishing','A long running traditional skill allowing users to fish in any body of water.','Allows players to fish in any body of water and catch fish.','Life')"
    count = cursor.execute(sqlite_insert_query) 
    sqlite_insert_query = "INSERT INTO proficiency_skills (skill_name, skill_description, skill_effects, skill_type) VALUES ('woodcutting','A useful trait for any survivalist is the ability to chop wood.','Allows players to cut trees equivalent to their skill level.','Life')"
    count = cursor.execute(sqlite_insert_query)
    sqlite_insert_query = "INSERT INTO proficiency_skills (skill_name, skill_description, skill_effects, skill_type) VALUES ('sword mastery','A useful trait for any survivalist is the ability to chop wood.','Allows players to cut trees equivalent to their skill level.','combat')"
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
