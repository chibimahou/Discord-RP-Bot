import discord
import sqlite3
import os
import re
import pytz
from datetime import datetime, timedelta
import math as mat
import function_calls.calc as calc
import function_calls.query.query as que
from discord.ext import commands
from discord import app_commands
from discord.utils import get

def request_party_invite(character_name_a, character_name_b, discord_tag):
        """_summary_
                Sends a party invite request to character_name_b from character_name_a.
                Convert the character names to lowercase and check if each user exists in the charactersheets table.
                If users do not exist, return False, if they do, return true.
        Args:
            character_name_a (_type_): Person who called the command
            character_name_b (_type_): Person being interacted with
            discord_tag (_type_): Unique discord account code

        Returns:
            _type_: Message to display to users
        """
        
#Validates fields are expected values    
        if(calc.validate_fields(character_name_a) == True and  calc.validate_fields(character_name_b) == True):
                #KYZEN -> kyzen
                character_name_a_lower = character_name_a.lower()
                character_name_b_lower = character_name_b.lower()
                #Kyzen is an actual player (l)
                character_a = calc.verify_player_exists(character_name_a_lower)
                character_b = calc.verify_player_exists(character_name_b_lower)
                #If both players exist
                if character_a == True and character_b == True:
                        #Check if the invitee is in a party already
                        if(in_party(character_name_b_lower)):
                                return("""```""" + character_name_b_lower + """ is already in a party.```""")
                        #Checks if invite exists already
                        if(invite_exists(character_name_a_lower, character_name_b_lower)):
                                return("""```An invite was already sent to this player. Please wait until they respond or the request expires in 30 minutes from the original request.```""")
                        #Invite does not already exist
                        else:
                                sqliteConnection = sqlite3.connect('characterSheet.db')
                                sqliteConnection2 = sqlite3.connect('sessions.db')
                                cursor = sqliteConnection.cursor()
                                cursor2 = sqliteConnection2.cursor()
                                #If the party exists
                                if(in_party(character_name_a_lower)):
                                        #Create a party for the inviter
                                        party_id = calc.create_invite_id(character_name_a_lower)  
                                        #Create a unique ID for the party invite
                                        invite_id = calc.create_invite_id(character_name_a_lower + character_name_b_lower)
                                        query2 = que.invite_sessions()
                                        cursor2.execute(query2, (invite_id, character_name_a_lower, character_name_b_lower, party_id, calc.get_current_datetime()))
                                        sqliteConnection2.commit()
                                        sqliteConnection.close()
                                        sqliteConnection2.close()
                                        return('```' + character_name_a_lower + ' has sent ' + character_name_b_lower + ' a party invite.\n\n Use the command \'/accept_or_decline_party_invite to reply.\'```')   

                                #If the party does not exist
                                else:
                                        #Create a unique ID for the party invite
                                        invite_id = calc.create_invite_id(character_name_a_lower + character_name_b_lower)
                                        party_id = calc.create_invite_id(character_name_a_lower)  
                                        query2 = que.invite_sessions()
                                        cursor2.execute(query2, (invite_id, character_name_a_lower, character_name_b_lower, party_id, calc.get_current_datetime()))
                                        sqliteConnection2.commit()
                                        #Create party in party table
                                        query = que.add_party_sessions()
                                        cursor2.execute(query, (party_id, character_name_a_lower, "", 1))
                                        sqliteConnection2.commit()
                                        query = que.add_party_charactersheets()
                                        cursor.execute(query, (party_id, character_name_a_lower, discord_tag))
                                        sqliteConnection.commit()             
                                        sqliteConnection.close()
                                        sqliteConnection2.close()
                                        return('```' + character_name_a_lower + ' has sent ' + character_name_b_lower + ' a party invite.\n\n Use the command \'/accept_or_decline_party_invite to reply!\'```')   
                else:
                        return("""```Sorry, but one of these characters do not exist.```""")        
        return('```One of the character names do not exist.```')
    
def get_session_db():
        sqliteConnection = sqlite3.connect('sessions.db')
        cursor = sqliteConnection.cursor()
        query = """SELECT *
                   FROM invites"""
        party_exists = cursor.execute(query).fetchall()
        if(party_exists):
                print("Printing session DB:")
                print()
                for row in party_exists:
                        for value in row:
                                print(value, end=' ')
                        print()
                return "Success"
        else:
               print("Failure, no items")
               return "Fail"

def get_party_db():
        sqliteConnection = sqlite3.connect('sessions.db')
        cursor = sqliteConnection.cursor()
        query = """SELECT *
                   FROM party"""
        party_exists = cursor.execute(query).fetchall()
        if(party_exists):
                print("Printing session DB:")
                print()
                for row in party_exists:
                        for value in row:
                                print(value, end=' ')
                        print()
                return "Success"
        else:
               print("Failure, no items")
               return "Fail"
       
def get_character_db():
        sqliteConnection = sqlite3.connect('characterSheet.db')
        cursor = sqliteConnection.cursor()
        characters = ["kotori", "kyzen"]
        query = """SELECT *
                   FROM charactersheets"""
        party_exists = cursor.execute(query).fetchall()
        if(party_exists):
                print("Printing session DB:")
                print()
                for row in party_exists:
                        for value in row:
                                print(value, end=' ')
                        print()
                return "Success"
        else:
               print("Failure, no items")
               return "Fail"
        
def accept_or_decline_party_invite(character_name_a, character_name_b, accept_or_decline, discord_tag):
    if(calc.validate_fields(character_name_a) == True and  calc.validate_fields(character_name_b) == True):
        #Convert the variables to lower case
        character_name_a_lower = character_name_a.lower()
        character_name_b_lower = character_name_b.lower()
        accept_or_decline_lower = accept_or_decline.lower()
        character_a = calc.verify_player_exists(character_name_a_lower)
        character_b = calc.verify_player_exists(character_name_b_lower)
        #if players exist in the database
        if character_a == True and character_b == True:
                #If player input an invalid response
                if accept_or_decline_lower != "accept" and accept_or_decline_lower != "decline":
                        return('``` Please input \'accept\' or \'decline\' in the accept_or_decline field.```')   
                #If player input a valid response
                else: 
                        sqliteConnection = sqlite3.connect('characterSheet.db')
                        sqliteConnection2 = sqlite3.connect('sessions.db')
                        cursor = sqliteConnection.cursor()
                        cursor2 = sqliteConnection2.cursor()
                        if(invite_exists(character_name_b_lower, character_name_a_lower)):
                                #If player accepted the party invite
                                if accept_or_decline_lower == "accept":
                                        party_id = calc.create_invite_id(character_name_b_lower)
                                        query = que.add_party_charactersheets()
                                        cursor.execute(query, (party_id, character_name_a_lower, discord_tag))
                                        remove_invite(character_name_b_lower, character_name_a_lower)
                                        sqliteConnection.commit()
                                        #Get party information.
                                        query = que.get_party_information()
                                        party_info = cursor2.execute(query, (party_id,)).fetchone()
                                        
                                        player_count = party_info[1] + 1
                                        print(player_count)
                                        if(player_count > 6):
                                                sqliteConnection.close()
                                                sqliteConnection2.close()
                                                return('```Sorry, this party is currently full.```')
                                        else:
                                                party_members = calc.remove_white_spaces_around_commas(party_info[0])
                                                print(party_members)
                                                added_player_to_party_string = calc.concatenate_string(party_members, character_name_a_lower, "add")
                                                print(added_player_to_party_string)
                                                query = que.update_party_sessions()
                                                cursor2.execute(query,(player_count, added_player_to_party_string, party_id))
                                                sqliteConnection2.commit()
                                                sqliteConnection2.close()
                                                return("""```Success! """ + character_name_a_lower + """ has been added to the party!```""")
                                else:
                                        remove_invite(character_name_b_lower, character_name_a_lower)
                                        sqliteConnection.close()
                                        sqliteConnection2.close()
                                        return('```' + character_name_b + ' has declined your party invite.```')
                        else:
                                return("""```This invite does not exist or has expired.```""")
        return('``` One of the character names do not exist.```')

def leave_party(character_name_a, discord_tag):
        if(calc.validate_fields(character_name_a) == True):
                #Convert the variables to lower case
                character_name_a_lower = character_name_a.lower()
                character_a = calc.verify_player_exists(character_name_a_lower)
                #if players exist in the database
                if character_a == True:                
                        sqliteConnection = sqlite3.connect('characterSheet.db')
                        sqliteConnection2 = sqlite3.connect('sessions.db')
                        cursor = sqliteConnection.cursor()
                        cursor2 = sqliteConnection2.cursor()
                        if(in_party(character_name_a_lower)):
                                query = que.get_party_id_charactersheets()
                                players_party_id = cursor.execute(query,(character_name_a_lower,)).fetchone()
                                query = que.get_party_information()
                                party_info = cursor2.execute(query,(players_party_id[0],)).fetchone()
                                player_count = party_info[1] - 1
                                print("count" + str(player_count))
                                player = players_party_id[0]
                                if player_count <= 0:                  
                                        query = que.remove_party_sessions()
                                        cursor2.execute(query,(players_party_id[0],))
                                        sqliteConnection2.commit()
                                        query = que.remove_party_charactersheets()
                                        cursor.execute(query,(character_name_a_lower,))
                                        sqliteConnection.close()
                                        sqliteConnection2.close()
                                        return("""```There are no players in the party. It has been disbanded.```""")
                                else:
                                        print("info" + str(party_info))
                                        party_members = calc.remove_white_spaces_around_commas(party_info[0])
                                        if party_info[2] == players_party_id[0]:
                                                print(party_members)
                                                print([players_party_id[0]])
                                                character_information = calc.get_character_information(party_members[1])
                                                player = character_information[23]
                                                users_with_party_id = [players_party_id[0]] + party_members
                                                query = que.update_all_players_in_party_charactersheet(party_members)
                                                cursor.execute(query, tuple(users_with_party_id))
                                        print("members" + str(party_members))
                                        removed_player_to_party_string = calc.concatenate_string(party_members, character_name_a_lower, "remove")
                                        print(removed_player_to_party_string)

                                        query = que.remove_party_charactersheets()
                                        cursor.execute(query,(character_name_a_lower,))
                                        query = que.update_party_sessions()
                                        cursor2.execute(query,(player_count, removed_player_to_party_string, player))
                                        sqliteConnection.commit()
                                        sqliteConnection2.commit()
                                        sqliteConnection2.close()
                                        return("""```""" + character_name_a_lower + """ has successfully left the party.""")
                                                
                else:
                        return("""```One of the character you input does not exist.```""")     
        return('``` The values you entered are invald.```')        
#Sends a party invite request to character_name_b from character_name_a.
#Convert the character names to lowercase and check if each user exists in the charactersheets table.
#If users do not exist, return False, if they do, return true.
def request_guild_invite(character_name_a, character_name_b, guild_name):
    if(calc.validate_fields(character_name_a) == True and  calc.validate_fields(character_name_b) == True):
        character_a = calc.verify_player_exists(character_name_a)
        character_b = calc.verify_player_exists(character_name_b)
        guild_a = calc.verify_guild_exists(guild_name)
        approver_a = calc.check_guild_approvers(character_name_a, guild_name)
        guild_name_lower = guild_name.lower()
        if character_a == True and character_b == True:
                if guild_a == True:
                        if approver_a == True:
                                return('```' + character_name_a + ' sent a guild invite to ' + character_name_b + '.```') 
                        else:
                                return('```' + character_name_a + ' is not an approver for the guild: ' + guild_name_lower + '```')
                return('```The guild name you input does not exist.```') 
        return('```One of the character names do not exist.```') 

def accept_or_decline_guild_invite(character_name_a, character_name_b, guild_name, accept_or_decline):
    if(calc.validate_fields(character_name_a) == True and  calc.validate_fields(character_name_b) == True):
        character_a = calc.verify_player_exists(character_name_a)
        character_b = calc.verify_player_exists(character_name_b)
        guild_a = calc.verify_guild_exists(guild_name)
        if character_a == True and character_b == True:
                if guild_a == True:
                       accept_or_decline_lower = accept_or_decline.lower()
                if accept_or_decline_lower != "accept" and accept_or_decline_lower != "decline":
                        return('``` Please input \'accept\' or \'decline\' in the accept_or_decline field.```')   
                else: 
                        if accept_or_decline_lower == "accept":
                                add_to_guild = calc.add_to_guild(character_name_b, guild_name)
                                if add_to_guild == True:
                                        return('```' + character_name_b + ' has accepted your guild invite.```')   
                                else:
                                        return('``` Something went wrong adding the user to the guild. ```')
                        return('```' + character_name_b + ' has declined your party invite.```')
        return('``` One of the character names do not exist.```')
    
def invite_exists(character_name_a, character_name_b):
        #Create invite_id
        invite_id = calc.create_invite_id(character_name_a + character_name_b)
        print(invite_id)
        sqliteConnection = sqlite3.connect('sessions.db')
        cursor = sqliteConnection.cursor()
        query = que.invite_valid_sessions()
        invite = cursor.execute(query, (invite_id,)).fetchone()
        if(invite is None):
                return False
        else:
                # Assuming the DateField is in UTC and invite[1] contains a string representation of the date
                utc_date_str = invite[1]

                # Define the UTC and EST timezones
                est_tz = pytz.timezone('America/New_York')

                # Convert the UTC date to the EST timezone
                est_date = datetime.fromisoformat(utc_date_str)

                # Get the current time in the EST timezone
                current_time_est = datetime.now(est_tz)
                print(est_date)
                print(">=")
                # Check if the date was created within the last 30 minutes
                thirty_minutes_ago = current_time_est - timedelta(minutes=30)
                thirty_minutes_ago_utc = thirty_minutes_ago.astimezone(pytz.utc)
                est_date_utc = est_date.astimezone(pytz.utc)

                print(thirty_minutes_ago_utc)
                if thirty_minutes_ago_utc >= est_date_utc:
                        remove_invite(character_name_a, character_name_b)
                        sqliteConnection.commit()
                        cursor.close()
                        sqliteConnection.close()
                        return False
                else:
                        cursor.close()
                        sqliteConnection.close()
                        return True
        
def remove_invite(character_name_a, character_name_b):
       try:
                invite_id = calc.create_invite_id(character_name_a + character_name_b)
                sqliteConnection = sqlite3.connect('sessions.db')
                cursor = sqliteConnection.cursor()
                query = que.remove_invite_sessions()
                cursor.execute(query, (invite_id,)).fetchone()
                sqliteConnection.commit()
                cursor.close()
                sqliteConnection.close()
                return True
       except Exception as e:
               print("Failed to find invite: ", e)
               return False
       
def in_party(character_name):
        sqliteConnection = sqlite3.connect('characterSheet.db')
        cursor = sqliteConnection.cursor()
        query = que.get_party_id_charactersheets()
        empty = ""
        party_exists = cursor.execute(query, (character_name,)).fetchone()
        print(party_exists[0])
        if party_exists[0] == "\"\"" or party_exists[0] == "":
                print("IF: Not in a party")
                return False
        else:
                print("ELSE: In a party")
                return True              


        