import unittest
from unittest.mock import patch, AsyncMock
from utils.impl.modImpl import (create_mob_logic, create_buff_logic, delete_buff_logic)

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


    @patch('utils.functions.database_functions.get_db_connection', new_callable=AsyncMock)
    @patch('utils.functions.mod_functions.check_if_buff_exists', new_callable=AsyncMock)
    @patch('utils.functions.mod_functions.create_buff_data', new_callable=AsyncMock)
    @patch('utils.functions.mod_functions.add_buff_to_db', new_callable=AsyncMock)
    async def test_create_buff_logic_success(self, mock_add_buff_to_db, mock_create_buff_data, mock_check_if_buff_exists, mock_get_db_connection):
        # Mocking the database connection
        mock_get_db_connection.return_value = (AsyncMock(), AsyncMock())
        
        # Mocking the check_if_buff_exists function to return False (buff does not exist)
        mock_check_if_buff_exists.return_value = False
        
        # Mocking the add_buff_to_db function to return None (successful insertion)
        mock_add_buff_to_db.return_value = None
        
        buff_data = {
            "name": "strength_boost",
            "description": "Increases strength by 5.",
            "stat_1": "strength",
            "operation_1": "flat",
            "value_1": 5,
            "activates_1": "immediate",
            "stat_2": '',
            "operation_2": '',
            "value_2": 0,
            "activates_2": '',
            "debuff_stat_1": '',
            "debuff_operation_1": '',
            "debuff_value_1": 0,
            "debuff_activates_1": '',
            "debuff_stat_2": '',
            "debuff_operation_2": '',
            "debuff_value_2": 0,
            "debuff_activates_2": '',
            "guild_id": 1234567890,
            "inserted_by": "test_user",
            "insertion_date": "2023-10-10 12:00:00"
        }
        
        result = await create_buff_logic(buff_data)
        
        # Assertion
        self.assertEqual(result, "```Buff created successfully.```")

    @patch('utils.functions.database_functions.get_db_connection', new_callable=AsyncMock)
    @patch('utils.functions.mod_functions.check_if_buff_exists', new_callable=AsyncMock)
    @patch('utils.functions.mod_functions.create_buff_data', new_callable=AsyncMock)
    @patch('utils.functions.mod_functions.add_buff_to_db', new_callable=AsyncMock)
    async def test_create_buff_logic_failure(self, mock_add_buff_to_db, mock_create_buff_data, mock_check_if_buff_exists, mock_get_db_connection):
        # Mocking the database connection
        mock_get_db_connection.return_value = (AsyncMock(), AsyncMock())
        
        # Mocking the check_if_buff_exists function to raise an exception
        mock_check_if_buff_exists.side_effect = Exception("Database error")
        
        buff_data = {
            "name": "strength_boost",
            "description": "Increases strength by 5.",
            "stat_1": "strength",
            "operation_1": "flat",
            "value_1": 5,
            "activates_1": "immediate",
            "stat_2": '',
            "operation_2": '',
            "value_2": 0,
            "activates_2": '',
            "debuff_stat_1": '',
            "debuff_operation_1": '',
            "debuff_value_1": 0,
            "debuff_activates_1": '',
            "debuff_stat_2": '',
            "debuff_operation_2": '',
            "debuff_value_2": 0,
            "debuff_activates_2": '',
            "guild_id": 1234567890,
            "inserted_by": "test_user",
            "insertion_date": "2023-10-10 12:00:00"
        }
        
        result = await create_buff_logic(buff_data)
        
        # Assertion
        self.assertTrue(result, "```An unexpected error occurred: Database error```")

    @patch('utils.functions.database_functions.get_db_connection', new_callable=AsyncMock)
    @patch('utils.functions.mod_functions.check_if_buff_exists', new_callable=AsyncMock)
    @patch('utils.functions.mod_functions.delete_buff_from_db', new_callable=AsyncMock)
    @patch('utils.functions.mod_functions.add_buff_to_db', new_callable=AsyncMock)
    async def test_delete_buff_logic_success(self, mock_add_buff_to_db, mock_delete_buff_from_db, mock_check_if_buff_exists, mock_get_db_connection):
        # Mocking the database connection
        mock_get_db_connection.return_value = (AsyncMock(), AsyncMock())
        
        # Mocking the check_if_buff_exists function to return False (buff does not exist)
        mock_check_if_buff_exists.return_value = False
        
        # Mocking the add_buff_to_db function to return None (successful insertion)
        mock_add_buff_to_db.return_value = None
        
        buff_data = {
            "name": "strength_boost",
            "guild_id": 1234567890
        }
        
        result = await delete_buff_logic(buff_data)
        
        # Assertion
        self.assertEqual(result, "```Buff deleted successfully.```")

    @patch('utils.functions.database_functions.get_db_connection', new_callable=AsyncMock)
    @patch('utils.functions.mod_functions.check_if_buff_exists', new_callable=AsyncMock)
    @patch('utils.functions.mod_functions.delete_buff_from_db', new_callable=AsyncMock)
    @patch('utils.functions.mod_functions.add_buff_to_db', new_callable=AsyncMock)
    async def test_delete_buff_logic_failure(self, mock_add_buff_to_db, mock_delete_buff_from_db, mock_check_if_buff_exists, mock_get_db_connection):
        # Mocking the database connection
        mock_get_db_connection.return_value = (AsyncMock(), AsyncMock())
        
        # Mocking the check_if_buff_exists function to return False (buff does not exist)
        mock_check_if_buff_exists.return_value = False
        
        # Mocking the add_buff_to_db function to return None (successful insertion)
        mock_add_buff_to_db.return_value = None
        
        buff_data = {
            "name": "strength_boost",
            "guild_id": 1234567890
        }
        
        result = await delete_buff_logic(buff_data)
        
        # Assertion
        self.assertEqual(result, "```Buff does not exist.```")

if __name__ == "__main__":
    unittest.main()