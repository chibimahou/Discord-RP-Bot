import discord
import sqlite3
import os
import re
import random
import function_calls.inventory as inv
import function_calls.invites as invi
import function_calls.spawns as spa
import function_calls.skills as ski
import function_calls.experience as exp
import function_calls.col as col
import function_calls.help as help
import function_calls.stats as sta
import function_calls.calc as mat
import function_calls.mod_commands as mod
import function_calls.combat as com
import function_calls.trade as tra
import function_calls.mod_normal_commands as modnormal
from discord.ext import commands
from discord import app_commands
from discord.utils import get

print("Hello")
client = commands.Bot(command_prefix="!", intents = discord.Intents.all())

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@commands.command()
async def sync(self, ctx) -> None:
   fmt = await ctx.bot.tree.sync()
   await ctx.send(
      f"Synced {len(fmt)} command to the current guild."
   )
   return

@client.command()
async def addrole(ctx, member : discord.Member, role : discord.Role):
    await member.add_roles(role)


@client.tree.command(name="hello", description="Hello!")
async def hello(interaction: discord.Interaction):
        await client.tree.sync()
        print(f'Command tree synced.')

@client.tree.command(name="test")
async def test(interaction: discord.Interaction):
    await interaction.response.send_message(f"Hey {interaction.user.mention}! This is a slash command!" )

@client.tree.command(name="character")
@app_commands.describe(character_name = "kirito!")
async def character(interaction: discord.Interaction, character_name: str):
        discord_tag = interaction.user.id
        results = sta.check_character(character_name, discord_tag)
        await interaction.response.send_message(results)

@client.tree.command(name="character_mod")
@app_commands.describe(character_name = "kirito!")
async def character_mod(interaction: discord.Interaction, character_name: str):
        results = modnormal.check_character_mods(character_name)
        await interaction.response.send_message(results)

#Display Character stat screen.
@client.tree.command(name="stat_screen")
@app_commands.describe(character_name = "Hello!")
async def stat_screen(interaction: discord.Interaction, character_name: str):
            discord_tag = interaction.user.id
            results = sta.stat_screen(character_name)
            await interaction.response.send_message(results)


#Display Character stat screen.
@client.tree.command(name="add_character")
@app_commands.describe(first_name="kirigaya", last_name="kazuto", ingame_name="Kirito", height="5'2\"", physique="muscular",  age="12", birthday="1/2/22", bio="A young boy who loves vrmmos.", level="1")
async def add_Character(interaction: discord.Interaction, first_name:str, last_name:str, ingame_name:str, height:str, physique:str,  age:str, birthday:str, bio:str, level: str):
            discord_tag = interaction.user.id
            print(discord_tag)
            results = sta.add_character(first_name, last_name, ingame_name, height, physique, age, birthday, bio, level, discord_tag)
            await interaction.response.send_message(results)

#Display Character stat screen.
@client.tree.command(name="finish_battle")
@app_commands.describe(character_name="kirigaya", mob_name="kazuto", number_defeated="Kirito")
async def finish_battle(interaction: discord.Interaction, character_name:str, mob_name:str, number_defeated:str):
            discord_tag = interaction.user.id
            print(discord_tag)
            results = spa.mob_drops(character_name, mob_name, number_defeated, discord_tag)
            await interaction.response.send_message(results)

#Display Character stat screen.
@client.tree.command(name="inventory")
@app_commands.describe(character_name = "Hello!")
async def inventory(interaction: discord.Interaction, character_name: str):
            discord_tag = interaction.user.id
            results = inv.inventory(character_name)
            await interaction.response.send_message(results)

#Display Character stat screen.
@client.tree.command(name="change_weapon")
@app_commands.describe(character_name = "Hello!")
async def change_weapon(interaction: discord.Interaction, character_name: str):
        discord_tag = interaction.user.id
        sqliteConnection = sqlite3.connect('characterSheet.db')
        cursor = sqliteConnection.cursor()
        character_information = cursor.execute("SELECT currentWeaponEquipped FROM charactersheets WHERE nickname = '" + character_name + "'").fetchall()
        cursor.close()
        await interaction.response.send_message('```' + character_name + ' currently equipped weapon: ' + character_information[0][0] + '```')

#Display Character stat screen.
@client.tree.command(name="add_inventory")
@app_commands.describe(character_name = "Kirito", items_to_add = "1,2")
async def add_inventory(interaction: discord.Interaction, character_name: str, items_to_add: str):
            discord_tag = interaction.user.id
            results = inv.add_inventory(character_name, items_to_add, discord_tag)
            await interaction.response.send_message(results)

#Display Character stat screen.
@client.tree.command(name="remove_inventory")
@app_commands.describe(character_name = "Hello!", items_to_remove = "1,2")
async def remove_inventory(interaction: discord.Interaction, character_name: str, items_to_remove: str):
            discord_tag = interaction.user.id
            results = inv.remove_inventory(character_name, items_to_remove, discord_tag)
            await interaction.response.send_message(results)
#Display Character stat screen.
@client.tree.command(name="add_skill")
@app_commands.describe(character_name = "Kirito", skill_to_add = "Fishing", skill_level = "1")
async def add_skill(interaction: discord.Interaction, character_name: str, skill_to_add: str, skill_level: str):
            discord_tag = interaction.user.id
            results = inv.add_inventory(character_name, skill_to_add)
            discord_tag = interaction.user.id
            if results == True:
                await interaction.response.send_message('```' + skill_to_add + ' has been successfully added to your inventory. ' + '```')
            else:    
                await interaction.response.send_message('``` Sorry, ' + skill_to_add + ' is not in your inventory. ' + '```')

#Display Character stat screen.
@client.tree.command(name="remove_skill")
@app_commands.describe(character_name = "Hello!", skill_to_remove = "Fishing", levels_to_remove = "1")
async def remove_skill(interaction: discord.Interaction, character_name: str, skill_to_remove: str, levels_to_remove: str):
            discord_tag = interaction.user.id
            results = ski.remove_skills(character_name, skill_to_remove)
            if results == True:
                await interaction.response.send_message('```' + skill_to_remove + ' has been successfully removed from your inventory. ' + '```')
            else:    
                await interaction.response.send_message('``` Sorry, ' + skill_to_remove + ' is not in your inventory. ' + '```')

#Display Character stat screen.
@client.tree.command(name="experience")
@app_commands.describe(character_name = "Kirito", experience_to_add = "10")
async def experience(interaction: discord.Interaction, character_name: str, experience_to_add: str):
            discord_tag = interaction.user.id
            results = exp.experience(character_name, experience_to_add)
            await interaction.response.send_message(results)

#Display Character stat screen. 
@client.tree.command(name="add_experience")
@app_commands.describe(character_name = "Hello!", experience_to_add = "20")
async def add_experience(interaction: discord.Interaction, character_name: str, experience_to_add: str):
            discord_tag = interaction.user.id
            results = exp.add_experience(character_name, experience_to_add)
            await interaction.response.send_message(results)

#Display Character stat screen.
@client.tree.command(name="remove_experience")
@app_commands.describe(character_name = "Hello!", experience_to_remove = "20")
async def remove_experience(interaction: discord.Interaction, character_name: str, experience_to_remove: str):
            discord_tag = interaction.user.id
            results = exp.remove_experience(character_name, experience_to_remove)
            await interaction.response.send_message(results)

#Display Character stat screen.
@client.tree.command(name="combat")
@app_commands.describe(character_name = "Hello!")
async def combat(interaction: discord.Interaction, character_name: str):
            discord_tag = interaction.user.id
            results = com.combat(character_name)
            await interaction.response.send_message(results)

#Display Character stat screen.
@client.tree.command(name="add_stat")
@app_commands.describe(character_name = "Hello!", stat = "str", points_to_add = "2")
async def add_stat(interaction: discord.Interaction, character_name: str, stat: str, points_to_add: str):
            discord_tag = interaction.user.id
            results = sta.add_stats(character_name, stat, points_to_add, discord_tag)
            await interaction.response.send_message(results)

#Display Character stat screen.
@client.tree.command(name="remove_stat")
@app_commands.describe(character_name = "Hello!", stat = "str", points_to_remove = "2")
async def remove_stat(interaction: discord.Interaction, character_name: str, stat: str, points_to_remove: str):
            discord_tag = interaction.user.id
            results = sta.remove_stats(character_name, stat, points_to_remove, discord_tag)
            await interaction.response.send_message(results)

#Display Character stat screen.
@client.tree.command(name="add_col")
@app_commands.describe(character_name = "Kirito", col_to_add = "20")
async def add_col(interaction: discord.Interaction, character_name: str, col_to_add: str):
            discord_tag = interaction.user.id
            results = col.add_col(character_name, col_to_add)
            await interaction.response.send_message(results)


#Display Character stat screen.
@client.tree.command(name="remove_col")
@app_commands.describe(character_name = "Kirito",  col_to_remove = "20")
async def remove_col(interaction: discord.Interaction, character_name: str, col_to_remove: str):
            discord_tag = interaction.user.id
            results = col.remove_col(character_name, col_to_remove)
            await interaction.response.send_message(results)

#Display Character stat screen.
@client.tree.command(name="check_items")
@app_commands.describe(item_name = "Healing potion")
async def check_items(interaction: discord.Interaction, item_name: str):
        discord_tag = interaction.user.id
        item_name_lower = item_name.lower()
        sqliteConnection = sqlite3.connect('characterSheet.db')
        cursor = sqliteConnection.cursor()
        character_information = cursor.execute("SELECT * FROM items WHERE item = '" + item_name_lower + "'").fetchall()
        await interaction.response.send_message('```' + 'The item you selected is: ' + character_information[0][1] + ' ' + character_information[0][2] + ' ' + character_information[0][3] + character_information[0][4] + '```')

#Display Character stat screen.
@client.tree.command(name="add_skills")
@app_commands.describe(character_name = "Kirito", skill_name = "Vorpal Slash")
async def add_skills(interaction: discord.Interaction,character_name: str, skill_name: str):
            discord_tag = interaction.user.id
            results = ski.add_skills(character_name, skill_name)
            await interaction.response.send_message(results)

#Display Character stat screen.
@client.tree.command(name="remove_skills")
@app_commands.describe(character_name = "Kirito", skill_name = "Vorpal Strike")
async def remove_skills(interaction: discord.Interaction, character_name: str, skill_name: str):
            discord_tag = interaction.user.id
            results = ski.remove_skills(character_name, skill_name)
            await interaction.response.send_message(results)

#Display Character stat screen.
@client.tree.command(name="send_guild_request")
@app_commands.describe(inviters_name = "Kirito", invitees_name = "Asuna", guild_name = "Moonlit black cats")
async def remove_skills(interaction: discord.Interaction, inviters_name: str, invitees_name: str, guild_name: str):
           discord_tag = interaction.user.id
           results = invi.request_guild_invite(inviters_name, invitees_name, guild_name)
           await interaction.response.send_message(results)

#Display Character stat screen.
@client.tree.command(name="accept_or_decline_guild_request")
@app_commands.describe(inviters_name = "Kirito", invitees_name = "Asuna", guild_name = "moonlit black cats", accept_or_decline = "accept")
async def accept_or_decline_guild_request(interaction: discord.Interaction, inviters_name: str, invitees_name: str, guild_name: str, accept_or_decline: str):
            discord_tag = interaction.user.id
            results = invi.accept_or_decline_guild_invite(inviters_name, invitees_name, guild_name, accept_or_decline)
            await interaction.response.send_message(results)

#Display Character stat screen.
@client.tree.command(name="send_party_invite")
@app_commands.describe(inviters_name = "Kirito", invitees_name = "Asuna")
async def send_party_invite(interaction: discord.Interaction, inviters_name: str, invitees_name: str):
            discord_tag = interaction.user.id
            results = invi.request_party_invite(inviters_name, invitees_name)
            await interaction.response.send_message(results)

#Display Character stat screen.
@client.tree.command(name="accept_or_decline_party_invite")
@app_commands.describe(inviters_name = "Kirito", invitees_name = "Asuna", accept_or_decline = "Accept")
async def accept_or_decline_party_invite(interaction: discord.Interaction, inviters_name: str, invitees_name: str, accept_or_decline: str):
            discord_tag = interaction.user.id
            results = invi.accept_or_decline_party_invite(inviters_name, invitees_name, accept_or_decline)
            await interaction.response.send_message(results)

#Display Character stat screen.
@client.tree.command(name="request_trade")
@app_commands.describe(character_name_a="Kirito", item_to_trade_a="herb", character_name_b="Asuna", item_to_trade_b="Bronze Ingot")
async def request_trade(interaction: discord.Interaction, character_name_a: str, item_to_trade_a: str, character_name_b: str, item_to_trade_b: str):
    discord_tag = interaction.user.id
    valid_trade = tra.trade(character_name_a, item_to_trade_a, character_name_b, item_to_trade_b)
    moderator_roles = [role for role in interaction.guild.roles if role.permissions.manage_messages]

    moderator_mentions = ' '.join([role.mention for role in moderator_roles])
    if valid_trade:
        await interaction.response.send_message(f"```{moderator_mentions}: {character_name_a} would like to trade: \n\n{item_to_trade_a} \n\n{character_name_b} would like to trade: \n\n{item_to_trade_b}. \n\nIf both players respond to this with an emote, that will confirm the trade: \n\nPlease ping a moderator to come and innitiate the trade.```"
        )
    else:
        await interaction.response.send_message("```Trade invalid: One player does not have the required item(s). Please verify your inventories.```")

#Display Character stat screen.
@client.tree.command(name="help_commands")
@app_commands.describe()
async def help_commands(interaction: discord.Interaction):
    results = help.help_commands()
    await interaction.response.send_message(results, ephemeral=True)

#Display Character stat screen.
@client.tree.command(name="help_damage")
@app_commands.describe()
async def help_damage(interaction: discord.Interaction):
    results = help.help_damage()
    await interaction.response.send_message(results, ephemeral=True)

#Display Character stat screen.
@client.tree.command(name="help_roleplay")
@app_commands.describe()
async def help_roleplay(interaction: discord.Interaction):
    results = help.help_roleplay()
    await interaction.response.send_message(results, ephemeral=True)

#Display Character stat screen.
@client.tree.command(name="add_proficiency_skill")
@app_commands.describe(character_name="Kirito", skill_to_add="woodcutting")
async def add_proficiency_skill(interaction: discord.Interaction, character_name: str, skill_to_add: str):
    discord_tag = interaction.user.id    
    results = ski.add_proficiency_skills(character_name, skill_to_add, discord_tag)
    await interaction.response.send_message(results, ephemeral=True)

#Display Character stat screen.
@client.tree.command(name="add_proficiency_level")
@app_commands.describe(character_name="Kirito", skill_to_add="woodcutting", points_to_add = "2")
async def add_proficiency_level(interaction: discord.Interaction, character_name: str, skill_to_add: str, points_to_add: str):
    discord_tag = interaction.user.id    
    results = ski.add_proficiency_level(character_name, skill_to_add, points_to_add, discord_tag)
    await interaction.response.send_message(results, ephemeral=True)

#Display Character stat screen.
@client.tree.command(name="remove_proficiency_skill")
@app_commands.describe(character_name="Kirito", skill_to_remove="woodcutting")
async def remove_proficiency_skill(interaction: discord.Interaction, character_name: str, skill_to_remove: str):
    discord_tag = interaction.user.id    
    results = ski.remove_proficiency_skills(character_name, skill_to_remove, discord_tag)
    await interaction.response.send_message(results, ephemeral=True)

@client.tree.command(name="spawn", description="Spawns a mob!")
@app_commands.describe(character_name = 'Kirito', floor = '1', area = 'something')
async def spawn(interaction: discord.Interaction, character_name: str, floor: str, area: str):
        discord_tag = interaction.user.id
        results = spa.spawn(floor, area)
        name = str(results[0][0])
        HealthPoints = str(results[0][1])
        strength  = str(results[0][2])
        DEX = str(results[0][3])
        SPE = str(results[0][4])
        drops = str(results[0][6]).lower()
        defense = str(results[0][7])
        random_monster_spawn = random.randint(1, 4)
        await interaction.response.send_message(results[0][5].format(character_name=character_name, spawns=name, HealthPoints=HealthPoints, strength=strength, Dexterity=DEX, Speed=SPE, Defense=defense, drops=drops, random_monster_spawn=random_monster_spawn))

@client.tree.command(name="calculate_combat_skill")
@app_commands.describe(character_name_a = "Kirito", character_name_b = "Asuna", weapon_name_a = "one handed bronze sword", skill_base_damage_a = "2.0", status_ailment_on_weapon_a = "poison", armor_base_defense_combined_b = "25",  skill_reduction_value_b = "15", material_modifier_armor_b = "1.0")
async def calculate_combat_skill(interaction: discord.Interaction, character_name_a: str, character_name_b: str, weapon_name_a: str, skill_base_damage_a: str, status_ailment_on_weapon_a: str, armor_base_defense_combined_b: str, skill_reduction_value_b: str, material_modifier_armor_b: str):
       discord_tag = interaction.user.id
       results = com.combat(character_name_a, character_name_b, 'yes', weapon_name_a, skill_base_damage_a, status_ailment_on_weapon_a, armor_base_defense_combined_b, skill_reduction_value_b, material_modifier_armor_b)
       await interaction.response.send_message (results)

@client.tree.command(name="calculate_combat_slash")
@app_commands.describe(character_name_a = "Kirito", character_name_b = "Asuna", weapon_name_a = "one handed bronze sword", status_ailment_on_weapon_a = "poison", armor_base_defense_combined_b = "25", material_modifier_armor_b = "1.0")
async def calculate_mob_combat_slash(interaction: discord.Interaction, character_name_a: str, character_name_b: str, weapon_name_a: str, status_ailment_on_weapon_a: str, armor_base_defense_combined_b: str, material_modifier_armor_b: str):
       discord_tag = interaction.user.id
       skill_use = "no"
       skill_a = "0"
       skill_reduction_b = "0"
       results = com.combat(character_name_a, character_name_b, 'no', weapon_name_a, skill_a, status_ailment_on_weapon_a, armor_base_defense_combined_b, skill_reduction_b, material_modifier_armor_b)
       await interaction.response.send_message (results)

@client.tree.command(name="calculate_mob_combat_skill")
@app_commands.describe(character_name_a = "Kirito", mob_name_b = "Asuna", weapon_name_a = "one handed bronze sword", skill_base_damage_a = "2.0", status_ailment_on_weapon_a = "poison")
async def calculate_mob_combat_skill(interaction: discord.Interaction, character_name_a: str, mob_name_b: str, weapon_name_a: str, skill_base_damage_a: str, status_ailment_on_weapon_a: str):
       discord_tag = interaction.user.id
       results = com.mob_combat(character_name_a, mob_name_b, 'yes', weapon_name_a, skill_base_damage_a, status_ailment_on_weapon_a)
       await interaction.response.send_message (results)

@client.tree.command(name="calculate_mob_combat_slash")
@app_commands.describe(character_name_a = "Kirito", mob_name_b = "Asuna", weapon_name_a = "one handed bronze sword", status_ailment_on_weapon_a = "poison")
async def calculate_mob_combat_slash(interaction: discord.Interaction, character_name_a: str, mob_name_b: str, weapon_name_a: str, status_ailment_on_weapon_a: str):
       discord_tag = interaction.user.id
       skill_a = "0"
       results = com.mob_combat(character_name_a, mob_name_b, 'no', weapon_name_a, skill_a, status_ailment_on_weapon_a)
       await interaction.response.send_message (results)

@client.tree.command(name="change_cursor_color")
@app_commands.describe(character_name_a = "Kirito", cursor_color="green")
async def change_cursor_color(interaction: discord.Interaction, character_name_a: str, cursor_color: str):
       discord_tag = interaction.user.id
       skill_a = "0"
       results = sta.cursor_color(character_name_a, cursor_color)
       await interaction.response.send_message (results)

@client.tree.command(name="confirm_trade")
@app_commands.describe(character_name_a = "Kirito", item_to_trade_a = "herb", character_name_b = "Asuna", item_to_trade_b = "Bronze Ingot" )
async def confirm_trade(interaction: discord.Interaction, character_name_a: str, item_to_trade_a: str, character_name_b: str, item_to_trade_b: str):
       discord_tag = interaction.user.id
       allowed_roles = ['executive', 'co-owner', 'owner', 'moderator']
       if mat.is_allowed(interaction.user.roles, allowed_roles):
         trade_completed = tra.accept_trade(character_name_a, item_to_trade_a, character_name_b, item_to_trade_b)
         if trade_completed == True:
           await interaction.response.send_message ('```The trade has been completed!```')
         else:
           await interaction.response.send_message ('```There seems to have been an issue with the trade.```')
       else:
           await interaction.response.send_message ('```You do not have permission to confirm trades.```')       

#Display Character stat screen.
@client.tree.command(name="add_character_mods")
@app_commands.describe(first_name="kirigaya", last_name="kazuto", ingame_name="Kirito", height="5'2\"", physique="muscular",  age="12", birthday="1/2/22", bio="A young boy who loves vrmmos.", level="1", skill_list = "vorpal strike, vorpal blade", inventory = "herb, bronze ingot", guild = "Moonlit black cats", character_class = "knight", player_color = "green", unique_skills = "dual wielding, holy shield", proficiency_skills = "fishing, one handed sword mastery", col = "100", experience = "100", strength = "100", defense = "100", speed = "100", dexterity = "100", player_status = "poisoned")
async def add_Character_mods(interaction: discord.Interaction, first_name:str, last_name:str, ingame_name:str, height:str, physique:str,  age:str, birthday:str, bio:str, level: str, skill_list: str, inventory: str, guild: str, character_class: str, player_color: str, unique_skills: str, proficiency_skills: str, col: str, experience: str, strength: str, defense: str, speed: str, dexterity: str, player_status: str):
        discord_tag = interaction.user.id
        allowed_roles = ['Executive Moderators', 'owners', 'bio manager']
        if mat.is_allowed(interaction.user.roles, allowed_roles):           
            results = mod.add_character(first_name, last_name, ingame_name, height, physique,  age, birthday, bio, level, skill_list, inventory, guild, character_class, player_color, unique_skills, proficiency_skills, col, experience, strength, defense, speed, dexterity, player_status)
            await interaction.response.send_message(results)

#Display Character stat screen.
@client.tree.command(name="remove_character_mods")
@app_commands.describe(ingame_name="Kirito")
async def remove_Character_mods(interaction: discord.Interaction, ingame_name:str):
        discord_tag = interaction.user.id
        allowed_roles = ['Executive Moderators', 'owners']
        if mat.is_allowed(interaction.user.roles, allowed_roles):           
            results = mod.remove_character(ingame_name)
            await interaction.response.send_message(results)

@client.tree.command(name="request_duel")
@app_commands.describe(character_name_a = "Kirito", character_name_b = "Asuna", type_of_duel = "half loss")
async def request_duel(interaction: discord.Interaction, character_name_a: str, character_name_b: str, type_of_duel: str):
            discord_tag = interaction.user.id
            results = com.request_duel(character_name_a, character_name_b, type_of_duel)
            await interaction.response.send_message(results)   

@client.tree.command(name="accept_or_decline_duel")
@app_commands.describe(character_name_a = "Kirito", character_name_b = "Asuna", accept_or_decline = "accept")
async def accept_or_decline_duel(interaction: discord.Interaction, character_name_a: str, character_name_b: str, accept_or_decline: str):
            discord_tag = interaction.user.id
            results = com.accept_or_decline_duel_invite(character_name_a, character_name_b, accept_or_decline)
            await interaction.response.send_message(results)   

@client.tree.command(name="add_item_to_game_mod")
@app_commands.describe(item_catagory = "medicinal", item_name = "herb", item_description = "A small plant used to cure injuries.", item_rarity = "common", dropped_by = "little nepenthes")
async def add_item_to_game_mod(interaction: discord.Interaction, item_catagory: str, item_name: str, item_description: str, item_rarity: str, dropped_by: str):
    moderator_roles = [role for role in interaction.guild.roles if role.permissions.manage_messages]
    allowed_roles = ['Executive Moderator', 'Owners']  
    if mat.is_allowed(interaction.user.roles, allowed_roles):           
        results = mod.add_item_to_server(item_catagory, item_name, item_description, item_rarity, dropped_by)
        await interaction.response.send_message(results)
    else:
        await interaction.response.send_message("You do not have the right permission to use this command.")

@client.tree.command(name="remove_item_from_game_mod")
@app_commands.describe(item_name = "herb")
async def remove_item_from_game_mod(interaction: discord.Interaction, item_name: str):
    moderator_roles = [role for role in interaction.guild.roles if role.permissions.manage_messages]
    allowed_roles = ['Executive Moderator', 'Owners']  
    if mat.is_allowed(interaction.user.roles, allowed_roles):           
        results = mod.remove_item_from_server(item_name)
        await interaction.response.send_message(results)
    else:
        await interaction.response.send_message("You do not have the right permission to use this command.")

@client.tree.command(name="add_weapon_to_game_mod")
@app_commands.describe(weapon_name = "medicinal", weapon_description = "herb", weapon_rarity = "A small plant used to cure injuries.", how_to_obtain = "common", base_power = "little nepenthes", additional_effects = "little nepenthes", crit_chance = "little nepenthes", weapon_material = "bronze", weapon_attack_type = "str", catagory = "weapon")
async def add_item_to_game_mod(interaction: discord.Interaction, weapon_name: str, weapon_description: str, weapon_rarity: str, how_to_obtain: str, base_power: str, additional_effects: str, crit_chance: str, weapon_material: str, weapon_attack_type: str, catagory: str):
    moderator_roles = [role for role in interaction.guild.roles if role.permissions.manage_messages]
    allowed_roles = ['Executive Moderator', 'Owners']  
    if mat.is_allowed(interaction.user.roles, allowed_roles):           
        results = mod.add_weapon_to_server(weapon_name, weapon_description, weapon_rarity, how_to_obtain, base_power, additional_effects, crit_chance, weapon_material, weapon_attack_type, catagory)
        await interaction.response.send_message(results)
    else:
        await interaction.response.send_message("You do not have the right permission to use this command.")

@client.tree.command(name="remove_weapon_from_game_mod")
@app_commands.describe(weapon_name = "one handed bronze sword")
async def remove_weapon_from_game_mod(interaction: discord.Interaction, weapon_name: str):
    moderator_roles = [role for role in interaction.guild.roles if role.permissions.manage_messages]
    allowed_roles = ['Executive Moderator', 'Owners']  
    if mat.is_allowed(interaction.user.roles, allowed_roles):           
        results = mod._to_server(weapon_name)
        await interaction.response.send_message(results)
    else:
        await interaction.response.send_message("You do not have the right permission to use this command.")


@client.tree.command(name="at_command", description="test")
@app_commands.describe()
async def at_command(interaction: discord.Interaction):
    moderator_roles = [role for role in interaction.guild.roles if role.permissions.manage_messages]

    moderator_mentions = ','.join([role.mention for role in moderator_roles])
    allowed_roles = ['Moderator', 'Co-Owner']
    print(moderator_mentions)
    if not mat.is_allowed(interaction.user.roles, allowed_roles):
        await interaction.response.send_message(f'Invalid roles')
    else: 
        await interaction.response.send_message(f'{moderator_mentions} Please check the character stats')
  
#Run the client.
client.run("MTAwNjM4NTMzNDEwOTYyMjMzNA.G9Ln1_.z0jCVUjrATCwirU1EszdbSqobpcudcZ1helxmY")