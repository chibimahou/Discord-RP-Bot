import logging
import math
from utils.functions.database_functions import get_db_connection, close_db_connection

# Characters
#_______________________________________________________________________________________________________________________

# add character data to an object
async def comment_wrap(data):
    return f"```{data}```"