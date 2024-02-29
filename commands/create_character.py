import discord
from discord.ext import commands

class create_character(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # A simple command inside the cog
    @commands.tree.command(name="test", description="Hello!")
    async def test(interaction: discord.Interaction):
        await interaction.response.send_message("test")

    # If you're using slash commands, the structure would be a bit different
    # For the sake of simplicity, I'm demonstrating with a regular command

def setup(bot):
    bot.add_cog(create_character(bot))
