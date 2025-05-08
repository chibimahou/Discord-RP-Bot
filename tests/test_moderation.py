import unittest
import logging
from unittest.mock import patch, AsyncMock, MagicMock
from utils.impl.modImpl import (create_item_logic, 
                                delete_item_logic)


class TestCreateItemLogic(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        # Setup logging for debugging
        logging.basicConfig(level=logging.DEBUG)

        # Mock dependencies
        self.mock_get_db_connection = patch(
            'utils.functions.database_functions.get_db_connection',
            AsyncMock(return_value=(AsyncMock(), AsyncMock()))
        ).start()
        self.mock_check_if_item_exists = patch(
            'utils.functions.mod_functions.check_if_item_exists',
            AsyncMock()
        ).start()
        self.mock_create_item_data = patch(
            'utils.functions.mod_functions.create_item_data',
            AsyncMock()
        ).start()
        self.mock_add_item_to_db = patch(
            'utils.functions.mod_functions.add_item_to_db',
            AsyncMock()
        ).start()
        self.addCleanup(patch.stopall)

    async def test_create_item_logic_success(self):
        # Mock return values for a successful item creation
        self.mock_check_if_item_exists.return_value = False  # Item does not exist
        self.mock_create_item_data.return_value = {"mock": "item_data"}  # Mock item data
        self.mock_add_item_to_db.return_value = None  # Simulate successful DB insertion

        # Test data
        item_data = {
            "discord_tag": 1234567890,
            "guild_id": 987654321,
            "item_name": "Excalibur",
            "item_type": "Weapon",
            "item_value": 100,
            "item_description": "A legendary sword.",
            "item_rarity": "Legendary",
            "item_location": "Avalon",
            "item_material": "Mythril",
            "item_weight": 10,
            "item_effect": "Attack Boost",
            "item_effect_value": 50,
            "item_effect_duration": 300
        }
        # Call the function
        result = await create_item_logic(item_data)

        # Assertions
        self.assertEqual(result, "```Item created successfully.```")

    async def test_create_item_logic_item_exists(self):
        # Mock return value for an existing item
        self.mock_check_if_item_exists.return_value = True  # Item already exists

        # Test data
        item_data = {
            "discord_tag": 1234567890,
            "guild_id": 987654321,
            "item_name": "Excalibur"
        }

        # Call the function
        result = await create_item_logic(item_data)

        # Assertions
        self.assertEqual(result, '```Item already exists.```')


    async def test_delete_item_logic_success(self):
        # Mock return values for a successful item creation
        self.mock_check_if_item_exists.return_value = False  # Item does not exist
        self.mock_create_item_data.return_value = {"mock": "item_data"}  # Mock item data
        self.mock_add_item_to_db.return_value = None  # Simulate successful DB insertion

        # Test data
        item_data = {
            "item_name": "Excalibur",
            "guild_id": 987654321,
            "discord_tag": 1234567890
        }
        
        # Call the function
        result = await delete_item_logic(item_data)

        # Assertions
        self.assertEqual(result, "```Item deleted successfully.```")

    async def test_delete_item_logic_failure_not_found(self):
        # Mock return values for a successful item creation
        self.mock_check_if_item_exists.return_value = False  # Item does not exist
        self.mock_create_item_data.return_value = {"mock": "item_data"}  # Mock item data
        self.mock_add_item_to_db.return_value = None  # Simulate successful DB insertion

        # Test data
        item_data = {
            "item_name": "404 not found",
            "guild_id": 987654321,
            "discord_tag": 1234567890
        }
        
        # Call the function
        result = await delete_item_logic(item_data)

        # Assertions
        self.assertEqual(result, "```Item not found.```")

    async def test_delete_item_logic_failure_missing_data(self):
        # Mock return values for a successful item creation
        self.mock_check_if_item_exists.return_value = False  # Item does not exist
        self.mock_create_item_data.return_value = {"mock": "item_data"}  # Mock item data
        self.mock_add_item_to_db.return_value = None  # Simulate successful DB insertion

        # Test data
        item_data = {
            "item_name": "404 not found",
            "discord_tag": 1234567890
        }
        
        # Call the function
        result = await delete_item_logic(item_data)

        # Assertions
        self.assertEqual(result, "```An unexpected error occurred: 'guild_id'```")

if __name__ == "__main__":
    unittest.main()