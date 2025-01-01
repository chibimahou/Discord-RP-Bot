import unittest
from unittest.mock import patch, AsyncMock
from utils.impl.modImpl import create_mob_logic

class TestModLogic(unittest.IsolatedAsyncioTestCase):

    @patch('utils.functions.mod_functions.add_mob_to_db', new_callable=AsyncMock)
    async def test_create_mob_logic_success(self, mock_add_mob_to_db):
        mob_data = {
            "name": "goblin",
            "description": "A small, green creature with sharp teeth.",
            "average_level": 1,
            "exp_reward": 50,
            "equipment_head": "bronze helmet",
            "equipment_body": "bronze chestplate",
            "equipment_legs": "bronze leggings",
            "equipment_feet": "bronze boots",
            "equipment_hands": "bronze gauntlets",
            "equipment_main_hand": "bronze sword",
            "equipment_off_hand": "bronze shield",
            "equipment_accessory_1": "bronze ring",
            "equipment_accessory_2": "cloak",
            "hp": 5,
            "strength": 5,
            "dexterity": 5,
            "defense": 5,
            "speed": 5,
            "charisma": 5,
            "inserted_by": "test_user",
            "insertion_date": "2023-10-10",
            "guild_id": "1234567890"
        }

        result = await create_mob_logic(mob_data)
        
        # Assertion
        self.assertEqual(result, "```Character created successfully.```")

    @patch('utils.functions.mod_functions.add_mob_to_db', new_callable=AsyncMock)
    async def test_create_mob_logic_failure(self, mock_add_mob_to_db):
        # Mocking the add_mob_to_db function to raise an exception
        mock_add_mob_to_db.side_effect = Exception("Database error")

        mob_data = {
            "name": "goblin",
            "description": "A small, green creature with sharp teeth.",
            "average_level": 1,
            "exp_reward": 50,
            "equipment_head": "bronze helmet",
            "equipment_body": "bronze chestplate",
            "equipment_legs": "bronze leggings",
            "equipment_feet": "bronze boots",
            "equipment_hands": "bronze gauntlets",
            "equipment_main_hand": "bronze sword",
            "equipment_off_hand": "bronze shield",
            "equipment_accessory_1": "bronze ring",
            "equipment_accessory_2": "cloak",
            "hp": 5,
            "strength": 5,
            "dexterity": 5,
            "defense": 5,
            "speed": 5,
            "charisma": 5,
            "inserted_by": "test_user",
            "insertion_date": "2023-10-10",
            "guild_id": "1234567890"
        }

        result = await create_mob_logic(mob_data)
        
        # Assertion
        self.assertTrue(result, "```An unexpected error occurred: Database error```")

if __name__ == "__main__":
    unittest.main()