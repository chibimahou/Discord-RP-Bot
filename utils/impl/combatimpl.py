import discord
from discord import app_commands
from cogs.utility import (validate_alphanumeric, validate_height, validate_age, 
                     validate_date, validate_text, validate_level, get_db_connection,
                     close_db_connection)
from pymongo import MongoClient
import random
import logging

async def spawn_mob_logic(location: str, interaction: discord.Interaction):
    try:
        # Extract player's name from the interaction
        player_name = interaction.user.display_name

        # Establish database connection
        client, db = await get_db_connection()
        if db is None:
            return "Failed to connect to the database."

        # Query the database to fetch mobs based on the specified location
        mobs_available = await db["mobs"].find({"spawn_location": location}).to_list(length=None)

        if not mobs_available:
            return "No mobs available in this location."

        # Randomly select a mob from the list of available mobs
        selected_mob = random.choice(mobs_available)

        # Generate a random number of mobs to spawn (between 1 and 4)
        num_mobs_to_spawn = random.randint(selected_mob['spawn_amount']['min'], selected_mob['spawn_amount']['max'])

        # Prepare the spawn message
        spawn_message = (
            f"After walking through the {location}, a glowing red aura is seen a mere 10 feet in front of {player_name} inside nearby bushes. "
            "As the aura slowly fades away glowing red eyes can be seen from within the bushes. After hearing the sound of snarling, "
            f"{num_mobs_to_spawn} {selected_mob['name']} make(s) an appearance ready for a fight."
        )

        # Include mob stats in the spawn message
        stats = selected_mob['stats']
        spawn_message += (
            f"\n\nStats:\n"
            f"HP: {stats['hp']}\n"
            f"Dexterity: {stats['dex']}\n"
            f"Strength: {stats['str']}\n"
            f"Defense: {stats['def']}\n"
            f"Charisma: {stats['cha']}\n"
            f"Speed: {stats['spd']}\n"
            f"XP: {stats['xp']}\n"
        )

        # Include mob rewards (drops) in the spawn message
        drops = ", ".join(drop['id'] for drop in selected_mob['drops'])
        spawn_message += (
            f"\n\nRewards:\n"
            f"{drops} (Common drops with a chance for rare items)"
        )

        # Include options for the player to run or accept the battle
        spawn_message += (
            f"\n\nRun - You lose 20% of your current HP.\n"
            "Accept the battle and risk potential death.\n"
            "Fight or Flee."
        )

        return spawn_message

    except Exception as e:
        logging.error(f"An error occurred during spawn mob logic: {e}")
        return "An error occurred while spawning the mob."

def close_db_connection(connection):
    connection.close()


