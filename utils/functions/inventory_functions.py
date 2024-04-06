import logging
import math
from utils.functions.character_functions import get_active_character
from utils.functions.item_functions import get_item
from utils.functions.database_functions import get_db_connection, close_db_connection

# Characters
#_______________________________________________________________________________________________________________________

# add character data to an object
async def add_item_to_inventory(character_data, item_data):
    client, db = await get_db_connection()
    if db is None:
        return f"Failed to connect to the database."

    try:
        character_document = await get_active_character(db, character_data)
        if not character_document:
            return f"Character not found."
        item_document = await get_item(db, item_data)
        if not item_document:
            return f"Item not found."
        logging.info(f"Item found: {item_document['name']}")

        # Check if the item already exists in the user's inventory
        item_exists = check_item_exists_in_inventory(character_document, item_data)
        
        # If the iten does not exist, append it to the inventory
        logging.info(f"Item exists: {item_exists}")
        if not item_exists:
            # If the item does not exist, append it to the inventory
            character_document["inventory"][item_document["inventory_field"]].append({
                "oid": item_document["_id"],
                "name": item_data["name"],
                "quantity": item_data["quantity"]
            })
        # Update the user document with the modified inventory
        update = await db["characters"].update_one({"_id": character_document["_id"]}, 
                                     {"$set": {"inventory.equipment": character_document["inventory"]["equipment"]}})
        
        if update.modified_count < 0:
            return f"Item not added!: {item_data['name']}"
        return f"Item added successfully!: {item_data['name']}"
    
    except Exception as e:
        print(f"An error occurred: {e}")
        return f"An error occurred while adding the item."
    finally:
        await close_db_connection(client)

# Remove an item from the users inventory
async def remove_item_from_inventory(character_data, item_data):
    client, db = await get_db_connection()
    if db is None:
        return f"Failed to connect to the database."

    try:
        character_document = await get_active_character(db, character_data)
        if not character_document:
            return f"Character not found."
        item_document = await get_item(db, item_data)
        if not item_document:
            return f"Item not found."
        logging.info(f"Item found: {item_document['name']}")

        # Check if the item exists in the user's inventory
        item_exists = check_item_exists_in_inventory(character_document, item_data)
        
        logging.info(f"Item exists: {item_exists}")
        
        if item_exists:
            # If the item exists, remove it from the inventory
            character_document["inventory"][item_document["inventory_field"]].remove({
                "oid": item_document["_id"],
            })
            logging.info(f"Item removed: {item_document['name']}")
        else:
            return f"Item not found in inventory."

    except Exception as e:
        logging.error(f"Failed to remove item from inventory: {str(e)}")
        return f"Failed to remove item from inventory: {str(e)}"

    finally:
        close_db_connection(client)
        
def check_item_exists_in_inventory(character_document, item_data):
    # Initialize item_exists to False
    item_exists = False
    
    # Iterate over each equipment_item in the character's equipment array
    for equipment_item in character_document["inventory"]["equipment"]:
        # Log the name of the current equipment item
        logging.info(f"Equipment item: {equipment_item}")

        # Check if the current equipment_item's name matches the item_data name
        if equipment_item["name"] == item_data["name"]:
            logging.info(f"Item exists in inventory: {item_data['name']}")
            
            # If a match is found, increase the quantity of the equipment item
            item_exists = True
            break

    return item_exists

def update_quantity(character_document, item_data, add_or_remove):
    # Iterate over each equipment_item in the character's equipment array
    for equipment_item in character_document["inventory"]["equipment"]:
        # Log the name of the current equipment item
        logging.info(f"Equipment item: {equipment_item}")

        # Check if the current equipment_item's name matches the item_data name
        if equipment_item["name"] == item_data["name"]:
            logging.info(f"Item exists in inventory: {item_data['name']}")

            # If a match is found, increase the quantity of the equipment item
            if add_or_remove == "add":
                equipment_item["quantity"] += item_data["quantity"]
            else:
                equipment_item["quantity"] -= item_data["quantity"]
                if equipment_item["quantity"] <= 0:
                    character_document["inventory"]["equipment"].remove(equipment_item)
            break
    return character_document
