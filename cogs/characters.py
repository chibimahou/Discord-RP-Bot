import discord
from discord import app_commands
from datetime import datetime
from utils.impl.charactersimpl import (create_logic, delete_logic, active_logic, 
                                       switch_active_logic, all_available_logic,
                                        add_stat_logic, level_up_logic)

class characters(app_commands.Group):
    # To be implemented
    # _______________________________________________________
    # Create a character
    @app_commands.command()
    @app_commands.describe(first_name="kirigaya", last_name="kazuto", characters_name="Kirito", height="5'2\"", physique="muscular",  age="12", birthday="1/2/22", bio="A young boy who loves vrmmos.", level="1")
    async def create(self, interaction: discord.Interaction, first_name:str, last_name:str, characters_name:str, height:str, physique:str,  age:str, birthday:str, bio:str, level: str):          
        character_data = {
            "first_name": first_name.lower(),
            "last_name": last_name.lower(),
            "characters_name": characters_name.lower(),
            "height": height,
            "physique": physique.lower(),
            "age": age,
            "birthday": birthday,
            "bio": bio.lower(),
            "level": level,
            "discord_tag": interaction.user.id,
            "guild_id": interaction.guild.id    
        }

        results = await create_logic(character_data, interaction)
        await interaction.response.send_message(results)

                          
    # Delete a character  
    @app_commands.command()
    async def delete_character(self, interaction: discord.Interaction, characters_name:str):
        character_data = {
            "characters_name": characters_name,
            "discord_tag": interaction.user.id,
            "guild_id": interaction.guild.id       
        }
        results = await delete_logic(character_data, interaction)
        await interaction.response.send_message(results)
            
    # Change active character  
    @app_commands.command()
    async def switch_active(self, interaction: discord.Interaction, characters_name:str):
        character_data = {
            "characters_name": characters_name,
            "discord_tag": interaction.user.id,
            "guild_id": interaction.guild.id       
        }
        results =await switch_active_logic(character_data, interaction)
        await interaction.response.send_message(results)

    # View all characters a player currently has available  
    @app_commands.command()
    async def all_available(self, interaction: discord.Interaction):
        character_data = {
            "discord_tag": interaction.user.id,
            "guild_id": interaction.guild.id       
        }
        results = await all_available_logic(character_data)
        await interaction.response.send_message(results)
        
    # Select a character from multiple characters listed under a user    
    @app_commands.command()
    async def active(self, interaction: discord.Interaction):
        character_data = {
            "discord_tag": interaction.user.id,
            "guild_id": interaction.guild.id       
        }
        # Fetch user data from the database
        discord_tag = interaction.user.id          
        results = await active_logic(character_data)
        await interaction.response.send_message(results)

    # Add stats to the user
    @app_commands.command()
    async def add_stat(self, interaction: discord.Interaction, stat_name:str, stat_value: int):
        character_data = {
            "discord_tag": interaction.user.id,
            "guild_id": interaction.guild.id,
            "stat_name": stat_name,
            "stat_value": stat_value
        }
        results = await add_stat_logic(character_data)
        await interaction.response.send_message(results)

    # Level up the user
    @app_commands.command()
    async def level_up(self, interaction: discord.Interaction):
        character_data = {
            "discord_tag": interaction.user.id,
            "guild_id": interaction.guild.id
        }
        results = await level_up_logic(character_data)
        await interaction.response.send_message(results)
        
    
    #_______________________________________________________

async def setup(bot):
    bot.tree.add_command(characters(name="characters", description="Managing player profiles, stats, and inventory."))
