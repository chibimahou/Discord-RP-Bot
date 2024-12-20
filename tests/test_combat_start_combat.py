import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import unittest
import logging
from unittest.mock import patch, AsyncMock, MagicMock
from utils.impl.combatImpl import start_combat_logic


class TestStartCombatLogic(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        logging.basicConfig(level=logging.DEBUG)
        self.mock_get_db_connection = patch('utils.functions.database_functions.get_db_connection', AsyncMock(return_value=(AsyncMock(), AsyncMock()))).start()
        self.mock_active_character = patch('utils.functions.character_functions.active_character', AsyncMock()).start()
        self.mock_get_character_by_name = patch('utils.functions.character_functions.get_character_by_name', AsyncMock()).start()
        self.mock_get_party = patch('utils.functions.group_functions.get_party', AsyncMock()).start()
        # self.mock_get_mob_by_name = patch('utils.functions.mob_functions.get_mob_by_name', AsyncMock()).start()
        self.mock_get_initiative_order = patch('utils.functions.combat_functions.get_initiative_order', AsyncMock()).start()
        self.mock_create_combat_document = patch('utils.functions.combat_functions.create_combat_document', AsyncMock()).start()
        self.mock_create_combat_instance = patch('utils.functions.combat_functions.create_combat_instance', AsyncMock()).start()
        self.addCleanup(patch.stopall)

    async def test_start_combat_logic_success(self):
        self.mock_get_db_connection.return_value = (AsyncMock(), AsyncMock())
        self.mock_active_character.return_value = AsyncMock()
        self.mock_get_character_by_name.return_value = AsyncMock()
        self.mock_get_party.return_value = AsyncMock()
        #self.mock_get_mob_by_name.return_value = AsyncMock()
        self.mock_get_initiative_order.return_value = AsyncMock()
        self.mock_create_combat_document.return_value = AsyncMock()
        self.mock_create_combat_instance.return_value = AsyncMock()

        character_data = {"action": "attack",
                          "discord_tag": 1000000000,
                          "guild_id": 1234567890}
        target_data = {"characters_name": "test_character_01",
                       "guild_id": 1234567890,
                       "type": "character"}
        result = await start_combat_logic(character_data, target_data)
        self.assertEqual(result, "```Combat has started.```")

    async def test_start_combat_logic_failed_only_character(self):
        self.mock_get_db_connection.return_value = (AsyncMock(), AsyncMock())
        self.mock_active_character.return_value = AsyncMock()
        self.mock_get_character_by_name.return_value = AsyncMock()
        self.mock_get_party.return_value = AsyncMock()
        #self.mock_get_mob_by_name.return_value = AsyncMock()
        self.mock_get_initiative_order.return_value = AsyncMock()
        self.mock_create_combat_document.return_value = AsyncMock()
        self.mock_create_combat_instance.return_value = AsyncMock()

        character_data = {"action": "attack",
                          "discord_tag": 1000000000,
                          "guild_id": 1234567890}
        result = await start_combat_logic(character_data)
        self.assertEqual(result, "```No opponent found. Please make sure you have designated an opponent.```")
        
    async def test_start_combat_logic_character_not_found(self):
        self.mock_get_db_connection.return_value = (AsyncMock(), AsyncMock())
        self.mock_active_character.return_value = None

        character_data = {"action": "attack",
                          "discord_tag": 1999999999,
                          "guild_id": 1234567890}        
        result = await start_combat_logic(character_data)
        self.assertEqual(result, "```Character not found.```")

    async def test_start_combat_logic_target_not_found(self):
        self.mock_get_db_connection.return_value = (AsyncMock(), AsyncMock())
        self.mock_active_character.return_value = AsyncMock()
        self.mock_get_character_by_name.return_value = None

        character_data = {"action": "attack",
                          "discord_tag": 1000000000,
                          "guild_id": 1234567890}
        target_data = {"characters_name": "unknown_character",
                       "guild_id": 1234567890,
                       "type": "character"}
        result = await start_combat_logic(character_data, target_data)
        self.assertEqual(result, "```Target not found.```")

    async def test_start_combat_logic_mob_not_found(self):
        self.mock_get_db_connection.return_value = (AsyncMock(), AsyncMock())
        self.mock_active_character.return_value = AsyncMock()
        # self.mock_get_mob_by_name.return_value = None

        character_data = {"action": "attack",
                          "discord_tag": 1000000000,
                          "guild_id": 1234567890}        
        mob_data = {"mob_name": "test_mob"}
        result = await start_combat_logic(character_data, None, mob_data)
        self.assertEqual(result, "```Mob not found.```")