import discord
from discord import app_commands

class quests(app_commands.Group):
    @app_commands.command()
    async def create_character(self, interaction: discord.Interaction):
        await interaction.response.send_message("test")
        
async def setup(bot):
    bot.tree.add_command(quests(name="quests", description="Handling quests or adventures that players can embark on."))
