import discord
from discord import app_commands
from datetime import datetime
import mysql.connector
from mysql.connector import Error
from utils.impl.groupsImpl import create_party_logic, party_invite_logic

class characters(app_commands.Group):

    # send party invite
    @app_commands.command()
    @app_commands.describe(invitee="joe")
    async def party_invite(self, interaction: discord.Interaction, invitee: str):          
        invite_data = {
            "invitee": invitee,
            "discord_tag": interaction.user.id,
            "guild_id": interaction.guild.id         
        }

        results = party_invite_logic(invite_data)
        await interaction.response.send_message(results)
    
    # Create a party
    @app_commands.command()
    @app_commands.describe(party_name = "The Avengers")
    async def create_party(self, interaction: discord.Interaction, party_name: str):          
        party_data = {
            "party_name": party_name,
            "discord_tag": interaction.user.id,
            "guild_id": interaction.guild.id         
        }
        results = await create_party_logic(party_data)
        await interaction.response.send_message(results)
        #_______________________________________________________

async def setup(bot):
    bot.tree.add_command(characters(name="groups", description="Managing player parties, guild and any group related feature."))
