import discord
from discord import app_commands
from datetime import datetime
import mysql.connector
from mysql.connector import Error
from utils.impl.groupsImpl import (create_party_logic, party_invite_logic, 
                                   accept_party_invite_logic, decline_party_invite_logic,
                                   leave_party_logic)
from utils.impl.charactersimpl import create_character_logic, delete_character_logic, active_character_logic

class characters(app_commands.Group):
    # ______________________________________________________________________________________________________________________
    # send party invite
    # ______________________________________________________________________________________________________________________
    @app_commands.command()
    @app_commands.describe(invitee="joe")
    async def party_invite(self, interaction: discord.Interaction, invitee: str):          
        character_data = {
            "characters_name": invitee.lower(),
            "discord_tag": interaction.user.id,
            "guild_id": interaction.guild.id         
        }
        results = await party_invite_logic(character_data, interaction)
        await interaction.followup.send(results, ephemeral=True)

    # ______________________________________________________________________________________________________________________    
    # Create a party
    # ______________________________________________________________________________________________________________________
    @app_commands.command()
    @app_commands.describe(party_name = "The Avengers")
    async def create_party(self, interaction: discord.Interaction, party_name: str):          
        party_data = {
            "party_name": party_name.lower(),
            "discord_tag": interaction.user.id,
            "guild_id": interaction.guild.id         
        }
        results = await create_party_logic(party_data)
        await interaction.response.send_message(results)

    # ______________________________________________________________________________________________________________________
    # Accept a party invite
    # ______________________________________________________________________________________________________________________
    @app_commands.command()
    @app_commands.describe(inviter="joe")
    async def accept_party_invite(self, interaction: discord.Interaction, inviter: str):
        character_data = {
            "characters_name": inviter.lower(),
            "response" : "accept",
            "discord_tag": interaction.user.id,
            "guild_id": interaction.guild.id         
        }
        user_id = await interaction.guild.fetch_member(character_data['discord_tag'])
        print(f"test {user_id}")

        results = await accept_party_invite_logic(character_data, interaction, user_id)
        await interaction.followup.send(results, ephemeral=True)
    

    # ______________________________________________________________________________________________________________________
    # Decline a party invite
    # ______________________________________________________________________________________________________________________
    @app_commands.command()
    @app_commands.describe(inviter="joe")
    async def decline_party_invite(self, interaction: discord.Interaction, inviter: str):
        character_data = {
            "characters_name": inviter.lower(),
            "response" : "accept",
            "discord_tag": interaction.user.id,
            "guild_id": interaction.guild.id         
        }
        user_id = await interaction.guild.fetch_member(character_data['discord_tag'])
        print(f"test {user_id}")

        results = await accept_party_invite_logic(character_data, interaction, user_id)
        await interaction.followup.send(results, ephemeral=True)
    
    # ______________________________________________________________________________________________________________________
    # Leave a party
    # ______________________________________________________________________________________________________________________
    @app_commands.command()
    async def leave_party(self, interaction: discord.Interaction):          
        party_data = {
            "discord_tag": interaction.user.id,
            "guild_id": interaction.guild.id         
        }
        results = await leave_party_logic(party_data, interaction)
        await interaction.followup.send(results, ephemeral=True)
        
async def setup(bot):
    bot.tree.add_command(characters(name="groups", description="Managing player parties, guild and any group related feature."))
