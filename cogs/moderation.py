import discord
from discord import app_commands
from mysql.connector import Error


class moderation(app_commands.Group):

    # Level up the user
    @app_commands.command()
    async def create_item(self, interaction: discord.Interaction, item_name:str, item_quality: str, 
                          item_description: str, effect_type: str, effect_ammount: str,
                          material_to_craft_1: str, quantity_1: int, material_to_craft_2: str, 
                          quantity_2: int, material_to_craft_3: str, quantity_3: int, 
                          material_to_craft_4: str, quantity_4: int, 
                          material_to_craft_5: str, quantity_5: int):
        # Example role names or IDs you're looking for
        allowed_role_names = ['Moderator', 'Admin']

        # Check if the user has any of the allowed roles by name or ID
        user_roles = interaction.user.roles  # This is a list of roles the user has
        if any(role.name in allowed_role_names for role in user_roles):
            # User has an allowed role
            # results = await create_item_logic(interaction.user.id, interaction.guild.id)
           # await interaction.response.send_message(results)
       # else:
            # User does not have the required role
            await interaction.response.send_message("You do not have permission to use this command.", ephemeral=True)

        
async def setup(bot):
    bot.tree.add_command(moderation(name="mod", description="mod commands"))
