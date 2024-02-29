import discord
from discord import app_commands
from datetime import datetime
import mysql.connector
from mysql.connector import Error
from utils.impl.charactersimpl import create_character_logic, delete_character_logic, active_character_logic

class characters(app_commands.Group):
    # To be implemented
    # _______________________________________________________
    # Create a character
    @app_commands.command()
    @app_commands.describe(invitee="joe")
    async def invite(self, interaction: discord.Interaction, invitee: str):          
        invite_data = {
            "invitee": invitee,
            "discord_tag": interaction.user.id          
        }

        results = create_character_logic(invite_data, interaction)
        await results
    
    #_______________________________________________________

async def setup(bot):
    bot.tree.add_command(characters(name="groups", description="Managing player parties, guild and any group related feature."))
