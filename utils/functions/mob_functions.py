import logging
import math
import random
from utils.functions.database_functions import get_db_connection, close_db_connection
from utils.functions.character_functions import active_character

# mobs
#_______________________________________________________________________________________________________________________
async def generate_mobs(db, mob_data):
    # 
    
async def get_mobs_from_channel(db, mob_data):
    # Get all mobs that match the channel name
    mob = await db['mobs'].find({
        "misc.channel": mob_data["channel"],
        "misc.guild_id": mob_data["guild_id"]})
    if mob is None:
        return None
    else:
        return mob
    
async def generate_random_number_of_enemies(db, mob_document):
    # Get a random number between 1 and 5
    num_enemies = random.randint(1, mob_document['spawn']['max'])
    # Get a random mob from the list of mobs
    mob = await get_random_mob(db, mob_document)
    # Create a list of mobs
    mob_list = []
    for i in range(num_enemies):
        mob_list.append(mob)
    return mob_list
    
async def get_random_mob(db, mob_data):
    mob_list = await get_mobs_from_channel(db, mob_data)
    mob = random.choice(mob_list)
    