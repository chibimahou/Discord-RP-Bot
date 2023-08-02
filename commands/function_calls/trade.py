import discord
import sqlite3
import os
import re
import function_calls.calc as calc
import function_calls.inventory as inventory
import function_calls.col as col
from discord.ext import commands
from discord import app_commands
from discord.utils import get

def trade(character_name_a, item_to_trade_a, character_name_b, item_to_trade_b, col_ammount, discord_tag):
    if(calc.verify_account(character_name_a, discord_tag) or calc.verify_account(character_name_b, discord_tag)):     
        if(calc.validate_fields(character_name_a) == True and calc.validate_fields(character_name_b) == True and calc.validate_fields(item_to_trade_a) == True and calc.validate_fields(item_to_trade_b) == True):
                item_to_trade_a_lower = item_to_trade_a.lower()
                item_to_trade_b_lower = item_to_trade_b.lower()
                sqliteConnection = sqlite3.connect('characterSheet.db')
                cursor = sqliteConnection.cursor()
                if(item_to_trade_a_lower == 'col'):
                        print("1")
                        character_a_inventory = col.check_col(character_name_a, col_ammount)
                        if(character_a_inventory != True):
                                print("2")
                                return "Failed to complete trade: " + character_name_a.lower() + " does not have enough col." 
                else:       
                        print("3")        
                        character_a_inventory = inventory.check_inventory_for_item(character_name_a, item_to_trade_a_lower)
                if(item_to_trade_b_lower == 'col'):
                        print("4")
                        character_b_inventory = col.check_col(character_name_b, col_ammount)
                        if(character_b_inventory != True):
                                print("5")                               
                                return "Failed to complete trade: " + character_name_b.lower() + " does not have enough col." 
                else:
                        print("6")
                        character_b_inventory = inventory.check_inventory_for_item(character_name_b, item_to_trade_b_lower)
                if(character_a_inventory == True and character_b_inventory == True):
                        if(item_to_trade_a_lower == 'col'):
                                return  f"```{character_name_a} would like to trade: \n\n{col_ammount} col \n\n{character_name_b} would like to trade: \n\n{item_to_trade_b}. \n\nIf both players respond to this with an emote, that will confirm the trade. \n\nModerators have been alerted to initiate the trade.```"                               
                        elif(item_to_trade_b_lower == 'col'):
                                return  f"```{character_name_a} would like to trade: \n\n{item_to_trade_a} \n\n{character_name_b} would like to trade: \n\n{col_ammount} col. \n\nIf both players respond to this with an emote, that will confirm the trade. \n\nModerators have been alerted to initiate the trade.```"
                        else:       
                                return  f"```{character_name_a} would like to trade: \n\n{item_to_trade_a} \n\n{character_name_b} would like to trade: \n\n{item_to_trade_b}. \n\nIf both players respond to this with an emote, that will confirm the trade. \n\nModerators have been alerted to initiate the trade.```"
                else:
                        return "Failed to request trade. Please verify items in both players inventories and try again.."
    else:
           return "Failure. Please only request trades involving your character."
def accept_trade(character_name_a, item_to_trade_a, character_name_b, item_to_trade_b, col_ammount):
    if(calc.validate_fields(character_name_a) == True and calc.validate_fields(character_name_b) == True and calc.validate_fields(item_to_trade_a) == True and calc.validate_fields(item_to_trade_b) == True):
        success_or_failure = False
        check_item_exist_a = inventory.check_inventory_for_item(character_name_a, item_to_trade_a.lower())
        check_item_exist_b = inventory.check_inventory_for_item(character_name_b, item_to_trade_b.lower())
        if((check_item_exist_a == True or item_to_trade_a.lower() == "col") and (check_item_exist_b == True or item_to_trade_b.lower() == "col")):
                if(item_to_trade_a.lower() == "col"):
                        remove_a = col.remove_col_trade(character_name_a, col_ammount)
                        print("Remove: " + item_to_trade_a + " ammount: " + col_ammount)
                else:
                        remove_a = inventory.remove_inventory_trade(character_name_a, item_to_trade_a)
                        print("Remove: " + item_to_trade_a)
                if(remove_a == True):
                        if(item_to_trade_b.lower() == "col"):
                                add_a = col.add_col_trade(character_name_a, col_ammount)
                                print("add: " + item_to_trade_b + " ammount: " + col_ammount)
                        else:
                                add_a = inventory.add_inventory_trade(character_name_a, item_to_trade_b)
                                print("add: " + item_to_trade_b)
                        
                        if(add_a == True):
                                if(item_to_trade_b.lower() == "col"):
                                        remove_b = col.remove_col_trade(character_name_a, col_ammount)
                                        print("Remove: " + item_to_trade_b + " ammount: " + col_ammount)
                                else:
                                        print("Remove: " + item_to_trade_b)
                                        remove_b = inventory.remove_inventory_trade(character_name_b, item_to_trade_b)                                                  
                                if(remove_b == True):
                                        if(item_to_trade_a.lower() == "col"):
                                                add_b = col.add_col_trade(character_name_b, col_ammount)
                                                print("add: " + item_to_trade_a + " ammount: " + col_ammount)
                                        else:
                                                print("add: " + item_to_trade_a)
                                                add_b = inventory.add_inventory_trade(character_name_b, item_to_trade_a)                             
                                        if(add_b == True):
                                                return True
                                        else:
                                                add_b = inventory.remove_inventory_trade(character_name_b, item_to_trade_b)
                                                remove_a = inventory.add_inventory_trade(character_name_a, item_to_trade_b)
                                                add_a = inventory.remove_inventory_trade(character_name_a, item_to_trade_a)
                                                return False          

                                else:
                                        add_b = inventory.remove_inventory_trade(character_name_b, item_to_trade_b)
                                        remove_a = inventory.add_inventory_trade(character_name_a, item_to_trade_b)  
                                        return False          
                        
                        else:
                                remove_a = inventory.add_inventory_trade(character_name_a, item_to_trade_b)
                                return False          
                else:
                        return False 
        else:
                return False