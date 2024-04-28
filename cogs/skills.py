import discord
from discord import app_commands

class skills(app_commands.Group):
    @app_commands.command()
    async def create_character(self, interaction: discord.Interaction):
        await interaction.response.send_message("test")

async def setup(bot):
    bot.tree.add_command(skills(name="skills", description="Handling player skills and abilities."))
