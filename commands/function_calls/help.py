import discord
import sqlite3
import array
import random
import math
import function_calls.inventory as inv
import function_calls.skills as ski
import function_calls.experience as exp
import function_calls.col as col
import function_calls.stats as sta
import function_calls.calc as mat
import function_calls.trade as tra
from discord.ext import commands
from discord import app_commands
from discord.utils import get


def help_commands():
        command_list = """```
        (p) - Only person who put the command can see this message
        (m) - Only moderators can use this command.
        Command list:
        
        player commands:
        stat_screen(p) - View the players stats, inventory, skills and sword arts.
        inventory(p) - View the players inventory.
        experience(p) - View the players current experience.
        
        Modify commands:
        add_character - Allows the player to create a character.
        remove_character(m) - Remove a character from the server.
        add_inventory - Add an item to the players inventory.
        remove_inventory - Remove an item from the players inventory.
        add_experience - Add experience to the player.
        remove_experience - Remove experience from the player.
        add_col - Add col to the players inventory.
        remove_col - Remove col from the playerse inventory.
        add_skill - Add a skill to the players skill list.
        remove_skill - Remove a skill from the players skill list.
        add_proficency_skill - Add a proficiency skill to the players skill list.
        remove_proficiency_skill - Remove a proficiency skill from the players skill list.
        
        Check commands:
        check_items - Display an items or weapon information.
        check_skills - Display a skills or sword arts information
        check_character - Allows the player to view any players character sheet.
        ```"""
        return command_list

def help_damage():
        command_list = """```
        Damage is calculated using this formula:
        
        player A damage = (str attribute modifier * (weapon base power + sword skill damage) * weapon material modifier)

        Player A has a str of 50, so a 5.0 str modifier.
        Equipment: Steel one handed sword: 50 base power.

        (5.0 * 50 * 3.0) = 750 damage

        player B damage reduction = (def multiplier + (armor value * armor skill reduction) + armor material modifier)
        
        Player B has a def of 40, so a 4.0 def modifier.
        Equipment: full steel plate armor, 5 + 4 + 4 + 6 + 5 = 24 total armor value.
        since it is steel armor, the modifier is 3.0.

        (4.0 * 24 * 3.0) = 288 damage reduction

        total damage = player A damage - player B damage reduction

        So 750 - 288 = 462 total damage.

        graze damage reduction: Roll a 100 sided dice. if the role is greater than your graze success check (90 - Dexterity modifier * 5) 
        then you will take graze damage.
        
        Example: 

        dice roll = 78, player B\'s dex = 25, so your modifier is 2.5. 
        2.5* 5 = 15
        (90 - 15 = 75).
        75 < 78, as a result, you only take graze damage.
        
        so, (100 - 78) = 22\% reduced damage

        So the graze formula will be (graze_damage/100) * (total damage).

        with all the examples above we get (22/100) * (462) = 102 damage reduction. so a total of 462 - 102 = 360 damage dealt.

        Note: If skills are not being used, remove the \'sword skill damage\' and \' armor skill reduction\' from the equation.        
        Note: graze reduction maximum: slash: 25\% chance. Arts: 40\% chance.
        Note: Stat modifiers. 5-10 = 1.0, + .1 every level afterwards.
        Note: Archery: replace str attribute modifier with dex attribute modifier.
        
        For more information: visit the \'SAO: The Final Stand Combat\' doc.
        ```"""
        return command_list

def help_roleplay():
        command_list = """```
        
        ```"""
        return command_list