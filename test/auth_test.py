import os
import json

import unittest

import gw2api
import gw2api.v2


class TestAuthenticated(unittest.TestCase):
    token_filename = "api-key.txt"

    def setUp(self):
        super(TestAuthenticated, self).setUp()

        if os.path.exists(self.token_filename):
            with open(self.token_filename, "r") as fp:
                self.api_key = fp.read().strip()
        else:
            self.api_key = None

    def test_account_no_auth(self):
        gw2api.v2.account.set_token(None)
        with self.assertRaises(Exception) as context:
            gw2api.v2.account.get()
        self.assertIn("endpoint requires authentication",
                      str(context.exception))

    def test_account(self):
        if not self.api_key:
            self.skipTest("No authorization token found")

        gw2api.v2.account.set_token(self.api_key)
        response = gw2api.v2.account.get()
        self.assertIsInstance(response, dict)
        self.assertIn("id", response)
        self.assertIn("name", response)
        self.assertIn("world", response)

        bank = gw2api.v2.account.get_bank()
        self.assertIsInstance(bank, list)

        materials = gw2api.v2.account.get_materials()
        self.assertIsInstance(materials, list)

    def test_token_info(self):
        if not self.api_key:
            self.skipTest("No authorization token found")

        response = gw2api.v2.token_info.get(self.api_key)
        self.assertTrue(self.api_key.startswith(response["id"]))
        self.assertIn("name", response)
        self.assertIn("permissions", response)

    def test_transactions(self):
        if not self.api_key:
            self.skipTest("No authorization token found")

        gw2api.v2.transactions.set_token(self.api_key)

        gw2api.v2.transactions.current_buys()
        gw2api.v2.transactions.current_sells()
        gw2api.v2.transactions.history_buys()
        gw2api.v2.transactions.history_sells()

    def test_characters(self):
        if not self.api_key:
            self.skipTest("No authorization token found")

        gw2api.v2.characters.set_token(self.api_key)

        character_names = gw2api.v2.characters.get_ids()
        self.assertIsInstance(character_names, list)
        self.assertIsInstance(character_names[0], basestring)

        character_name = character_names[0]

        character = gw2api.v2.characters.get(character_name)
        self.assertIsInstance(character, dict)
        self.assertEqual(character["name"], character_name)

        inventory = gw2api.v2.characters.get_inventory(character_name)
        self.assertIsInstance(inventory, list)

        equipment = gw2api.v2.characters.get_equipment(character_name)
        self.assertIsInstance(equipment, list)
