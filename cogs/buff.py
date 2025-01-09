import discord
from discord import app_commands
from datetime import datetime
from utils.impl.buffimpl import (create_logic, delete_logic, active_logic, 
                                       switch_active_logic, all_available_logic,
                                        add_stat_logic, level_up_logic)

class buff(app_commands.Group):
    # ______________________________________________________________________________________________________________________
    # Create a character
    # ______________________________________________________________________________________________________________________
    @app_commands.command()
    @app_commands.describe(item_identifier="1", buff_name="strength boost")
    async def apply_buff(self, interaction: discord.Interaction, item_identifier: int, buff_name: str):          
        item_data = {
            "identifier": item_identifier,
            "buff_name": buff_name,
            "discord_tag": interaction.user.id,
            "guild_id": interaction.guild.id    
        }

        results = await create_logic(item_data)
        await interaction.response.send_message(results)

async def setup(bot):
    bot.tree.add_command(buff(name="buff", description="manage buffs."))
