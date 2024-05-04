import discord
import logging
from discord import app_commands
from utils.functions.moderation_functions import toggle_functions

def toggle_parties_logic(guild_id):
    message = toggle_functions("parties", guild_id)
    return message