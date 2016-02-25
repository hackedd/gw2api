import requests

import gw2api
import gw2api.v2

from auth_test import AuthenticatedTestBase


class TestGuildAuthenticated(AuthenticatedTestBase):
    guild_id = None

    @classmethod
    def setUpClass(cls):
        super(TestGuildAuthenticated, cls).setUpClass()

        if not cls.api_key:
            return

        gw2api.v2.account.set_token(cls.api_key)
        gw2api.v2.guild.set_token(cls.api_key)

        # Try to find a guild that we can access with the API key we have.
        account = gw2api.v2.account.get()
        for guild_id in account["guilds"]:
            try:
                gw2api.v2.guild.get_members(guild_id)
                cls.guild_id = guild_id
                break
            except requests.RequestException:
                pass

    def setUp(self):
        super(TestGuildAuthenticated, self).setUp()

        if not self.guild_id:
            self.skipTest("No usable guild found")

    def test_guild_ranks(self):
        ranks = gw2api.v2.guild.get_ranks(self.guild_id)
        self.assertIsInstance(ranks, list)
        rank_names = [rank["id"] for rank in ranks]
        self.assertIn("Leader", rank_names)

    def test_guild_members(self):
        members = gw2api.v2.guild.get_members(self.guild_id)
        self.assertIsInstance(members, list)

    def test_guild_treasury(self):
        treasury = gw2api.v2.guild.get_treasury(self.guild_id)
        self.assertIsInstance(treasury, list)

    def test_guild_upgrades(self):
        upgrades = gw2api.v2.guild.get_upgrades(self.guild_id)
        self.assertIsInstance(upgrades, list)
        for upgrade_id in upgrades:
            self.assertIsInstance(upgrade_id, int)

    def test_guild_stash(self):
        stash = gw2api.v2.guild.get_stash(self.guild_id)
        self.assertIsInstance(stash, list)

        for first_tab in stash:
            self.assertIsInstance(first_tab, dict)
            self.assertIn("upgrade_id", first_tab)
            self.assertIn("size", first_tab)
            self.assertIn("coins", first_tab)
            self.assertIn("inventory", first_tab)

    def test_guild_log(self):
        log = gw2api.v2.guild.get_log(self.guild_id)
        self.assertIsInstance(log, list)
        for entry in log[:5]:
            self.assertIsInstance(entry, dict)
            self.assertIn("id", entry)
            self.assertIn("type", entry)

    def test_guild_teams(self):
        teams = gw2api.v2.guild.get_teams(self.guild_id)
        self.assertIsInstance(teams, list)
        for entry in teams[:5]:
            self.assertIsInstance(entry, dict)
            self.assertIn("id", entry)
            self.assertIn("members", entry)
            self.assertIn("name", entry)
