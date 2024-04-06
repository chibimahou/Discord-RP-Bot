import discord
from discord import app_commands
from mysql.connector import Error

from utils.functions.inventory_functions import (
                    add_item_to_inventory, remove_item_from_inventory, check_inventory)
from utils.functions.database_functions import (
                    get_db_connection)
from utils.functions.validation_functions import (validate_alphanumeric, validate_height, validate_age, 
                    validate_text, validate_level)

from pymongo import MongoClient

def add_logic(interaction, characters_data, item_data):
    message = add_item_to_inventory(characters_data, item_data)
    return message

def remove_logic(interaction, characters_data, item_data):
    message = remove_item_from_inventory(characters_data, item_data)
    return message

def check_logic(interaction, characters_data):
    message = check_inventory(characters_data)
    return message