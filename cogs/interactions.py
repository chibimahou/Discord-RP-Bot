import discord
from discord import app_commands

class interactions(app_commands.Group):
    @app_commands.command()
    async def create_character(self, interaction: discord.Interaction):
        await interaction.response.send_message("test")
        
async def setup(bot):
    bot.tree.add_command(interactions(name="interactions", description="Manage player interactions or social aspects."))
