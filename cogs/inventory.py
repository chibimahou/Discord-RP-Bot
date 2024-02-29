import discord
from discord import app_commands
from utils.impl.inventoryimpl import (add_inventory_logic)

class inventory(app_commands.Group):
    @app_commands.command()
    async def add_inventory(self, interaction: discord.Interaction):
        results = add_inventory_logic(interaction, interaction.user.id)
        await results
        
async def setup(bot):
    bot.tree.add_command(inventory(name="inventory", description="Handling player inventory interactions."))
