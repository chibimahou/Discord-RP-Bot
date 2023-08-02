import discord
import sqlite3
import os
import re
import random
import math as mat
import function_calls.calc as calc
import function_calls.query.query as que
import function_calls.validate as val
import function_calls.inventory as inv
from discord.ext import commands
from discord import app_commands
from discord.utils import get

def start_blacksmithing(character_name, item, process, discord_tag):
        if(calc.verify_account(character_name, discord_tag)):
            if(val.item_exists(item)):
                character_name_lower = character_name.lower()
                item_lower = item.lower()
                process_lower = process.lower()
                skill = val.get_players_skills("blacksmithing", character_name_lower, discord_tag)
                material = val.get_blacksmithing_material(item_lower)
                if(process_lower != material[6]):
                     inv.remove_inventory(character_name_lower, material[0], discord_tag)
                     return("``` Failure: You have used the wrong processing type for this material. ```")
                else:
                     success_rate = ((int(skill[1]) - int(material[5])) * 10) + 50
                     if(success_rate >= 100):
                          inv.remove_inventory(character_name_lower, material[0], discord_tag)
                          inv.add_inventory(character_name_lower, material[7], discord_tag)
                          return("""```Success! you have forged a """ + material[7] + """```""")
                     else:
                          failure_rate = random.randint(0, 100)
                          if(success_rate >= failure_rate):
                               inv.remove_inventory(character_name_lower, material[0], discord_tag)
                               inv.add_inventory(character_name_lower, material[7], discord_tag)
                               return ("""```Success! you have forged a """ + material[7] + """```""")
                          else:
                               inv.remove_inventory(character_name_lower, material[0], discord_tag)
                               return ("""```Failure! You have failed to process the """ + item_lower + """.```""")
        else:
            return('``` This account is not linked to this discord account. Please log into the proper account, or reach out to a moderator to switch accounts if you do not have access to that account. ```')