import discord
from discord import app_commands
from datetime import datetime
from utils.impl.modImpl import (create_mob_logic)
from utils.functions.utility_functions import has_required_role

class mod(app_commands.Group):
    
    def __init__(self):
        super().__init__(name="mod", description="Moderator functions.")

    # ______________________________________________________________________________________________________________________
    # Create a character
    # ______________________________________________________________________________________________________________________
    @app_commands.command()
    @app_commands.describe(name="goblin", average_level = 1, exp_reward = 50, equipment_head = "bronze helmet", equipment_body = "bronze chestplate", 
                           equipment_legs = "bronze leggings", equipment_feet = "bronze boots", equipment_hands = "bronze gauntlets", equipment_main_hand = "bronze sword",
                           equipment_off_hand = "bronze shield", equipment_accessory_1 = "bronze ring", equipment_accessory_2 = "cloak", hp = 5, strength = 5, dexterity = 5, 
                           defense = 5, speed = 5, charisma = 5)
    async def create_mobs(self, interaction: discord.Interaction,  user: discord.Member, name:str, average_level:int, exp_reward:int, equipment_head:str, equipment_body:str,
                          equipment_legs:str, equipment_feet:str, equipment_hands:str, equipment_main_hand:str, equipment_off_hand:str, equipment_accessory_1:str, 
                          equipment_accessory_2:str, hp:int, strength:int, dexterity:int, defense:int, speed:int, charisma:int):          
        # Check if the user is authorized to perform this action
        authorized = await has_required_role(user)
        if(authorized):
            mob_data = {
                "name": name.lower(),
                "average_level": average_level,
                "exp_reward": exp_reward,
                "equipment_head": equipment_head,
                "equipment_body": equipment_body,
                "equipment_legs": equipment_legs,
                "equipment_feet": equipment_feet,
                "equipment_hands": equipment_hands,
                "equipment_main_hand": equipment_main_hand,
                "equipment_off_hand": equipment_off_hand,
                "equipment_accessory_1": equipment_accessory_1,
                "equipment_accessory_2": equipment_accessory_2,
                "hp": hp,
                "strength": strength,
                "dexterity": dexterity,
                "defense": defense,
                "speed": speed,
                "charisma": charisma,            
                "guild_id": interaction.guild_id,
                "inserted_by": interaction.user.id,
                "insertion_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"), 
            }
            results = await create_mob_logic(mob_data)
        else:
            results = "You are not authorized to perform this action."
        await interaction.response.send_message(results)


    #_______________________________________________________

async def setup(bot):
    bot.tree.add_command(mod(name="mod", description="Moderator functions."))
