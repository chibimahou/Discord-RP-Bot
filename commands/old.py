import discord
import sqlite3
import os

print("Hello")
client = discord.Client()

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return
#Say Hello.
    if message.content.startswith('$hello'):
        await message.channel.send('Hello!')
    
#Display Character information.
    if message.content.startswith('!character'):
        await message.channel.send('```' + 'Please input your character name.' + '```')
        def check(msg):
           return msg.author == message.author and msg.channel == message.channel

        msg = await client.wait_for("message", check=check)

        sqliteConnection = sqlite3.connect('characterSheet.db')
        cursor = sqliteConnection.cursor()
        character_information = cursor.execute("SELECT * FROM charactersheets WHERE firstName = '" + msg.content + "'").fetchall()
        col = str(character_information[0][16])
        exp = str(character_information[0][17])
        level = str(character_information[0][18])
        strength = str(character_information[0][19])
        defense = str(character_information[0][20])
        speed = str(character_information[0][21])

        cursor.close()
        await message.channel.send('```real name:                    ** ' + character_information[0][0] + ' ' + character_information[0][1] + ' **\nheight:                       ** ' + character_information[0][2] + ' **\nsize:                         ** ' + character_information[0][3]  + ' **\nage:                          ** ' + character_information[0][4] + ' **\nbirthday:                     ** ' + character_information[0][11] + ' **\nbio:                          ** ' + character_information[0][7] + ' **\n\nusername:                     ** ' + character_information[0][12] + ' **                            cursor color: ** ' + character_information[0][10] + ' **\nlevel:                        ** ' + level + ' **\nexperience:                   ** ' +  exp + ' **\nstr: ** ' + strength + ' ** def: ** ' + defense + ' **spd: ** ' + speed + ' **                                       col: ** ' + col +  ' **\nclass:                        ** ' + character_information[0][9] + ' **\ncurrently equipped weapon:    ** ' + character_information[0][15] + ' **\nstatus:                       ** ' + character_information[0][14] + ' **\nguild:                        ** ' + character_information[0][8] + ' **\n\nskill list:\n\n** ' + character_information[0][5] + ' **\n\nunique skills:\n\n** ' +  character_information[0][13] + ' **\n\ninventory:\n\n** ' + character_information[0][6] + ' **```')

#Display Character stat screen.
    if message.content.startswith('stat_screen'):
        await message.channel.send('```' + 'Please input your character name.' + '```')
        def check(msg):
           return msg.author == message.author and msg.channel == message.channel

        msg = await client.wait_for("message", check=check)

        sqliteConnection = sqlite3.connect('characterSheet.db')
        cursor = sqliteConnection.cursor()
        character_information = cursor.execute("SELECT * FROM charactersheets WHERE firstName = '" + msg.content + "'").fetchall()
        cursor.close()
        await message.channel.send('```' + character_information[0][0] + character_information[0][1] + '\n' + character_information[0][2] + '\n' + character_information[0][3] + '\n' + character_information[0][4] + '\n' + character_information[0][5] + '\n' + character_information[0][6] + '\n' + character_information[0][7] + '\n' + character_information[0][8] + '\n' + character_information[0][9] + '\n' + character_information[0][10] + '\n' + character_information[0][11] + '\n' + character_information[0][12] + '\n' + character_information[0][13] + '\n' + character_information[0][14] + '```')

#Add Character Sheet to the database. MODS ONLY.
    if message.content.startswith('!add_Character'):
        #First Name
        await message.channel.send('```' + 'Please input the characters first name:' + '```')
        def check(msg):
           return msg.author == message.author and msg.channel == message.channel

        msg = await client.wait_for("message", check=check)

        first_name = msg.content

        #Last Name
        await message.channel.send('```' + 'Please input the characters last name:' + '```')
        def check(msg):
           return msg.author == message.author and msg.channel == message.channel

        msg = await client.wait_for("message", check=check)

        last_name = msg.content
        #Nickname
        await message.channel.send('```' + 'Please input the characters nickname:' + '```')
        def check(msg):
           return msg.author == message.author and msg.channel == message.channel 

        msg = await client.wait_for("message", check=check)

        nickname = msg.content

        #Nickname
        await message.channel.send('```' + 'Please input the characters height:' + '```')
        def check(msg):
           return msg.author == message.author and msg.channel == message.channel 

        msg = await client.wait_for("message", check=check)

        height = msg.content

        #size
        await message.channel.send('```' + 'Please input the characters size:' + '```')
        def check(msg):
           return msg.author == message.author and msg.channel == message.channel 

        msg = await client.wait_for("message", check=check)

        size = msg.content

        #Age
        await message.channel.send('```' + 'Please input the characters age:' + '```')
        def check(msg):
           return msg.author == message.author and msg.channel == message.channel

        msg = await client.wait_for("message", check=check)

        age = msg.content

        #birthday
        await message.channel.send('```' + 'Please input the characters birthday:' + '```')
        def check(msg):
           return msg.author == message.author and msg.channel == message.channel 

        msg = await client.wait_for("message", check=check)

        birthday = msg.content

        #bio
        await message.channel.send('```' + 'Please input the characters bio:' + '```')
        def check(msg):
           return msg.author == message.author and msg.channel == message.channel 

        msg = await client.wait_for("message", check=check)

        bio = msg.content

         #level
        await message.channel.send('```' + 'Please input the characters level:' + '```')
        def check(msg):
           return msg.author == message.author and msg.channel == message.channel 

        msg = await client.wait_for("message", check=check)

        level = msg.content

        sqliteConnection = sqlite3.connect('characterSheet.db')
        cursor = sqliteConnection.cursor()
        character_information = cursor.execute("INSERT INTO charactersheets(firstName, lastName, nickname, height, size, age, birthday, playerStatus, guild, class, skillList, uniqueSkills, currentWeaponEquipped, playerColor, inventory, bio, col, experience, level, str, def, spd) VALUES ('" + first_name + "','" + last_name + "','" + nickname + "','" + height + "','" + size + "','" + age + "','" + birthday + "','normal','guild','class','skill list','unique skills','weapon equipped','green','inventory','" + bio + "','0','0','" + level + "','1','2','3'" + ")")
        sqliteConnection.commit()
        print(first_name)
        cursor.close()
        print(last_name)

        await message.channel.send('``` Character created. Welcome to Sword Art Online!```')
#Check inventory
    if message.content.startswith('!inventory'):
        await message.channel.send('```' + 'Please input your character name.' + '```')
        def check(msg):
           return msg.author == message.author and msg.channel == message.channel

        msg = await client.wait_for("message", check=check)

        sqliteConnection = sqlite3.connect('characterSheet.db')
        cursor = sqliteConnection.cursor()
        character_information = cursor.execute("SELECT inventory FROM charactersheets WHERE firstName = '" + msg.content + "'").fetchall()
        cursor.close()
     #   character_inventory = character_information[0][0].replace(", ", "\n")
        character_inventory = character_information[0][0]

        await message.channel.send('```' + character_inventory + '```')


#Change currently equipped item
    if message.content.startswith('!change_weapon'):
        await message.channel.send('```' + 'Please input your character name.' + '```')
        def check(msg):
           return msg.author == message.author and msg.channel == message.channel

        msg = await client.wait_for("message", check=check)

        sqliteConnection = sqlite3.connect('characterSheet.db')
        cursor = sqliteConnection.cursor()
        character_information = cursor.execute("SELECT currentWeaponEquipped FROM charactersheets WHERE firstName = '" + msg.content + "'").fetchall()
        cursor.close()
        await message.channel.send('```' + msg.content + ' currently equipped weapon: ' + character_information[0][0] + '```')

#Update inventory
    if message.content.startswith('!add_inventory'):
        await message.channel.send('```' + 'Please input your character name.' + '```')
        def check(msg):
           return msg.author == message.author and msg.channel == message.channel

        msg = await client.wait_for("message", check=check)

        characterName = msg.content
        sqliteConnection = sqlite3.connect('characterSheet.db')
        cursor = sqliteConnection.cursor()
        character_information = cursor.execute("SELECT inventory FROM charactersheets WHERE firstName = '" + msg.content + "'").fetchall()
        character_new_inventory = character_information[0][0]
        character_inventory = character_information[0][0].replace(", ", "\n")
        character_name = msg.content
        await message.channel.send('```' + 'Your inventory is: \n' + character_inventory + '\nWhat would you like to add?' '```')
        def check(msg):
           return msg.author == message.author and msg.channel == message.channel 

        msg = await client.wait_for("message", check=check)
        character_new_inventory = character_new_inventory + ', ' + msg.content + ', '
        character_information = cursor.execute("UPDATE charactersheets SET inventory = '" + character_new_inventory + "' WHERE firstName = '" + character_name + "'").fetchall()
        sqliteConnection.commit()
        cursor.close()
        character_new_inventory = character_new_inventory.replace(", ", "\n")

        await message.channel.send('```' + 'Your updated inventory is: \n' + character_new_inventory + '```')

#remove inventory
    if message.content.startswith('!remove_inventory'):
        await message.channel.send('```' + 'Please input your character name.' + '```')
        def check(msg):
           return msg.author == message.author and msg.channel == message.channel

        msg = await client.wait_for("message", check=check)

        characterName = msg.content
        sqliteConnection = sqlite3.connect('characterSheet.db')
        cursor = sqliteConnection.cursor()
        character_information = cursor.execute("SELECT inventory FROM charactersheets WHERE firstName = '" + msg.content + "'").fetchall()
        new_character_inventory = character_information[0][0]
        character_inventory = character_information[0][0].replace(", ", "\n")
        character_name = msg.content
        await message.channel.send('```' + 'Your inventory is: \n' + character_inventory + '\nWhat would you like to remove?' + new_character_inventory + '```')
        def check(msg):
           return msg.author == message.author and msg.channel == message.channel 

        msg = await client.wait_for("message", check=check)
        new_character_inventory = new_character_inventory.replace(msg.content + ', ', "")
        character_information = cursor.execute("UPDATE charactersheets SET inventory = '" + new_character_inventory + "' WHERE firstName = '" + character_name + "'").fetchall()
        sqliteConnection.commit()
        cursor.close()
        character_new_inventory = new_character_inventory.replace(", ", "\n")

        await message.channel.send('```' + 'Your updated inventory is: \n' + character_new_inventory + '```')

#experience to next level
    if message.content.startswith('!experience'):
        await message.channel.send('```' + 'Please input your character name.' + '```')
        def check(msg):
           return msg.author == message.author and msg.channel == message.channel

        msg = await client.wait_for("message", check=check)

        characterName = msg.content
        sqliteConnection = sqlite3.connect('characterSheet.db')
        cursor = sqliteConnection.cursor()
        character_information = cursor.execute("SELECT charactersheets.level, charactersheets.experience, experience.experience FROM charactersheets INNER JOIN experience ON charactersheets.level = experience.level;").fetchall()
        character_level = str(character_information[0][0])
        character_experience_to_level = str(character_information[0][2] - character_information[0][1])
        character_name = msg.content
        await message.channel.send('```' + 'Your current level is: ' + character_level + '. You need ' + character_experience_to_level + ' experience to level up.```')

#add experience
    if message.content.startswith('!add_experience'):
        await message.channel.send('```' + 'Please input your character name.' + '```')
        def check(msg):
           return msg.author == message.author and msg.channel == message.channel

        msg = await client.wait_for("message", check=check)

        characterName = msg.content

        await message.channel.send('```' + 'Please input your experience earned.' + '```')
        def check(msg):
           return msg.author == message.author and msg.channel == message.channel

        msg = await client.wait_for("message", check=check)
        experience_earned = msg.content

        sqliteConnection = sqlite3.connect('characterSheet.db')
        cursor = sqliteConnection.cursor()
        character_current_experience = cursor.execute("SELECT experience, level FROM charactersheets WHERE firstName = '" + characterName + "'").fetchall()
        experience = str(int(experience_earned) + character_current_experience[0][0])
        level = character_current_experience[0][1]
        cursor.execute("UPDATE charactersheets SET experience = '" + experience + "' WHERE firstName = '" + characterName + "'").fetchall()
        sqliteConnection.commit()
        character_information = cursor.execute("SELECT charactersheets.level, charactersheets.experience, experience.experience FROM charactersheets INNER JOIN experience ON charactersheets.level = experience.level WHERE firstName = '" + characterName + "';").fetchall()
        if character_information[0][1] > character_information[0][2]:
           level = str(level + 1)
           cursor.execute("UPDATE charactersheets SET level = '" + level + "' WHERE firstName = '" + characterName + "'").fetchall()
           sqliteConnection.commit()
           character_information = cursor.execute("SELECT charactersheets.level, charactersheets.experience, experience.experience FROM charactersheets INNER JOIN experience ON charactersheets.level = experience.level;").fetchall()
           new_level = str(level)
           character_experience_to_level = str(character_information[0][2] - character_information[0][1])
           await message.channel.send('```' + 'Congratulations, You leveled up! Your current level is: ' + new_level + '. You need ' + character_experience_to_level + ' experience to level up.```')


        else:
         character_level = str(character_information[0][0])
         character_experience_to_level = str(character_information[0][2] - character_information[0][1])
         character_name = msg.content
         await message.channel.send('```' + 'Your current level is: ' + character_level + '. You need ' + character_experience_to_level + ' experience to level up.```')

#add stat
    if message.content.startswith('!add_stat'):
        await message.channel.send('```' + 'Please input your character name.' + '```')
        def check(msg):
           return msg.author == message.author and msg.channel == message.channel

        msg = await client.wait_for("message", check=check)

        characterName = msg.content

        await message.channel.send('```' + 'Please input the stat you want to increase \n' + 'str\nspd\ndef' + '```')
        def check(msg):
           return msg.author == message.author and msg.channel == message.channel

        msg = await client.wait_for("message", check=check)
        stat = msg.content

        await message.channel.send('```' + 'Please input the total points you want to distribute.' + '```')
        def check(msg):
           return msg.author == message.author and msg.channel == message.channel

        msg = await client.wait_for("message", check=check)
        points_to_distribute = msg.content
        sqliteConnection = sqlite3.connect('characterSheet.db')
        cursor = sqliteConnection.cursor()
        character_current_stat = cursor.execute("SELECT " + stat + " FROM charactersheets WHERE firstName = '" + characterName + "'").fetchall()
        previous_stat = character_current_stat[0][0]
        new_stat = str(previous_stat + int(points_to_distribute))
        cursor.execute("UPDATE charactersheets SET " + stat + " = '" + new_stat + "' WHERE firstName = '" + characterName + "'").fetchall()
        sqliteConnection.commit()
        await message.channel.send('```' + 'Your new ' + stat + ' is: ' + new_stat + '.```')

#remove stat
    if message.content.startswith('!remove_stat'):
        await message.channel.send('```' + 'Please input your character name.' + '```')
        def check(msg):
           return msg.author == message.author and msg.channel == message.channel

        msg = await client.wait_for("message", check=check)

        characterName = msg.content

        await message.channel.send('```' + 'Please input the stat you want to decrease \n' + 'str\nspd\ndef' + '```')
        def check(msg):
           return msg.author == message.author and msg.channel == message.channel

        msg = await client.wait_for("message", check=check)
        stat = msg.content

        await message.channel.send('```' + 'Please input the total points you want to remove.' + '```')
        def check(msg):
           return msg.author == message.author and msg.channel == message.channel

        msg = await client.wait_for("message", check=check)
        points_to_distribute = msg.content
        sqliteConnection = sqlite3.connect('characterSheet.db')
        cursor = sqliteConnection.cursor()
        character_current_stat = cursor.execute("SELECT " + stat + " FROM charactersheets WHERE firstName = '" + characterName + "'").fetchall()
        previous_stat = character_current_stat[0][0]
        new_stat = str(previous_stat - int(points_to_distribute))
        cursor.execute("UPDATE charactersheets SET " + stat + " = '" + new_stat + "' WHERE firstName = '" + characterName + "'").fetchall()
        sqliteConnection.commit()
        await message.channel.send('```' + 'Your new ' + stat + ' is: ' + new_stat + '.```')

#add col
    if message.content.startswith('!add_col'):
        await message.channel.send('```' + 'Please input your character name.' + '```')
        def check(msg):
           return msg.author == message.author and msg.channel == message.channel

        msg = await client.wait_for("message", check=check)

        characterName = msg.content

        await message.channel.send('```' + 'Please input the ammount of col you want to add.```')
        def check(msg):
           return msg.author == message.author and msg.channel == message.channel

        msg = await client.wait_for("message", check=check)
        col_to_add = msg.content
        sqliteConnection = sqlite3.connect('characterSheet.db')
        cursor = sqliteConnection.cursor()
        character_current_stat = cursor.execute("SELECT col FROM charactersheets WHERE firstName = '" + characterName + "'").fetchall()
        previous_col = character_current_stat[0][0]
        new_col_ammount = str(previous_col + int(col_to_add))
        cursor.execute("UPDATE charactersheets SET col = '" + new_col_ammount + "' WHERE firstName = '" + characterName + "'").fetchall()
        sqliteConnection.commit()
        await message.channel.send('```' + 'Your new col ammount is: ' + new_col_ammount + '.```')

#remove col
    if message.content.startswith('!remove_col'):
        await message.channel.send('```' + 'Please input your character name.' + '```')
        def check(msg):
           return msg.author == message.author and msg.channel == message.channel

        msg = await client.wait_for("message", check=check)

        characterName = msg.content

        await message.channel.send('```' + 'Please input the ammount of col you want to remove.```')
        def check(msg):
           return msg.author == message.author and msg.channel == message.channel

        msg = await client.wait_for("message", check=check)
        col_to_remove = msg.content
        sqliteConnection = sqlite3.connect('characterSheet.db')
        cursor = sqliteConnection.cursor()
        character_current_stat = cursor.execute("SELECT col FROM charactersheets WHERE firstName = '" + characterName + "'").fetchall()
        previous_col = character_current_stat[0][0]
        new_col_ammount = str(previous_col - int(col_to_remove))
        cursor.execute("UPDATE charactersheets SET col = '" + new_col_ammount + "' WHERE firstName = '" + characterName + "'").fetchall()
        sqliteConnection.commit()
        await message.channel.send('```' + 'Your new col ammount is: ' + new_col_ammount + '.```')


#remove experience
    if message.content.startswith('!remove_experience'):
        await message.channel.send('```' + 'Please input your character name.' + '```')
        def check(msg):
           return msg.author == message.author and msg.channel == message.channel

        msg = await client.wait_for("message", check=check)

        characterName = msg.content

        await message.channel.send('```' + 'Please input the experience you want to remove.' + '```')
        def check(msg):
           return msg.author == message.author and msg.channel == message.channel

        msg = await client.wait_for("message", check=check)
        experience_earned = msg.content

        sqliteConnection = sqlite3.connect('characterSheet.db')
        cursor = sqliteConnection.cursor()
        character_current_experience = cursor.execute("SELECT experience, level FROM charactersheets WHERE firstName = '" + characterName + "'").fetchall()
        experience = str(character_current_experience[0][0] - int(experience_earned))
        level = character_current_experience[0][1]
        last_level = str(character_current_experience[0][1] - 1)
        cursor.execute("UPDATE charactersheets SET experience = '" + experience + "' WHERE firstName = '" + characterName + "'").fetchall()
        sqliteConnection.commit()
        character_information = cursor.execute("SELECT charactersheets.level, charactersheets.experience, experience.experience FROM charactersheets INNER JOIN experience ON charactersheets.level = experience.level;").fetchall()
        character_previous_level = cursor.execute("SELECT experience FROM experience WHERE level = " + last_level + "").fetchall()
        experience_to_level = character_previous_level[0][0]
        if character_information[0][1] < experience_to_level:
           level = str(level - 1)
           cursor.execute("UPDATE charactersheets SET level = '" + level + "' WHERE firstName = '" + characterName + "'").fetchall()
           sqliteConnection.commit()
           character_information = cursor.execute("SELECT charactersheets.level, charactersheets.experience, experience.experience FROM charactersheets INNER JOIN experience ON charactersheets.level = experience.level;").fetchall()
           new_level = str(level)
           character_experience_to_level = str(character_information[0][2] - character_information[0][1])
           await message.channel.send('```' + 'Your level has been reduced. Your current level is: ' + new_level + '. You need ' + character_experience_to_level + ' experience to level up.```')


        else:
         character_level = str(character_information[0][0])
         character_experience_to_level = str(character_information[0][2] - character_information[0][1])
         character_name = msg.content
         await message.channel.send('```' + 'Your current level is: ' + character_level + '. You need ' + character_experience_to_level + ' experience to level up.```')

#remove experience
    if message.content.startswith('!items'):

        sqliteConnection = sqlite3.connect('characterSheet.db')
        cursor = sqliteConnection.cursor()
        character_current_experience = cursor.execute("SELECT * FROM items").fetchall()
        item_count = cursor.execute("SELECT COUNT(*) FROM items WHERE id = '1'").fetchall()
        for row in character_current_experience:
         print (row)
        await message.channel.send('```' + str(character_current_experience[0][0])  + '\n' + str(character_current_experience[1][0])  + '\n' + str(character_current_experience[2][0])  + '\n' + str(character_current_experience[3][0])  +  '\n' +str(character_current_experience[4][0])  + '\n' + str(character_current_experience[5][0]) + '\nItem Count for index 1: ' +  str(item_count[0][0]) + '```')


#Run the client.
client.run("MTAwNjM4NTMzNDEwOTYyMjMzNA.GCL0zu.BQZnjK71yc6QpzXYGRWj1NzdQLAuvO1c_67OVg")