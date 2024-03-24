import discord
from discord import app_commands
from utils.impl.inventoryimpl import (add_logic)

class inventory(app_commands.Group):
    
    @app_commands.command()
    @app_commands.describe(item="bronze short sword", quantity="2")
    async def add(self, interaction: discord.Interaction, item: str, quantity: int):
        character_data = {
            "item": item,
            "quantity": quantity,
            "guild_id": interaction.guild.id,
            "discord_tag": interaction.user.id          
        }
        results = add_logic(interaction, character_data)
        await results
        
async def setup(bot):
    bot.tree.add_command(inventory(name="inventory", description="Handling player inventory interactions."))
