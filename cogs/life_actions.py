import discord
from discord import app_commands

class life_actions(app_commands.Group):
    @app_commands.command()
    async def create_character(self, interaction: discord.Interaction):
        await interaction.response.send_message("test")
        
async def setup(bot):
    bot.tree.add_command(life_actions(name="life_actions", description="Managing non-combat actions like cooking, fishing, etc."))
