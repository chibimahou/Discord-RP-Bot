import discord
from discord import app_commands
<<<<<<< HEAD
class moderation(app_commands.Group):
    from cogs.utility import (validate_alphanumeric, validate_height, validate_age, 
                     validate_date, validate_text, validate_level, get_db_connection,
                     close_db_connection, active_character)
from utils.impl.moderationImpl import (add_item_logic, add_mob_logic, delete_mob_logic, view_mob_logic)
=======

from cogs.utility import (validate_alphanumeric, validate_height, validate_age, 
                     validate_date, validate_text, validate_level, get_db_connection,
                     close_db_connection, active_character)
from utils.impl.moderationImpl import (add_item_logic, add_mob_logic)
>>>>>>> aa06357 (add mob command)

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
<<<<<<< HEAD
    async def add_mobs(self, interaction: discord.Interaction, mob_name:str, mob_description:str, mob_type:str, floor:str, spawn_channel:str, level:str, hp:str, str:str, defense:str, spd:str, dex:str, cha:str, xp:str, spawn_message:str, ):
=======
    async def add_mobs(self, interaction: discord.Interaction, mob_name:str, mob_description:str, mob_type:str, floor:str, spawn_channel:str, level:str, hp:str, str:str, defense:str, spd:str, dex:str, cha:str ):
>>>>>>> aa06357 (add mob command)
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
<<<<<<< HEAD
            "cha": cha, 
            "xp": xp,  
            "spawn_message": spawn_message,
        }
        results = await add_mob_logic(interaction, mob_data)
        await interaction.response.send_message(results) 
<<<<<<< HEAD
=======
=======
            "cha": cha,      
        }
        results = add_mob_logic(interaction, mob_data)
        await interaction.response.send_message(results) 
>>>>>>> aa06357 (add mob command)
    
    @app_commands.command()
    async def delete_mob(self, interaction: discord.interaction, mob_name: str): 
        #Delete any mob from the database
        deletion_result = await delete_mob_logic(interaction, mob_name)
        await interaction.response.send_message(deletion_result)
        
@app_commands.command()
async def view_mobs(self, interaction: discord.Interaction, query: str):
    if query.startswith("floor:"):
        floor = query.replace("floor:", "").strip()  
        mobs_info = await view_mob_logic(interaction, floor)
    else:
        mobs_info = await search_mobs_info(interaction, query)

    if not mobs_info:
        await interaction.response.send_message("No mobs found matching the search query.")
    else:
        await interaction.response.send_message(mobs_info)


async def fetch_mobs_info_by_floor(interaction, floor):
    try:
        # Call view_mob_logic to retrieve mobs information for the specified floor
        mobs_info = await view_mob_logic(interaction, floor)

        return mobs_info

    except Exception as e:
        print(f"An error occurred: {e}")
        return "An error occurred while fetching mob information."


async def search_mobs_info(interaction, search_query):
    return await view_mob_logic(interaction, search_query)

>>>>>>> dfc00fd (.)

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
