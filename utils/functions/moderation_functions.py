import logging
from utils.functions.database_functions import get_db_connection, close_db_connection

# moderation
#_______________________________________________________________________________________________________________________

# Add points to the assigned stat
async def add_points_to_stat(discord_tag, guild_id, character_name, stat_updates):
    client, db = await get_db_connection()
    try:
        # Ensure 'stat_updates' is a dictionary with stats as keys and points as values
        if not isinstance(stat_updates, dict):
            return "Invalid stat updates format. Expected a dictionary."

        # Prepare the update document using the stat updates
        update_doc = {"$inc": {f"stats.{stat}": points for stat, points in stat_updates.items()}}

        # Update the character's stats
        result = await db["characters"].update_one(
            {"discord_tag": discord_tag, "characters_name": character_name, "guild_id": guild_id},
            update_doc
        )

        if result.modified_count > 0:
            return "Stats updated successfully!"
        else:
            return "Character not found or no update needed."
    except Exception as e:
        logging.exception("Error adding points to stats")
        return "An error occurred while adding points to stats."
    finally:
        await close_db_connection(client)