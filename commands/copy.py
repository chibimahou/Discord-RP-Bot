# import discord
# import sys
# import sqlite3
# import os
# import re
# import function_calls.inventory
# from discord.ext import commands
# from discord import app_commands
# from discord.utils import get

# print("Hello")
# client = commands.Bot(command_prefix="!", intents = discord.Intents.all())

# @client.event
# async def on_ready():
#     print('We have logged in as {0.user}'.format(client))

# @commands.command()
# async def sync(self, ctx) -> None:
#    fmt = await ctx.bot.tree.sync()
#    await ctx.send(
#       f"Synced {len(fmt)} command to the current guild."
#    )
#    return

# @client.command()
# async def addrole(ctx, member : discord.Member, role : discord.Role):
#     await member.add_roles(role)


# @client.tree.command(name="hello", description="Hello!")
# async def hello(interaction: discord.Interaction):
#         await client.tree.sync()
#         print(f'Command tree synced.')

# @client.tree.command(name="test")
# async def test(interaction: discord.Interaction):
#     await interaction.response.send_message(f"Hey {interaction.user.mention}! This is a slash command!" )

# @client.tree.command(name="character")
# @app_commands.describe(character_name = "kirito!")
# async def character(interaction: discord.Interaction, character_name: str):
#         sqliteConnection = sqlite3.connect('characterSheet.db')
#         cursor = sqliteConnection.cursor()
#         character_information = cursor.execute("SELECT * FROM charactersheets WHERE nickname = '" + character_name + "'").fetchall()
#         col = str(character_information[0][17])
#         exp = str(character_information[0][18])
#         level = str(character_information[0][19])
#         strength = str(character_information[0][20])
#         defense = str(character_information[0][21])
#         speed = str(character_information[0][22])

#         cursor.close()
#         await interaction.response.send_message('```real name:                    ** ' + character_information[0][1] + ' ' + character_information[0][2] + ' **\nheight:                       ** ' + character_information[0][3] + ' **\nsize:                         ** ' + character_information[0][4]  + ' **\nage:                          ** ' + character_information[0][5] + ' **\nbirthday:                     ** ' + character_information[0][12] + ' **\nbio:                          ** ' + character_information[0][8] + ' **\n\nusername:                     ** ' + character_information[0][13] + ' **                            cursor color: ** ' + character_information[0][11] + ' **\nlevel:                        ** ' + level + ' **\nexperience:                   ** ' +  exp + ' **\nstr: ** ' + strength + ' ** def: ** ' + defense + ' **spd: ** ' + speed + ' **                                       col: ** ' + col +  ' **\nclass:                        ** ' + character_information[0][10] + ' **\ncurrently equipped weapon:    ** ' + character_information[0][16] + ' **\nstatus:                       ** ' + character_information[0][15] + ' **\nguild:                        ** ' + character_information[0][9] + ' **\n\nskill list:\n\n** ' + character_information[0][6] + ' **\n\nunique skills:\n\n** ' +  character_information[0][14] + ' **\n\ninventory:\n\n** ' + character_information[0][7] + ' **```')

# #Display Character stat screen.
# @client.tree.command(name="stat_screen")
# @app_commands.describe(character_name = "Hello!")
# async def stat_screen(interaction: discord.Interaction, character_name: str):

#         sqliteConnection = sqlite3.connect('characterSheet.db')
#         cursor = sqliteConnection.cursor()
#         character_information = cursor.execute("SELECT * FROM charactersheets WHERE firstName = '" + character_name + "'").fetchall()
#         cursor.close()
#         await interaction.response.send_message('```' + character_information[0][0] + character_information[0][1] + '\n' + character_information[0][2] + '\n' + character_information[0][3] + '\n' + character_information[0][4] + '\n' + character_information[0][5] + '\n' + character_information[0][6] + '\n' + character_information[0][7] + '\n' + character_information[0][8] + '\n' + character_information[0][9] + '\n' + character_information[0][10] + '\n' + character_information[0][11] + '\n' + character_information[0][12] + '\n' + character_information[0][13] + '\n' + character_information[0][14] + '```')



# #Display Character stat screen.
# @client.tree.command(name="add_character")
# @app_commands.describe(first_name="john", last_name="doe", ingame_name="Kirito", height="5.2", physique="muscular",  age="12", birthday="1/2/22", bio="A young boy who loves vrmmos.", level="1")
# async def add_Character(interaction: discord.Interaction, first_name:str, last_name:str, ingame_name:str, height:str, physique:str,  age:str, birthday:str, bio:str, level: str):

#         sqliteConnection = sqlite3.connect('characterSheet.db')
#         cursor = sqliteConnection.cursor()
#         character_information = cursor.execute("INSERT INTO charactersheets(firstName, lastName, nickname, height, size, age, birthday, playerStatus, guild, class, skillList, uniqueSkills, currentWeaponEquipped, playerColor, inventory, bio, col, experience, level, str, def, spd) VALUES ('" + first_name + "','" + last_name + "','" + ingame_name + "','" + height + "','" + physique + "','" + age + "','" + birthday + "','normal','guild','class','skill list','unique skills','weapon equipped','green', '1','" + bio + "','0','0','" + level + "','1','2','3'" + ")")
#         sqliteConnection.commit()
#         print(first_name)
#         cursor.close()
#         print(last_name)

#         await interaction.response.send_message('``` Character created. Welcome to Sword Art Online!```')

# #Display Character stat screen.
# @client.tree.command(name="inventory")
# @app_commands.describe(character_name = "Hello!")
# async def inventory(interaction: discord.Interaction, character_name: str):
#         sqliteConnection = sqlite3.connect('characterSheet.db')
#         cursor = sqliteConnection.cursor()
#         character_information = cursor.execute("SELECT inventory FROM charactersheets WHERE nickname = '" + character_name + "'").fetchall()
#         cursor.close()
#      #   character_inventory = character_information[0][0].replace(", ", "\n")
#         character_inventory = character_information[0][0]

#         await interaction.response.send_message('```' + character_inventory + '```')

# #Display Character stat screen.
# @client.tree.command(name="change_weapon")
# @app_commands.describe(character_name = "Hello!")
# async def change_weapon(interaction: discord.Interaction, character_name: str):
#         sqliteConnection = sqlite3.connect('characterSheet.db')
#         cursor = sqliteConnection.cursor()
#         character_information = cursor.execute("SELECT currentWeaponEquipped FROM charactersheets WHERE nickname = '" + character_name + "'").fetchall()
#         cursor.close()
#         await interaction.response.send_message('```' + character_name + ' currently equipped weapon: ' + character_information[0][0] + '```')

# #Display Character stat screen.
# @client.tree.command(name="add_inventory")
# @app_commands.describe(character_name = "Kirito", items_to_add = "1,2")
# async def add_inventory(interaction: discord.Interaction, character_name: str, items_to_add: str):
#             results = inventory.add_inventory()
#             await interaction.response.send_message('```' + results + '```')

# #Display Character stat screen.
# @client.tree.command(name="remove_inventory")
# @app_commands.describe(character_name = "Hello!", items_to_remove = "1,2")
# async def remove_inventory(interaction: discord.Interaction, character_name: str, items_to_remove: str):
#         sqliteConnection = sqlite3.connect('characterSheet.db')
#         cursor = sqliteConnection.cursor()
#         character_inventory = cursor.execute("SELECT inventory FROM charactersheets WHERE nickname = '" + character_name + "'").fetchall()       
#         old_inventory = str(character_inventory[0][0]).split(",")
#         old_inventory_length = len(old_inventory)
#         items_to_add_remove_spaces = items_to_remove.replace(", ", ",")
#         items_to_add_remove_spaces = items_to_add_remove_spaces.replace(" ,", ",")
#         new_items = items_to_add_remove_spaces.split(",")
#         print("Items to add: " + items_to_remove)
#         print("new_items" + new_items[0][0])
#         new_items_length = len(new_items)
#         new_inventory = ""
#         temp = 0
#         temp2 = 0

#         for temp in range(old_inventory_length):
#             print("old inventory: " + str(temp) + " out of: " + str(old_inventory_length))
#             for temp2 in range(new_items_length):
#                 if old_inventory[temp] != new_items[temp2]:
#                     if old_inventory_length != temp:
#                         new_inventory = new_inventory + old_inventory[temp] + ","
#                     else:
#                         new_inventory = new_inventory + old_inventory[temp] + ","

#                 else:
#                     old_inventory_length = old_inventory_length - 1
#         try:

#             cursor.execute("UPDATE charactersheets SET inventory = '" + new_inventory + "' WHERE nickname = '" + character_name + "'").fetchall()
#             sqliteConnection.commit()
#             character_information = cursor.execute("SELECT inventory FROM charactersheets WHERE nickname = '" + character_name + "'").fetchall()       
#             sqliteConnection.commit()
#             cursor.close()

#             await interaction.response.send_message('```' + 'Your updated inventory is: \n' + str(character_information[0][0]) + '```')
#         except:
#             print("Invalid character entered.")
#         await interaction.response.send_message('``` Character created. Welcome to Sword Art Online!```')

# #Display Character stat screen.
# @client.tree.command(name="experience")
# @app_commands.describe(character_name = "Kirito", experience_to_add = "10")
# async def experience(interaction: discord.Interaction, character_name: str, experience_to_add: str):
#         sqliteConnection = sqlite3.connect('characterSheet.db')
#         cursor = sqliteConnection.cursor()
#         character_information = cursor.execute("SELECT charactersheets.level, charactersheets.experience, experience.experience FROM charactersheets INNER JOIN experience ON charactersheets.level = experience.level WHERE charactersheets.nickname = '" + character_name + "';").fetchall()
#         character_level = str(character_information[0][0])
#         character_experience_to_level = str(character_information[0][2] - character_information[0][1])

#         await interaction.response.send_message('```' + 'Your current level is: ' + character_level + '. You need ' + character_experience_to_level + ' experience to level up.```')

# #Display Character stat screen. 
# @client.tree.command(name="add_experience")
# @app_commands.describe(character_name = "Hello!", experience_to_add = "20")
# async def add_experience(interaction: discord.Interaction, character_name: str, experience_to_add: str):
#         sqliteConnection = sqlite3.connect('characterSheet.db')
#         cursor = sqliteConnection.cursor()
#         character_current_experience = cursor.execute("SELECT experience, level FROM charactersheets WHERE nickname = '" + character_name + "'").fetchall()
#         experience = str(int(experience_to_add) + character_current_experience[0][0])
#         level = character_current_experience[0][1]
#         cursor.execute("UPDATE charactersheets SET experience = '" + experience + "' WHERE nickname = '" + character_name + "'").fetchall()
#         sqliteConnection.commit()
#         character_information = cursor.execute("SELECT charactersheets.level, charactersheets.experience, experience.experience FROM charactersheets INNER JOIN experience ON charactersheets.level = experience.level WHERE charactersheets.nickname = '" + character_name + "';").fetchall()
#         print(str(character_information[0][1]) + " " + str(character_information[0][2]))
#         if character_information[0][1] >= character_information[0][2]:
#            level = str(level + 1)
#            cursor.execute("UPDATE charactersheets SET level = '" + level + "' WHERE nickname = '" + character_name + "'").fetchall()
#            sqliteConnection.commit()
#            character_information = cursor.execute("SELECT charactersheets.level, charactersheets.experience, experience.experience FROM charactersheets INNER JOIN experience ON charactersheets.level = experience.level WHERE charactersheets.nickname = '" + character_name + "';").fetchall()
#            new_level = str(level)
#            character_experience_to_level = str(character_information[0][2] - character_information[0][1])
#            await interaction.response.send_message('```' + 'Congratulations, You leveled up! Your current level is: ' + new_level + '. You need ' + character_experience_to_level + ' experience to level up.```')

#         else:
#            character_level = str(character_information[0][0])
#            character_experience_to_level = str(character_information[0][2] - character_information[0][1])
#         await interaction.response.send_message('```' + 'Your current level is: ' + character_level + '. You need ' + character_experience_to_level + ' experience to level up.```')

# #Display Character stat screen.
# @client.tree.command(name="remove_experience")
# @app_commands.describe(character_name = "Hello!", experience_earned = "20")
# async def remove_experience(interaction: discord.Interaction, character_name: str, experience_earned: str):
#         sqliteConnection = sqlite3.connect('characterSheet.db')
#         cursor = sqliteConnection.cursor()
#         character_current_experience = cursor.execute("SELECT experience, level FROM charactersheets WHERE nickname = '" + character_name + "'").fetchall()
#         experience = str(character_current_experience[0][0] - int(experience_earned))
#         level = character_current_experience[0][1]
#         last_level = str(character_current_experience[0][1] - 1)
#         print("experience: " + str(experience) + " level: " + str(level) + " last level: " + str(last_level))
#         cursor.execute("UPDATE charactersheets SET experience = '" + experience + "' WHERE nickname = '" + character_name + "'").fetchall()
#         sqliteConnection.commit()
#         character_information = cursor.execute("SELECT charactersheets.level, charactersheets.experience, experience.experience FROM charactersheets INNER JOIN experience ON charactersheets.level = experience.level WHERE nickname = '" + character_name + "';").fetchall()
#         character_previous_level = cursor.execute("SELECT experience FROM experience WHERE level = " + last_level + "").fetchall()
#         experience_to_level = character_previous_level[0][0]
#         print("experience to level: " + str(experience_to_level) + "character_experience: " + str(character_information[0][1]))

#         if character_information[0][1] < experience_to_level:
#            level = str(level - 1)
#            cursor.execute("UPDATE charactersheets SET level = '" + level + "' WHERE nickname = '" + character_name + "'").fetchall()
#            sqliteConnection.commit()
#            character_information = cursor.execute("SELECT charactersheets.level, charactersheets.experience, experience.experience FROM charactersheets INNER JOIN experience ON charactersheets.level = experience.level WHERE nickname = '" + character_name + "';").fetchall()
#            new_level = str(level)
#            character_experience_to_level = str(character_information[0][2] - character_information[0][1])
#            print(str(character_information[0][2]) + " " + str(character_information[0][1]))
#            print("new level: " + str(new_level) + " level: " + str(level) + " experience to level: " + str(character_experience_to_level))

#            await interaction.response.send_message('```' + 'Your level has been reduced. Your current level is: ' + new_level + '. You need ' + character_experience_to_level + ' experience to level up.```')
#         else:
#             character_level = str(character_information[0][0])
#             character_experience_to_level = str(character_information[0][2] - character_information[0][1])
#             await interaction.response.send_message('```' + 'Your current level is: ' + character_level + '. You need ' + character_experience_to_level + ' experience to level up.```')

# #Display Character stat screen.
# @client.tree.command(name="add_stat")
# @app_commands.describe(character_name = "Hello!", stat = "str", points_to_add = "2")
# async def add_stat(interaction: discord.Interaction, character_name: str, stat: str, points_to_add: str):
#         sqliteConnection = sqlite3.connect('characterSheet.db')
#         cursor = sqliteConnection.cursor()
#         character_current_stat = cursor.execute("SELECT " + stat + " FROM charactersheets WHERE nickname = '" + character_name + "'").fetchall()
#         previous_stat = character_current_stat[0][0]
#         new_stat = str(previous_stat + int(points_to_add))
#         cursor.execute("UPDATE charactersheets SET " + stat + " = '" + new_stat + "' WHERE nickname = '" + character_name + "'").fetchall()
#         sqliteConnection.commit()
#         await interaction.response.send_message('```' + 'Your new ' + stat + ' is: ' + new_stat + '.```')

# #Display Character stat screen.
# @client.tree.command(name="remove_stat")
# @app_commands.describe(character_name = "Hello!", stat = "str", points_to_remove = "2")
# async def remove_stat(interaction: discord.Interaction, character_name: str, stat: str, points_to_remove: str):
#         sqliteConnection = sqlite3.connect('characterSheet.db')
#         cursor = sqliteConnection.cursor()
#         character_current_stat = cursor.execute("SELECT " + stat + " FROM charactersheets WHERE nickname = '" + character_name + "'").fetchall()
#         previous_stat = character_current_stat[0][0]
#         new_stat = str(previous_stat - int(points_to_remove))
#         cursor.execute("UPDATE charactersheets SET " + stat + " = '" + new_stat + "' WHERE nickname = '" + character_name + "'").fetchall()
#         sqliteConnection.commit()
#         await interaction.response.send_message('```' + 'Your new ' + stat + ' is: ' + new_stat + '.```')

# #Display Character stat screen.
# @client.tree.command(name="add_col")
# @app_commands.describe(character_name = "Kirito", col_to_add = "20")
# async def add_col(interaction: discord.Interaction, character_name: str, col_to_add: str):

#         sqliteConnection = sqlite3.connect('characterSheet.db')
#         cursor = sqliteConnection.cursor()
#         character_current_stat = cursor.execute("SELECT col FROM charactersheets WHERE nickname = '" + character_name + "'").fetchall()
#         previous_col = character_current_stat[0][0]
#         new_col_ammount = str(previous_col + int(col_to_add))
#         cursor.execute("UPDATE charactersheets SET col = '" + new_col_ammount + "' WHERE nickname = '" + character_name + "'").fetchall()
#         sqliteConnection.commit()
#         await interaction.response.send_message('```' + 'Your new col ammount is: ' + new_col_ammount + '.```')

# #Display Character stat screen.
# @client.tree.command(name="remove_col")
# @app_commands.describe(character_name = "Kirito",  col_to_remove = "20")
# async def remove_col(interaction: discord.Interaction, character_name: str, col_to_remove: str):
#         sqliteConnection = sqlite3.connect('characterSheet.db')
#         cursor = sqliteConnection.cursor()
#         character_current_stat = cursor.execute("SELECT col FROM charactersheets WHERE nickname = '" + character_name + "'").fetchall()
#         previous_col = character_current_stat[0][0]
#         new_col_ammount = str(previous_col - int(col_to_remove))
#         cursor.execute("UPDATE charactersheets SET col = '" + new_col_ammount + "' WHERE nickname   = '" + character_name + "'").fetchall()
#         sqliteConnection.commit()
#         await interaction.response.send_message('```' + 'Your new col ammount is: ' + new_col_ammount + '.```')

# #Display Character stat screen.
# @client.tree.command(name="check_items")
# @app_commands.describe(item_name = "Healing potion")
# async def check_items(interaction: discord.Interaction, item_name: str):
#         sqliteConnection = sqlite3.connect('characterSheet.db')
#         cursor = sqliteConnection.cursor()
#         character_information = cursor.execute("SELECT * FROM items WHERE item = '" + item_name + "'").fetchall()
#         await interaction.response.send_message('```' + 'The item you selected is: ' + character_information[0][1] + ' ' + character_information[0][2] + ' ' + character_information[0][3] + character_information[0][4] + '```')

# #Display Character stat screen.
# @client.tree.command(name="add_skills")
# @app_commands.describe(character_name = "Kirito", skill_name = "Vorpal Slash")
# async def add_skills(interaction: discord.Interaction,character_name: str, skill_name: str):
#         sqliteConnection = sqlite3.connect('characterSheet.db')
#         cursor = sqliteConnection.cursor()
#         character_skills = cursor.execute("SELECT skilllist FROM characterSheets WHERE nickname = '" + character_name + "'").fetchall()
#         skill_name_lower = skill_name.lower()
#         old_skills = str(character_skills[0][0]).split(",")
#         old_skills_length = len(old_skills)
#         new_skills = ""
#         temp = 0
#         for temp in range(old_skills_length):
#                 if old_skills[temp] != skill_name_lower and temp < old_skills_length - 1:
#                        new_skills = new_skills + old_skills[temp] + "," 
#                 elif old_skills[temp] != skill_name_lower and temp == old_skills_length - 1:
#                        new_skills = new_skills + old_skills[temp] + "," 
#                        new_skills = new_skills + skill_name_lower
#                 else:
#                        await interaction.response.send_message('```' + 'The skill: ' + skill_name_lower + ' is already in your skill list.' + '```')

#         cursor.execute("UPDATE charactersheets SET skilllist = '" + new_skills + "' WHERE nickname = '" + character_name + "'").fetchall()
#         sqliteConnection.commit()
#         await interaction.response.send_message('```' + 'The skill: ' + skill_name_lower + ' has been added. Your new skill list is: \n\n' + new_skills + '```')

# #Display Character stat screen.
# @client.tree.command(name="remove_skills")
# @app_commands.describe(character_name = "Kirito", skill_name = "Vorpal Strike")
# async def remove_skills(interaction: discord.Interaction, character_name: str, skill_name: str):
#         sqliteConnection = sqlite3.connect('characterSheet.db')
#         cursor = sqliteConnection.cursor()
#         character_skills = cursor.execute("SELECT skilllist FROM characterSheets WHERE nickname = '" + character_name + "'").fetchall()
#         skill_name_lower = skill_name.lower()
#         old_skills = str(character_skills[0][0]).split(",")
#         old_skills_length = len(old_skills)
#         new_skills = ""
#         temp = 0
#         for temp in range(old_skills_length):
#                 if old_skills[temp] != skill_name_lower and temp < old_skills_length - 1:
#                        new_skills = new_skills + old_skills[temp] + "," 
#                 elif old_skills[temp] != skill_name_lower and temp == old_skills_length:
#                         new_skills = new_skills + old_skills[temp]
#                         await interaction.response.send_message('```' + 'The skill: ' + skill_name_lower + ' does not exist.' + '```')
#                 elif old_skills[temp] == skill_name_lower and temp != old_skills_length - 1:
#                         new_skills = new_skills + ""
#                 else:
#                         new_skills = new_skills[:-1]
#         cursor.execute("UPDATE charactersheets SET skilllist = '" + new_skills + "' WHERE nickname = '" + character_name + "'").fetchall()
#         sqliteConnection.commit()
#         await interaction.response.send_message('```' + 'The skill: ' + skill_name_lower + ' has been removed. Your new skill list is: \n\n' + new_skills + '```')

# #Run the client.
# client.run("MTAwNjM4NTMzNDEwOTYyMjMzNA.GCL0zu.BQZnjK71yc6QpzXYGRWj1NzdQLAuvO1c_67OVg")