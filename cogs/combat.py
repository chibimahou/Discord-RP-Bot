import discord
from discord import app_commands
from utils.impl.combatimpl import (attack_logic, begin_combat_logic)

class combat(app_commands.Group):
    
    @app_commands.command()
    @app_commands.describe()
    async def begin_combat(self, interaction: discord.Interaction):
        combat_data = {
            "channel": interaction.channel.name,
            "discord_tag": interaction.user.id,
            "guild_id": interaction.guild.id    
        }
        result = await begin_combat_logic(combat_data)
        await interaction.response.send_message(result)
        
    @app_commands.command()
    @app_commands.describe(skill="Vorpal Strike", target="1, 2")
    async def Attack(self, interaction: discord.Interaction, skill: str, targets: int):
        target_list = [int(target.strip()) for target in targets.split(',')]
        player_character_data = {
            "skill": skill.lower(),
            "target": target_list,
            "discord_tag": interaction.user.id,
            "guild_id": interaction.guild.id    
        }
        result = await attack_logic(player_character_data)
        await interaction.response.send_message(result)
        
        
        
async def setup(bot):
    bot.tree.add_command(combat(name="combat", description="Managing combat interactions between players or entities."))
