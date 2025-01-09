import logging
import math
from utils.functions.character_functions import get_active_character
from utils.functions.item_functions import get_item
from utils.functions.database_functions import get_db_connection, close_db_connection
from utils.functions.utility_functions import comment_wrap
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
        item_document = await get_item(db, item_data["identifier", character_data["guild_id"]])
        if not item_document:
            return f"Item not found."
        logging.info(f"Item found: {item_document['name']}")

        # Check if the item already exists in the user's inventory
        item_exists = await update_quantity_or_check_item_exists(character_document, item_document["inventory_field"], item_data, "add")
        # If the iten does not exist, append it to the inventory
        logging.info(f"Item data: {character_document['inventory'][item_document['inventory_field']]}")
        if item_exists == False:
            # If the item does not exist, append it to the inventory
            character_document["inventory"][item_document["inventory_field"]].append({
                "oid": item_document["_id"],
                "name": item_data["name"],
                "quantity": item_data["quantity"]
            })
        # Update the user document with the modified inventory
        update = await db["characters"].update_one({"_id": character_document["_id"]}, 
                                     {"$set": {f"inventory.{item_document['inventory_field']}": character_document["inventory"][item_document["inventory_field"]]}})
        
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
        
        item_document = await get_item(db, item_data["identifier"], character_data["guild_id"])
        if not item_document:
            return f"Item not found."
        
        logging.info(f"Item found: {item_document['name']}")
        
        # Check if the item exists in the user's inventory
        item_exists = await update_quantity_or_check_item_exists(character_document, item_document["inventory_field"], item_data , "remove")
        
        logging.info(f"Item exists: {item_exists}")
        
        if item_exists:
            # Update the user document with the modified inventory
            update = await db["characters"].update_one({"_id": character_document["_id"]}, 
                             {"$set": {f"inventory.{item_document['inventory_field']}": character_document["inventory"][item_document["inventory_field"]]}})
        
            logging.info(f"Item removed: {item_document['name']}")
            if update.modified_count < 0:
                return f"Failed to remove item from inventory: {item_document['name']}"
            return f"Item removed successfully: {item_document['name']}"
        
        else:
            return f"Item not found in inventory."

    except Exception as e:
        logging.error(f"Failed to remove item from inventory: {str(e)}")
        return f"Failed to remove item from inventory: {str(e)}"

    finally:
        await close_db_connection(client)

async def check_inventory(character_data):
    client, db = await get_db_connection()
    if db is None:
        return "Failed to connect to the database."

    try:
        character_document = await get_active_character(db, character_data)
        if not character_document:
            return "Character not found."
        logging.info(f"Character found: {character_document['character']['characters_name']}")
        # Assuming the inventory structure is known and consistent
        inventory = character_document["inventory"]
        inventory_str_list = []  # List to hold inventory string descriptions
        logging.info(f"Inventory: {inventory}")
        # Iterate over each category in the inventory (e.g., 'equipment', 'consumables')
        for category, items in inventory.items():
            logging.info(f"Category: {category}")
            # Add the category name to the string list
            inventory_str_list.append(f"{category.capitalize()}:")
            logging.info(f"Items1: {items}")
            # Iterate over each item in the category
            for item in items:
                logging.info(f"Item2: {item}")
                # Assuming each item is a dictionary with 'name' and 'quantity'
                item_str = f" - {item['name'].capitalize()}: {item['quantity']}"
                inventory_str_list.append(item_str)

        # Join all the strings in the list into a single string to return
        inventory_str = "\n".join(inventory_str_list)
        return await comment_wrap(inventory_str)
    except Exception as e:
        logging.error(f"Failed to check inventory: {str(e)}")
        return f"Failed to check inventory: {str(e)}"
    finally:
        await close_db_connection(client)
        
async def update_quantity_or_check_item_exists(character_document, inventory_field, item_data, add_or_remove):
    # Iterate over each equipment_item in the character's equipment array
    for equipment_item in character_document["inventory"][inventory_field]:
        # Log the name of the current equipment item
        logging.info(f"Equipment item: {equipment_item}")

        # Check if the current equipment_item's name matches the item_data name
        if equipment_item["name"] == item_data["name"]:
            logging.info(f"Item exists in inventory: {item_data['name']}")

            # If a match is found, increase the quantity of the equipment item
            if add_or_remove == "check":
                break
            if add_or_remove == "add":
                equipment_item["quantity"] += item_data["quantity"]
            else:
                equipment_item["quantity"] -= item_data["quantity"]
                if equipment_item["quantity"] <= 0:
                    character_document["inventory"][inventory_field].remove(equipment_item)
                    
            logging.info(f"Item quantity updated: {character_document['inventory'][inventory_field]}")
            return True
    return False
