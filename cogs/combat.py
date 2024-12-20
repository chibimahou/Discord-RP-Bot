import discord
from discord import app_commands
from utils.impl.combatImpl import start_combat_logic, action_logic

class combat(app_commands.Group):
   
   # ______________________________________________________________________________________________________________________
   # Function: Start combat
   # ______________________________________________________________________________________________________________________
    @app_commands.command()
    async def start_combat(self, interaction: discord.Interaction, target: str):
        character_data = {
            "discord_tag": interaction.user.id,
            "guild_id": interaction.guild.id,
            "type": "character"
        }
        results = await start_combat_logic(character_data)
        await interaction.response.send_message(results)
    
    # ______________________________________________________________________________________________________________________
    # Function: Action
    # ______________________________________________________________________________________________________________________
    @app_commands.command()
    async def action(self, interaction: discord.Interaction, action:str):
        character_data = {
            "action": action.lower(),
            "discord_tag": interaction.user.id,
            "guild_id": interaction.guild.id
        }
        results = await action_logic(interaction, character_data)
        await interaction.response.send_message(results)
        
async def setup(bot):
    bot.tree.add_command(combat(name="combat", description="Managing combat interactions between players or entities."))
