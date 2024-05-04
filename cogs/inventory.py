import discord
from discord import app_commands
from utils.impl.inventoryimpl import (add_logic, remove_logic, check_logic, equip_logic)

class inventory(app_commands.Group):
    @app_commands.command()
    async def add(self, interaction: discord.Interaction, item_name:str):
        item_data = {
            "name": item_name.lower(),
            "guild_id": interaction.guild.id

        }
        character_data = {
            "discord_tag": interaction.user.id,
            "guild_id": interaction.guild.id
            }
        results = await add_logic(interaction, character_data, item_data)
        await interaction.response.send_message(results)
        
    @app_commands.command()
    async def remove(self, interaction: discord.Interaction, item_name:str, item_quantity: int):
        item_data = {
            "name": item_name.lower(),
            "quantity": item_quantity,
            "guild_id": interaction.guild.id

        }
        character_data = {
            "discord_tag": interaction.user.id,
            "guild_id": interaction.guild.id
            }
        results = await remove_logic(interaction, character_data, item_data)
        await interaction.response.send_message(results)
        
    @app_commands.command()
    async def check(self, interaction: discord.Interaction):
        character_data = {
            "discord_tag": interaction.user.id,
            "guild_id": interaction.guild.id
            }
        results = await check_logic(interaction, character_data)
        await interaction.response.send_message(results)
            
    @app_commands.command()
    async def equip(self, interaction: discord.Interaction, equipment: str):
        character_data = {
            "discord_tag": interaction.user.id,
            "guild_id": interaction.guild.id
            
            }
        results = await equip_logic(interaction, character_data)
        await interaction.response.send_message(results)
        
async def setup(bot):
    bot.tree.add_command(inventory(name="inventory", description="Handling player inventory interactions."))
