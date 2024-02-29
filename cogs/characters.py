import discord
from discord import app_commands
from datetime import datetime
import mysql.connector
from mysql.connector import Error
from utils.impl.charactersimpl import create_character_logic, delete_character_logic, active_character_logic

class characters(app_commands.Group):
    # To be implemented
    # _______________________________________________________
    # Create a character
    @app_commands.command()
    @app_commands.describe(first_name="kirigaya", last_name="kazuto", characters_name="Kirito", height="5'2\"", physique="muscular",  age="12", birthday="1/2/22", bio="A young boy who loves vrmmos.", level="1")
    async def create_character(self, interaction: discord.Interaction, first_name:str, last_name:str, characters_name:str, height:str, physique:str,  age:str, birthday:str, bio:str, level: str):          
        character_data = {
            "first_name": first_name,
            "last_name": last_name,
            "characters_name": characters_name,
            "height": height,
            "physique": physique,
            "age": age,
            "birthday": birthday,
            "bio": bio,
            "level": level,
            "discord_tag": interaction.user.id          
        }

        results = create_character_logic(character_data, interaction)
        await results

                          
    # Delete a character  
    @app_commands.command()
    async def delete_character(self, interaction: discord.Interaction, characters_name:str):
        character_data = {
            "characters_name": characters_name,
            "discord_tag": interaction.user.id          
        }
        results = delete_character_logic(character_data, interaction)
        await results
            
    
    # Select a character from multiple characters listed under a user    
    @app_commands.command()
    async def active_character(self, interaction: discord.Interaction):
        # Fetch user data from the database
        results = active_character_logic(interaction, interaction.user.id)
        await results
    
    
    #_______________________________________________________

async def setup(bot):
    bot.tree.add_command(characters(name="characters", description="Managing player profiles, stats, and inventory."))
