import re
import discord
from datetime import datetime

def validate_alphanumeric(input_str):
    pattern = re.compile(r'^\w+$')
    return bool(pattern.match(input_str))

def validate_height(input_str):
    patterns = [
        re.compile(r"^(?P<feet>\d+)'(?P<inches>\d+)\"$"),  # 5'10"
        re.compile(r"^(?P<feet>\d+)' (?P<inches>\d+)\"$"),  # 5' 10"
        re.compile(r"^(?P<feet>\d+)ft (?P<inches>\d+)in$"),  # 5ft 10in
        re.compile(r"^(?P<inches>\d+)\"$"),  # 70"
        re.compile(r"^(?P<inches>\d+)in$"),  # 70in
        re.compile(r"^(?P<cm>\d+)cm$"),  # 180cm
        re.compile(r"^(?P<cm>\d+) cm$"),  # 180 cm
    ]
    
    for pattern in patterns:
        match = pattern.match(input_str)
        if match:
            if 'feet' in match.groupdict() and 'inches' in match.groupdict():
                feet = int(match.group('feet'))
                inches = int(match.group('inches'))
                total_inches = feet * 12 + inches
                return total_inches  # or return as a tuple (feet, inches)
            elif 'inches' in match.groupdict():
                return int(match.group('inches'))
            elif 'cm' in match.groupdict():
                cm = int(match.group('cm'))
                inches = cm / 2.54
                return round(inches)  # or return cm if you prefer
    raise ValueError(f"Height format for '{input_str}' is not supported.")


def validate_age(input_str):
    return input_str.isdigit()

def validate_date(input_str):
    date_formats = [
        '%m/%d/%Y',  # 12/25/2022
        '%d/%b/%Y',  # 25/DEC/2022
        '%d-%b-%Y',  # 25-DEC-2022
        '%Y-%m-%d',  # 2022-12-25
        '%d %B %Y',  # 25 December 2022
        '%d %b %Y',  # 25 Dec 2022
        '%d/%m/%Y',  # 25/12/2022
        '%d-%m-%Y',  # 25-12-2022
    ]
    
    for date_format in date_formats:
        try:
            return datetime.strptime(input_str, date_format)
        except ValueError:
            continue
    raise ValueError(f"Date format for '{input_str}' is not supported.")


def validate_text(input_str):
    pattern = re.compile(r"^[a-zA-Z0-9.,'\"!? ]+$")
    return bool(pattern.match(input_str))

def validate_level(input_str):
    return input_str.isdigit() and int(input_str) >= 0

# Database Validations
async def validate_exists(db, entity_type, entity_data):
    if entity_type == "character":
        return await validate_character_exists(db, entity_data)
    elif entity_type == "item":
        return await validate_item_exists(db, entity_data)
    # Add more entity types as needed
    else:
        raise ValueError(f"Unknown entity type: {entity_type}")
    
async def validate_character_exists(db, character_data):
    character = await db['characters'].find_one({
        "misc.discord_tag": character_data["discord_tag"],
        "character.active": True})
    return character is not None

async def validate_item_exists(db, item_data):
    item = await db['items'].find_one({
        "item.name": item_data["name"]})
    return item is not None

async def validate_mobs_exists(db, item_data):
    item = await db['mobs'].find_one({
        "mob.name": item_data["name"]})
    return item is not None

async def validate_party_exists(db, item_data):
    item = await db['party'].find_one({
        "party.party_id": item_data["party_id"]})
    return item is not None

async def validate_guild_exists(db, item_data):
    item = await db['guild'].find_one({
        "guild.guild_id": item_data["guild_id"]})
    return item is not None

