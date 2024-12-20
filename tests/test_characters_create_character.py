import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import unittest
import logging
from unittest.mock import patch, AsyncMock, MagicMock
from utils.impl.charactersimpl import create_logic, add_stat_logic
# rest of your code

class TestCreateCharacterLogic(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        # Assuming logging setup for debugging
        logging.basicConfig(level=logging.DEBUG)
        
    async def asyncSetUp(self):
        # Setup mocks before each test method
        self.mock_get_db_connection = patch('utils.functions.database_functions.get_db_connection', AsyncMock(return_value=(AsyncMock(), AsyncMock()))).start()
        self.mock_check_character_exists = patch('utils.functions.character_functions.check_character_exists', AsyncMock()).start()
        self.mock_create_character = patch('utils.functions.character_functions.create_character', AsyncMock()).start()
        self.addCleanup(patch.stopall)

    # Test 1: Valid character data
    async def test_create_logic_success(self):
        # Explicitly setting return values for this test case for clarity
        self.mock_get_db_connection.return_value = (AsyncMock(), AsyncMock())  # Simulating DB connection
        self.mock_create_character.return_value = "Character created successfully."
        # Setup the scenario where the character does not exist
        self.mock_check_character_exists.return_value = AsyncMock(return_value=False)
        self.mock_create_character.return_value = AsyncMock(return_value="Character created successfully.")

        character_data = {
            "first_name": "Silica",
            "last_name": "Kazuto",
            "characters_name": "Silica",
            "height": "5'2\"",
            "physique": "petite",
            "age": "12",
            "birthday": "1/2/1122",
            "bio": "A young girl who loves vrmmos.",
            "level": "1",
            "discord_tag": 1234567890,
            "guild_id": 1234567890
 }
        
        result = await create_logic(character_data)
        
        # logging.info(f"Test result: {result}")  # Debugging output

        # Assertion adjusted for explicit mock behavior
        self.assertEqual(result, "```Character created successfully.```")

    # Test 2: Existing character
    async def test_create_logic_failure(self):
        # Explicitly setting return values for this test case for clarity
        self.mock_get_db_connection.return_value = (AsyncMock(), AsyncMock())  # Simulating DB connection
        self.mock_create_character.return_value = "Character already exists."
        # Setup the scenario where the character already exists
        self.mock_check_character_exists.return_value = AsyncMock(return_value=True)

        character_data = {
            "first_name": "Kirigaya",
            "last_name": "Kazuto",
            "characters_name": "test_character_01",
            "height": "5'2\"",
            "physique": "muscular",
            "age": "12",
            "birthday": "1/2/1122",
            "bio": "A young boy who loves vrmmos.",
            "level": "1",
            "discord_tag": 1234567890,
            "guild_id": 1234567890
        }
        
        result = await create_logic(character_data)
        
        # logging.info(f"Test result: {result}")  # Debugging output

        # Assertion adjusted for explicit mock behavior
        self.assertEqual(result, "```Character already exists.```")
        
    # Test 3: Add points to stat    
    async def test_add_stats_logic_success(self):
        # Explicitly setting return values for this test case for clarity
        self.mock_get_db_connection.return_value = (AsyncMock(), AsyncMock())  # Simulating DB connection
        self.mock_create_character.return_value = "Character already exists."
        # Setup the scenario where the character already exists
        self.mock_check_character_exists.return_value = AsyncMock(return_value=True)

        character_data = {
            "stat_name": "attack",
            "stat_value": 1,
            "discord_tag": 1000000000,
            "guild_id": 1234567890
        }
        
        result = await add_stat_logic(character_data)
        
        # logging.info(f"Test result: {result}")  # Debugging output

        # Assertion adjusted for explicit mock behavior
        self.assertEqual(result, f"```{character_data['stat_value']} point(s) added to str for {character_data['discord_tag']}```")
        

 
if __name__ == "__main__":
    unittest.main()