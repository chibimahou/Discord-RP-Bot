import discord
import logging
from discord import app_commands
from mysql.connector import Error

from utils.functions.moderation_functions import (
                    add_points_to_stat)
from utils.functions.database_functions import (
                    get_db_connection)
from utils.functions.validation_functions import (validate_alphanumeric, validate_height, validate_age, 
                    validate_text, validate_level)

# Function to add stat points to a character
async def add_stat_logic(discord_tag, guild_id, stat_name, stat_value):
    logging.info(f"Adding {stat_value} points to {stat_name} for {discord_tag} in guild {guild_id}")
    await add_points_to_stat(discord_tag, guild_id, stat_name, stat_value)

    return "Stat points added successfully!"