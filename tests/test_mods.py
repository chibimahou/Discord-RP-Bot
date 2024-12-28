import unittest
from unittest.mock import patch, AsyncMock
from utils.impl.inventoryimpl import add_logic, remove_logic, check_logic

class TestInventoryLogic(unittest.IsolatedAsyncioTestCase):

    @patch('utils.functions.inventory_functions.add_item_to_inventory', new_callable=AsyncMock)
    async def test_add_logic_success(self, mock_add_item_to_inventory):
        # Mocking the add_item_to_inventory function to return a success message
        mock_add_item_to_inventory.return_value = "Item added successfully."
        
        characters_data = {
            "discord_tag": 1234567891,
            "guild_id": 1234567890
        }
        
        item_data = {
            "name": "Sword",
            "quantity": 1,
            "guild_id": 1234567890
        }
        
        result = await add_logic(characters_data, item_data)
        
        # Assertion
        self.assertEqual(result, "Item added successfully.")
    
    @patch('utils.functions.inventory_functions.add_item_to_inventory', new_callable=AsyncMock)
    async def test_add_logic_failure_not_found(self, mock_add_item_to_inventory):
        # Mocking the add_item_to_inventory function to return a success message
        mock_add_item_to_inventory.return_value = "Item added successfully."
        
        characters_data = {
            "discord_tag": 1234567891,
            "guild_id": 1234567890
        }
        
        item_data = {
            "name": "not found",
            "quantity": 1,
            "guild_id": 1234567890
        }
        
        result = await add_logic(characters_data, item_data)
        
        # Assertion
        self.assertEqual(result, "Item not found.")
    
    @patch('utils.functions.inventory_functions.remove_item_from_inventory', new_callable=AsyncMock)
    async def test_remove_logic_success(self, mock_remove_item_from_inventory):
        # Mocking the remove_item_from_inventory function to return a success message
        mock_remove_item_from_inventory.return_value = "Item removed successfully."
        
        characters_data = {
            "characters_name": "Kirito",
            "discord_tag": 1234567891,
            "guild_id": 1234567890
        }
        
        item_data = {
            "item_name": "Sword",
            "quantity": 1
        }
        
        result = remove_logic(characters_data, item_data)
        
        # Assertion
        self.assertEqual(result, "Item removed successfully.")
    
    @patch('utils.functions.inventory_functions.check_inventory', new_callable=AsyncMock)
    async def test_check_logic_success(self, mock_check_inventory):
        # Mocking the check_inventory function to return a list of items
        mock_check_inventory.return_value = [
            {"item_name": "Sword", "quantity": 1},
            {"item_name": "Shield", "quantity": 1}
        ]
        
        characters_data = {
            "characters_name": "Kirito",
            "discord_tag": 1234567891,
            "guild_id": 1234567890
        }
        
        result = check_logic(characters_data)
        
        # Assertion
        self.assertEqual(result, [
            {"item_name": "Sword", "quantity": 1},
            {"item_name": "Shield", "quantity": 1}
        ])

if __name__ == "__main__":
    unittest.main()