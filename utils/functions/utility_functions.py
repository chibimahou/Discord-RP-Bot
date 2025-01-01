import discord
import logging
import math
from utils.functions.database_functions import get_db_connection, close_db_connection

# Characters
#_______________________________________________________________________________________________________________________

# add character data to an object
async def comment_wrap(data):
    return f"```{data}```"

async def get_user_roles(user: discord.Member):
    roles = [role.name for role in user.roles if role.name != "@everyone"]
    return ", ".join(roles) if roles else "No roles"

async def has_required_role(user: discord.Member):
    roles = await get_user_roles(user)
    return "Moderator" in roles or "Admin" in roles

