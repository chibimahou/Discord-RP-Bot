import unittest
import logging
from unittest.mock import patch, AsyncMock, MagicMock
from utils.impl.charactersimpl import (
    create_logic, add_stat_logic, 
    delete_logic, level_up_logic, switch_active_logic, all_available_logic)

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
    async def test_create_delete_character_logic_success(self):
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
        result_2 = await delete_logic(character_data)
        
        # logging.info(f"Test result: {result}")  # Debugging output

        # Assertion adjusted for explicit mock behavior
        self.assertEqual(result, "```Character created successfully.```")
        self.assertEqual(result_2, "```Character successfully deleted!```")

    # Test 2: Valid character data
    async def test_create_character_logic_success(self):
        # Explicitly setting return values for this test case for clarity
        self.mock_get_db_connection.return_value = (AsyncMock(), AsyncMock())  # Simulating DB connection
        self.mock_create_character.return_value = "Character created successfully."
        # Setup the scenario where the character does not exist
        self.mock_check_character_exists.return_value = AsyncMock(return_value=False)
        self.mock_create_character.return_value = AsyncMock(return_value="Character created successfully.")

        character_data = {
            "first_name": "Kirigaya",
            "last_name": "Kazuto",
            "characters_name": "Kirito",
            "height": "5'2\"",
            "physique": "petite",
            "age": "12",
            "birthday": "1/2/1122",
            "bio": "A young boy who loves vrmmos.",
            "level": "1",
            "discord_tag": 1234567891,
            "guild_id": 1234567890
 }
        character_data_2 = {
            "first_name": "Asuna",
            "last_name": "Yuuki",
            "characters_name": "Asuna",
            "height": "5'2\"",
            "physique": "petite",
            "age": "12",
            "birthday": "2/4/2242",
            "bio": "A young girl who loves vrmmos.",
            "level": "1",
            "discord_tag": 1234567891,
            "guild_id": 1234567890
 }
        character_data_3 = {
            "first_name": "Lisbeth",
            "last_name": "Lisbeth",
            "characters_name": "Lisbeth",
            "height": "5'2\"",
            "physique": "petite",
            "age": "12",
            "birthday": "2/4/2242",
            "bio": "A young girl who loves vrmmos.",
            "level": "1",
            "discord_tag": 1234567892,
            "guild_id": 1234567890
 }
        
        result = await create_logic(character_data)
        result_2 = await create_logic(character_data_2)
        result_3 = await create_logic(character_data_3)

        # logging.info(f"Test result: {result}")  # Debugging output

        # Assertion adjusted for explicit mock behavior
        self.assertEqual(result, "```Character created successfully.```")
        self.assertEqual(result_2, "```Character created successfully.```")
        self.assertEqual(result_3, "```Character created successfully.```")

    # Test 2: Existing character
    async def test_create_logic_exists_failure(self):
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
    @patch('utils.functions.character_functions.get_db_connection', new_callable=AsyncMock)
    @patch('utils.functions.character_functions.create_character', new_callable=AsyncMock)
    @patch('utils.functions.character_functions.check_character_exists', new_callable=AsyncMock)
    async def test_level_up_add_stats_logic_success(self, mock_check_character_exists, mock_create_character, mock_get_db_connection):
        # Explicitly setting return values for this test case for clarity
        mock_get_db_connection.return_value = (AsyncMock(), AsyncMock())  # Simulating DB connection
        mock_create_character.return_value = "Character already exists."
        # Setup the scenario where the character already exists
        mock_check_character_exists.return_value = True

        character_data = {
            "discord_tag": 1234567891,
            "guild_id": 1234567890
 }
        
        character_stats = {
            "stat_name": "attack",
            "stat_value": 1,
            "discord_tag": 1234567891,
            "guild_id": 1234567890
        }
        
        result = await level_up_logic(character_data)
        result_2 = await add_stat_logic(character_stats)
        
        # logging.info(f"Test result: {result}")  # Debugging output

        # Assertion adjusted for explicit mock behavior
        self.assertEqual(result, f"```Level up! You are now level. You have 3 points to distribute.```")
        self.assertEqual(result_2, f"```1 point(s) added to str for 1234567891```")
        
    @patch('utils.impl.charactersimpl.get_db_connection', new_callable=AsyncMock)
    @patch('utils.impl.charactersimpl.active_character', new_callable=AsyncMock)
    @patch('utils.impl.charactersimpl.get_character_by_name', new_callable=AsyncMock)
    @patch('utils.impl.charactersimpl.switch_active_character', new_callable=AsyncMock)
    @patch('utils.impl.charactersimpl.comment_wrap', new_callable=AsyncMock)
    async def test_switch_active_logic_success(self, mock_comment_wrap, mock_switch_active_character, mock_get_character_by_name, mock_active_character, mock_get_db_connection):
        # Mocking the database connection
        mock_get_db_connection.return_value = (AsyncMock(), AsyncMock())
        
        # Mocking the active character retrieval
        mock_active_character.return_value = {'character': {'characters_name': 'old_character'}}
        
        # Mocking the new character retrieval
        mock_get_character_by_name.return_value = {'character': {'characters_name': 'new_character'}}
        
        # Mocking the switch active character function
        mock_switch_active_character.return_value = True
        
        # Mocking the comment_wrap function
        mock_comment_wrap.return_value = "Active character switched to new_character!"
        
        character_data = {
            "characters_name": "Asuna",
            "discord_tag": 1234567891,
            "guild_id": 1234567890
        }
        
        character_data = {
            "characters_name": "Kirito",
            "discord_tag": 1234567891,
            "guild_id": 1234567890
        }
        
        result = await switch_active_logic(character_data)
        result_2 = await switch_active_logic(character_data)

        self.assertEqual(result, "Active character switched to new_character!")
        self.assertEqual(result_2, "Active character switched to new_character!")

    @patch('utils.impl.charactersimpl.get_db_connection', new_callable=AsyncMock)
    @patch('utils.impl.charactersimpl.active_character', new_callable=AsyncMock)
    @patch('utils.impl.charactersimpl.get_character_by_name', new_callable=AsyncMock)
    @patch('utils.impl.charactersimpl.switch_active_character', new_callable=AsyncMock)
    @patch('utils.impl.charactersimpl.comment_wrap', new_callable=AsyncMock)
    async def test_switch_active_logic_failure(self, mock_comment_wrap, mock_switch_active_character, mock_get_character_by_name, mock_active_character, mock_get_db_connection):
        # Mocking the database connection
        mock_get_db_connection.return_value = (AsyncMock(), AsyncMock())
        
        # Mocking the active character retrieval to return None
        mock_active_character.return_value = None
        
        # Mocking the comment_wrap function
        mock_comment_wrap.return_value = "No characters found."
        
        character_data = {
            "characters_name": "new_character",
            "discord_tag": "example#1234",
            "guild_id": "1234567890"
        }
        
        result = await switch_active_logic(character_data)
        
        # Assertion
        self.assertEqual(result, "No characters found.")
 
    @patch('utils.impl.charactersimpl.available_characters', new_callable=AsyncMock)
    async def test_all_available_logic_success(self, mock_available_characters):
        # Mocking the available_characters function to return a list of characters
        mock_available_characters.return_value = [
            {'character': {'characters_name': 'character1'}},
            {'character': {'characters_name': 'character2'}}
        ]
        
        character_data = {
            "discord_tag": "example#1234",
            "guild_id": "1234567890"
        }
        
        result = await all_available_logic(character_data)
        
        # Assertion
        self.assertEqual(result, "Your characters are: \n\ncharacter1\ncharacter2")
    
    @patch('utils.impl.charactersimpl.available_characters', new_callable=AsyncMock)
    async def test_all_available_logic_no_characters(self, mock_available_characters):
        # Mocking the available_characters function to return an empty list
        mock_available_characters.return_value = []
        
        character_data = {
            "discord_tag": "example#1234",
            "guild_id": "1234567890"
        }
        
        result = await all_available_logic(character_data)
        
        # Assertion
        self.assertEqual(result, "No characters found.")
    
    @patch('utils.impl.charactersimpl.available_characters', new_callable=AsyncMock)
    async def test_all_available_logic_error(self, mock_available_characters):
        # Mocking the available_characters function to raise an exception
        mock_available_characters.side_effect = Exception("Database error")
        
        character_data = {
            "discord_tag": "example#1234",
            "guild_id": "1234567890"
        }
        
        result = await all_available_logic(character_data)
        
        # Assertion
        self.assertEqual(result, "An error occurred while attempting to display the characters.")

if __name__ == "__main__":
    unittest.main()