#Insert Data into Table

import sqlite3

try:

    #1
    sqliteConnection = sqlite3.connect('characterSheet.db')
    cursor = sqliteConnection.cursor()
    print("Successfully Connected to SQLite")
    sqlite_insert_query = "INSERT INTO guilds (guild_name, guild_description, guild_approvers, guild_member_count) VALUES ('knights of the blood oath','A long running traditional skill allowing users to fish in any body of water.','kotori, kyzen', 2)"
    count = cursor.execute(sqlite_insert_query)
    sqlite_insert_query = "INSERT INTO guilds (guild_name, guild_description, guild_approvers, guild_member_count) VALUES ('moonlit black cats','A useful trait for any survivalist is the ability to chop wood.','kotori', 1)"
    count = cursor.execute(sqlite_insert_query) 
    sqlite_insert_query = "INSERT INTO guilds (guild_name, guild_description, guild_approvers, guild_member_count) VALUES ('moonlit pink cats','A useful trait for any survivalist is the ability to chop wood.','kotori', 1)"

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
