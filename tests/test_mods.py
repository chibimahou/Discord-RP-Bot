import unittest
from unittest.mock import patch, AsyncMock

class TestModLogic(unittest.IsolatedAsyncioTestCase):
    
    @patch('utils.functions.inventory_functions.add_item_to_inventory', new_callable=AsyncMock)
    async def test_add_logic_success(self, mock_add_item_to_inventory):
        a = 5