import discord
from discord import app_commands
from mysql.connector import Error

from cogs.utility import (validate_alphanumeric, validate_height, validate_age, 
                     validate_date, validate_text, validate_level, get_db_connection,
                     close_db_connection, active_character)
from utils.impl.moderationImpl import (add_item_logic)

class moderation(app_commands.Group):
    # Select a character from multiple characters listed under a user    
    @app_commands.command()
    async def add_item(self, interaction: discord.Interaction, item_name:str, item_description:str, rarity:str, how_to_obtain:str, catagory:str, method_to_obtain:str):
        # Fetch user data from the database
        item_data = {
            "item_name": item_name,
            "item_description": item_description,
            "rarity": rarity,  
            "how_to_obtain": how_to_obtain,
            "catagory": catagory,
            "method_to_obtain": method_to_obtain      
        }
        results = add_item_logic(interaction, item_data)
        await results
    
    # Add stats to the user
    @app_commands.command()
    async def add_stat(self, interaction: discord.Interaction, item_name:str, item_description:str, rarity:str, how_to_obtain:str, catagory:str, method_to_obtain:str):
        # Fetch user data from the database
        item_data = {
            "item_name": item_name,
            "item_description": item_description,
            "rarity": rarity,  
            "how_to_obtain": how_to_obtain,
            "catagory": catagory,
            "method_to_obtain": method_to_obtain      
        }
        results = add_item_logic(interaction, item_data)
        await results

async def setup(bot):
    bot.tree.add_command(moderation(name="mod", description="mod commands"))
