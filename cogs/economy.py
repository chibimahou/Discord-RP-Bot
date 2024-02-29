import discord
from discord import app_commands

class economy(app_commands.Group):
    @app_commands.command()
    async def create_character(self, interaction: discord.Interaction):
        await interaction.response.send_message("test")
        
async def setup(bot):
    bot.tree.add_command(economy(name="economy", description="Manage the in-game economy, currency, trading, or shops."))