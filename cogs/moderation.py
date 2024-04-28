import discord
from discord import app_commands
from utils.impl.moderationImpl import (search_mob_info)
import random


from cogs.utility import (validate_alphanumeric, validate_height, validate_age, 
                     validate_date, validate_text, validate_level, get_db_connection,
                     close_db_connection, active_character)

from utils.impl.moderationImpl import (add_item_logic, add_mob_logic, view_mob_logic, remove_mob_logic) 



class moderation(app_commands.Group):
   
    @app_commands.command()    
    async def add_mobs(self, interaction: discord.Interaction, mob_name:str, mob_description:str, mob_type:str, floor:str, spawn_channel:str, level:str, hp:str, str:str, defense:str, spd:str, dex:str, cha:str, xp:str, spawn_message:str, spawn_amount:str, drops: str):
    # Fetch user data from the database
        mob_data = {
        "mob_name": mob_name,
        "mob_description": mob_description,
        "mob_type": mob_type,  
        "floor": floor,
        "spawn_channel": spawn_channel,
        "level": level,
        "hp": hp, 
        "str": str,
        "defense": defense,
        "spd": spd, 
        "dex": dex,
        "cha": cha, 
        "xp": xp,  
        "spawn_message": spawn_message,
        "guild_id": interaction.guild.id,
        "spawn_amount": {
            "min": 1,
            "max": spawn_amount,
            
        },
        "drops": []
        
        }
        
        for drop in drops.split(','):
            drop_info = drop.split(',')
            if len(drop_info) == 3:
                name, id, chance = drop_info
                mob_data["drops"].append({ 
                    "name": name,
                    "id": id,
                    "drop_chance": int(chance)
                    
                })
                
        results = await add_mob_logic(mob_data)
        await interaction.response.send_message(results)
        
    @app_commands.command()    
    async def remove_mob(self, mob_name: str):
        result = await remove_mob_logic(mob_name)
        await self.send_message(result)
        
    @app_commands.command()
    async def view_mob(self, interaction: discord.Interaction, search_query: str):
        result = await view_mob_logic(interaction, search_query)
        await interaction.response.send_message(result)

        
        
async def setup(bot):
    bot.tree.add_command(moderation(name="mod", description="mod commands"))