import unittest
import logging
from unittest.mock import patch, AsyncMock, MagicMock
from utils.impl.charactersimpl import create_logic


class TestCreateCharactersLogic(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        # Assuming logging setup for debugging
        logging.basicConfig(level=logging.DEBUG)
        
    async def asyncSetUp(self):
        # Setup mocks before each test method
        self.mock_get_db_connection = patch('utils.functions.database_functions.get_db_connection', AsyncMock(return_value=(AsyncMock(), AsyncMock()))).start()
        self.mock_check_character_exists = patch('utils.functions.character_functions.check_character_exists', AsyncMock()).start()
        self.mock_create_character = patch('utils.functions.character_functions.create_character', AsyncMock()).start()
        self.addCleanup(patch.stopall)

    async def test_create_logic_success(self):
        # Explicitly setting return values for this test case for clarity
        self.mock_get_db_connection.return_value = (AsyncMock(), AsyncMock())  # Simulating DB connection
        self.mock_create_character.return_value = "Character created successfully."
        # Setup the scenario where the character does not exist
        self.mock_check_character_exists.return_value = AsyncMock(return_value=False)
        self.mock_create_character.return_value = AsyncMock(return_value="Character created successfully.")

        # Test 1: Valid character data
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
        self.assertEqual(result, "```Character created successfully.```")

    async def test_create_logic_failure(self):
        # Explicitly setting return values for this test case for clarity
        self.mock_get_db_connection.return_value = (AsyncMock(), AsyncMock())  # Simulating DB connection
        self.mock_create_character.return_value = "Character created successfully."
        # Setup the scenario where the character already exists
        self.mock_check_character_exists.return_value = AsyncMock(return_value=True)

        # Test 2: Existing character
        character_data = {
            "first_name": "Asuna",
            "last_name": "Yuuki",
            "characters_name": "test_character_02",
            "height": "5'2\"",
            "physique": "Slim",
            "age": "12",
            "birthday": "3/2/1122",
            "bio": "A young girl who loves vrmmos.",
            "level": "1",
            "discord_tag": 1234567891,
            "guild_id": 1234567890
 }
        
        result = await create_logic(character_data)
        
        # logging.info(f"Test result: {result}")  # Debugging output

        # Assertion adjusted for explicit mock behavior
        self.assertEqual(result, "```Character created successfully.```")
        
if __name__ == "__main__":
    unittest.main()