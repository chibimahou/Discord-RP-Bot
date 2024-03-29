import discord
from discord import app_commands
from mysql.connector import Error

from cogs.utility import (validate_alphanumeric, validate_height, validate_age, 
                     validate_date, validate_text, validate_level, get_db_connection,
                     close_db_connection, active_character)
from utils.impl.moderationImpl import (add_stat_logic)

class moderation(app_commands.Group):

    # Add stats to the user
    @app_commands.command()
    async def add_stat(self, interaction: discord.Interaction, stat_name:str, stat_value: int):
        discord_tag = interaction.user.id
        guild_id = interaction.guild.id
        results = await add_stat_logic(discord_tag, guild_id, stat_name, stat_value)
        await interaction.response.send_message(results)

async def setup(bot):
    bot.tree.add_command(moderation(name="mod", description="mod commands"))
