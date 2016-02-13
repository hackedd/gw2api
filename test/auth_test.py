import os
import unittest
import requests

import gw2api
import gw2api.v2


class AuthenticatedTestBase(unittest.TestCase):
    token_filename = "api-key.txt"
    api_key = None

    @classmethod
    def setUpClass(cls):
        if os.path.exists(cls.token_filename):
            with open(cls.token_filename, "r") as fp:
                cls.api_key = fp.read().strip()

    def setUp(self):
        if not self.api_key:
            self.skipTest("No authorization token found")


class TestAuthenticated(AuthenticatedTestBase):
    def test_account_no_auth(self):
        gw2api.v2.account.set_token(None)
        with self.assertRaises(Exception) as context:
            gw2api.v2.account.get()
        self.assertIn("endpoint requires authentication",
                      str(context.exception))

    def test_account(self):
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

        dyes = gw2api.v2.account.get_dyes()
        self.assertIsInstance(dyes, list)

        skins = gw2api.v2.account.get_skins()
        self.assertIsInstance(skins, list)

        wallet = gw2api.v2.account.get_wallet()
        self.assertIsInstance(wallet, list)

        minis = gw2api.v2.account.get_minis()
        self.assertIsInstance(minis, list)

        achievements = gw2api.v2.account.get_achievements()
        self.assertIsInstance(achievements, list)

        inventory = gw2api.v2.account.get_inventory()
        self.assertIsInstance(inventory, list)

    def test_token_info(self):
        response = gw2api.v2.token_info.get(self.api_key)
        self.assertTrue(self.api_key.startswith(response["id"]))
        self.assertIn("name", response)
        self.assertIn("permissions", response)

    def test_transactions(self):
        gw2api.v2.transactions.set_token(self.api_key)

        gw2api.v2.transactions.current_buys()
        gw2api.v2.transactions.current_sells()
        gw2api.v2.transactions.history_buys()
        gw2api.v2.transactions.history_sells()

    def test_characters(self):
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

        spec = gw2api.v2.characters.get_specializations(character_name)
        self.assertIsInstance(spec, dict)
        self.assertEqual(sorted(spec.keys()), ["pve", "pvp", "wvw"])

        recipes = gw2api.v2.characters.get_recipes(character_name)
        self.assertIsInstance(recipes, list)

    def test_pvp(self):
        gw2api.v2.pvp_stats.set_token(self.api_key)

        pvp_stats = gw2api.v2.pvp_stats.get()
        self.assertIsInstance(pvp_stats, dict)
        self.assertIn("pvp_rank", pvp_stats)

        gw2api.v2.pvp_games.set_token(self.api_key)

        games = gw2api.v2.pvp_games.get_ids()
        self.assertIsInstance(games, list)

        game = gw2api.v2.pvp_games.get(games[0])
        self.assertIsInstance(game, dict)

    def test_pvp_game_workaround(self):
        # https://api.guildwars2.com/v2/pvp/games/xyz is 404, but
        # https://api.guildwars2.com/v2/pvp/games?id=xyz works
        endpoint = gw2api.v2.AuthenticatedEndpoint("pvp/games")
        endpoint.set_token(self.api_key)
        games = endpoint.get_ids()
        with self.assertRaises(requests.HTTPError) as context:
            endpoint.get_one(games[0])
        self.assertEqual(context.exception.response.status_code, 404)
