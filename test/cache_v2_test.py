import unittest
import os
import tempfile
import json
import shutil

import gw2api
import gw2api.v2

from mock_requests import MockSession


class TestCache2(unittest.TestCase):
    def test_cache(self):
        class CacheMockSession(MockSession):
            def __init__(self):
                super(CacheMockSession, self).__init__()
                self.get_called = 0

            def get(self, url, **kwargs):
                self.get_called += 1
                return super(CacheMockSession, self).get(url, **kwargs)

        saved_session = gw2api.session

        quaggans = ["404", "aloha", "attack", "bear"]

        session = CacheMockSession()
        session.add_mock_response("get", gw2api.v2.BASE_URL + "quaggans",
                                  json.dumps(quaggans))

        for name in quaggans:
            url = gw2api.v2.BASE_URL + "quaggans/" + name
            response = {
                "id": name,
                "url": "https://static.staticwars.com/quaggans/%s.jpg" % name
            }
            session.add_mock_response("get", url, json.dumps(response))

        cache_dir = tempfile.mkdtemp()

        def exists(filename):
            return os.path.exists(os.path.join(cache_dir, filename))

        gw2api.set_cache_dir(None)
        self.assertFalse(gw2api.v2.quaggans.has_cached("quaggans.json"),
                         "endpoint reports cache exist")

        try:
            gw2api.set_cache_dir(cache_dir)
            gw2api.set_cache_time(3600)
            gw2api.set_session(session)

            self.assertFalse(exists("quaggans.json"),
                             "cache file exists before request")

            self.assertFalse(gw2api.v2.quaggans.has_cached("quaggans.json"),
                             "endpoint reports cache exist before request")

            # Call the webservice, test if the cache file is created.
            response = gw2api.v2.quaggans.get_ids()
            self.assertEqual(response, quaggans, "invalid response")
            self.assertEqual(session.get_called, 1, "invalid request count")
            self.assertTrue(exists("quaggans.json"),
                            "cache file does not exist")

            self.assertTrue(gw2api.v2.quaggans.has_cached("quaggans.json"),
                            "endpoint reports cache does not exist")

            # Call the webservice again, test that the cache is used instead.
            response = gw2api.v2.quaggans.get_ids()
            self.assertEqual(response, quaggans, "invalid response")
            self.assertEqual(session.get_called, 1, "invalid request count")

        finally:
            shutil.rmtree(cache_dir, ignore_errors=True)
            gw2api.set_cache_dir(None)
            gw2api.set_session(saved_session)
