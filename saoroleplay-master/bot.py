import discord
import sqlite3
import os
from discord.ext import commands
from discord import app_commands
from discord.utils import get

print("Hello")
client = commands.Bot(command_prefix="!", intents = discord.Intents.all())

@client.event
async def on_ready():
    await client.tree.sync()
    print('We have logged in as {0.user}'.format(client))

@client.tree.command(name="hello", description="Hello!")
async def hello(interaction: discord.Interaction):
        await client.tree.sync()
        print('Command tree synced.')

@client.tree.command(name="spawn", description="Spawns a mob!")
@app_commands.describe(floor = '1', area = 'something')
async def spawn(interaction: discord.Interaction, floor: str, area: str):
        sqliteConnection = sqlite3.connect('mobspawn.db')
        cursor = sqliteConnection.cursor()
        monster_spawns = cursor.execute("SELECT * from Location  ").fetchall()
        spawns= str(monster_spawns[0][0])
        monster_information = cursor.execute("SELECT mobs.name, stats.hp, stats.str, stats.agi, stats.spe FROM mobs INNER JOIN stats on mobs.ID = stats.ID WHERE mobs.ID = 1 ").fetchall()
        name = str(monster_information[0][0])
        HealthPoints = str(monster_information[0][1])
        strength  = str(monster_information[0][2])
        Agility = str(monster_information[0][3])
        Speed = str(monster_information[0][4])
        cursor.close()
        await interaction.response.send_message(f'``` Off In the distance {interaction.user.nick} hears a sound cue as a medium sized ' + spawns + ' with blue fur, glowing red eyes, a flat snout and sharp tusks protruding from both sides of its mouth appears at your forefront. \n \n Stats:  HP - ' + HealthPoints + '   STR - ' + strength +'   AGI - ' + Agility +'  SPE - ' + Speed +' \n \n Rewards: 40  Col, 15 XP, Raw Boar Pork, \n \n Run - user loses 15% HP \n \n Accept the battle and risk potiential death. \n \n Fight or Flee ```')

#Run the client.
client.run("MTAwNjAxODA5NjEwMTg2MzQ5NQ.GbpWtB.V57ceowv1c4RAa93-S31uWz_HeSsixmA0NPB24")
