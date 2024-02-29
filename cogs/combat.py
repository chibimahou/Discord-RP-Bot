import discord
from discord import app_commands

class combat(app_commands.Group):
    @app_commands.command()
    async def create_character(self, interaction: discord.Interaction):
        await interaction.response.send_message("test")
        
async def setup(bot):
    bot.tree.add_command(combat(name="combat", description="Managing combat interactions between players or entities."))
