import discord
from discord import app_commands
class moderation(app_commands.Group):
    from cogs.utility import (validate_alphanumeric, validate_height, validate_age, 
                     validate_date, validate_text, validate_level, get_db_connection,
                     close_db_connection, active_character)
from utils.impl.moderationImpl import (add_item_logic, add_mob_logic)

class moderation(app_commands.Group):
    # Select a character from multiple characters listed under a user    
    @app_commands.command()
    async def add_item(self, interaction: discord.Interaction, item_name:str, item_description:str, rarity:str, how_to_obtain:str, catagory:str, method_to_obtain:str):
        # Fetch user data from the database
        item_data = {
            "item_name": item_name,
            "item_description": item_description,
            "rarity": rarity,  
            "how_to_obtain": how_to_obtain,
            "catagory": catagory,
            "method_to_obtain": method_to_obtain      
        }
        results = add_item_logic(interaction, item_data)
        await interaction.response.send_message(results)
        
    @app_commands.command()    
    async def add_mobs(self, interaction: discord.Interaction, mob_name:str, mob_description:str, mob_type:str, floor:str, spawn_channel:str, level:str, hp:str, str:str, defense:str, spd:str, dex:str, cha:str ):
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
        }
        results = add_mob_logic(interaction, mob_data)
        await interaction.response.send_message(results) 

    # Add stats to the user
    @app_commands.command()
    async def add_stat(self, interaction: discord.Interaction, stat_name:str, stat_value: int):
        discord_tag = interaction.user.id
        guild_id = interaction.guild.id
       # results = await add_stat_logic(discord_tag, guild_id, stat_name, stat_value)
       # await interaction.response.send_message(results)

    # Level up the user
    @app_commands.command()
    async def level_up(self, interaction: discord.Interaction):
        discord_tag = interaction.user.id
        guild_id = interaction.guild.id
       # results = await level_up_logic(discord_tag, guild_id)
        #await interaction.response.send_message(results)
        
async def setup(bot):
    bot.tree.add_command(moderation(name="mod", description="mod commands"))
