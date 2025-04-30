import unittest
import logging
from unittest.mock import patch, AsyncMock
from utils.functions.combat_functions import (is_players_turn, start_combat)

class TestCombatFunctions(unittest.IsolatedAsyncioTestCase):
    
    async def asyncSetUp(self):
        # Assuming logging setup for debugging
        logging.basicConfig(level=logging.DEBUG)
        
    async def asyncSetUp(self):
        self.mock_get_db_connection = patch('utils.functions.database_functions.get_db_connection', AsyncMock(return_value=(AsyncMock(), AsyncMock()))).start()
        self.mock_check_character_exists = patch('utils.functions.character_functions.check_character_exists', AsyncMock()).start()
        self.mock_create_character = patch('utils.functions.character_functions.create_character', AsyncMock()).start()
        # Setup mocks before each test method
        self.addCleanup(patch.stopall)

    # Test 1: Start Combat Success
    @patch('utils.functions.database_functions.get_db_connection', new_callable=AsyncMock)
    async def test_begin_combat(self, mock_get_db_connection):
        mock_db = AsyncMock()
        mock_get_db_connection.return_value = (mock_db, AsyncMock())
        mock_db["combat"].find_one.return_value = None

        result = await start_combat(mock_db, "guild_1", "combat_instance_1")
        
        # logging.info(f"Test result: {result}")  # Debugging output

        # Assertion adjusted for explicit mock behavior
        self.assertTrue(result)
    # Test 1: Valid character data
    @patch('utils.functions.database_functions.get_db_connection', new_callable=AsyncMock)
    async def test_is_players_turn_success(self, mock_get_db_connection):
        mock_db = AsyncMock()
        mock_get_db_connection.return_value = (mock_db, AsyncMock())
        mock_db["combat"].find_one.return_value = {
            "combat": {
                "players_turn": "1234567890"
            },
            "instance": "combat_instance_1",
            "guild_id": "guild_1"
        }

        character_data = {
            "character": {
                "instance": "combat_instance_1"
            },
            "guild_id": "guild_1",
            "discord_tag": "1234567890"
        }
        result = await is_players_turn(mock_db, character_data)
        
        # logging.info(f"Test result: {result}")  # Debugging output

        # Assertion adjusted for explicit mock behavior
        self.assertTrue(result)
        
if __name__ == "__main__":
    unittest.main()