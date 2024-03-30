import discord
from discord import app_commands
from mysql.connector import Error


from utils.impl.moderationImpl import (add_stat_logic, level_up_logic)

class moderation(app_commands.Group):

    # Add stats to the user
    @app_commands.command()
    async def add_stat(self, interaction: discord.Interaction, stat_name:str, stat_value: int):
        discord_tag = interaction.user.id
        guild_id = interaction.guild.id
        results = await add_stat_logic(discord_tag, guild_id, stat_name, stat_value)
        await interaction.response.send_message(results)

    # Level up the user
    @app_commands.command()
    async def level_up(self, interaction: discord.Interaction):
        discord_tag = interaction.user.id
        guild_id = interaction.guild.id
        results = await level_up_logic(discord_tag, guild_id)
        await interaction.response.send_message(results)
        
async def setup(bot):
    bot.tree.add_command(moderation(name="mod", description="mod commands"))
