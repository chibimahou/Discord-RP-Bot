import discord
from discord import app_commands
from datetime import datetime
from utils.impl.charactersimpl import (create_logic, delete_logic, active_logic, 
                                       switch_active_logic, all_available_logic,
                                        add_stat_logic, level_up_logic)

class mobs(app_commands.Group):
    # ______________________________________________________________________________________________________________________
    # Create a character
    # ______________________________________________________________________________________________________________________
    @app_commands.command()
    @app_commands.describe(name="goblin")
    async def create(self, interaction: discord.Interaction, name:str):          
        mob_data = {
            "name": name.lower(),
        }

        results = await create_logic(mob_data)
        await interaction.response.send_message(results)


    #_______________________________________________________

async def setup(bot):
    bot.tree.add_command(mobs(name="mobs", description="Manages spawning, creating, and deleting mobs."))
