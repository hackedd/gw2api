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
        self.assertIn("endpoint requires authentication", str(context.exception))

    def test_account(self):
        if not self.api_key:
            self.skipTest("No authorization token found")

        gw2api.v2.account.set_token(self.api_key)
        response = gw2api.v2.account.get()
        self.assertIsInstance(response, dict)
        self.assertIn("id", response)
        self.assertIn("name", response)
        self.assertIn("world", response)
