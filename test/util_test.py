import unittest
import os
import tempfile

import gw2api
import gw2api.util
import gw2api.v2.util

from mock_requests import MockSession
import requests


class TestUtil(unittest.TestCase):
    def test_encode_chat_link(self):
        self.assertEqual(gw2api.encode_coin_link(0), "[&AQAAAAA=]")
        self.assertEqual(gw2api.encode_coin_link(1), "[&AQEAAAA=]")
        self.assertEqual(gw2api.encode_coin_link(3, 2, 1), "[&AdsnAAA=]")

        self.assertEqual(gw2api.encode_coin_link(3, 2, 1),
                         gw2api.encode_chat_link("coin", amount=10203))

        self.assertEqual(gw2api.encode_coin_link(1, 2),
                         gw2api.encode_chat_link("coin", copper=1, silver=2))

        # Copper Harvesting Sickle
        self.assertEqual(gw2api.encode_item_link(23029), "[&AgH1WQAA]")

        # Copper Logging Axe
        self.assertEqual(gw2api.encode_item_link(23030), "[&AgH2WQAA]")

        # Copper Mining Pick
        self.assertEqual(gw2api.encode_item_link(23031), "[&AgH3WQAA]")

        # Basic Salvage Kit
        self.assertEqual(gw2api.encode_item_link(23040), "[&AgEAWgAA]")

        # Zojja's Claymore (Dreamthistle Greatsword Skin) with
        # Superior Sigil of Bloodlust and Superior Sigil of Force
        link = gw2api.encode_item_link(46762, skin_id=3709,
                                       upgrade1=24575, upgrade2=24615)
        self.assertEqual(link, "[&AgGqtgDgfQ4AAP9fAAAnYAAA]")

        self.assertEqual(gw2api.encode_item_link(1234),
                         gw2api.encode_chat_link(gw2api.TYPE_ITEM, id=1234))
        self.assertEqual(gw2api.encode_item_link(1234),
                         gw2api.encode_chat_link("item", id=1234))

        # All norn will fall before us in time. Your time is now!
        self.assertEqual(gw2api.encode_chat_link("text", id=800),
                         "[&AyADAAA=]")

        # I will not soil my hands with you, insect. You are no match for me.
        self.assertEqual(gw2api.encode_chat_link("text", id=900),
                         "[&A4QDAAA=]")

        # Help me, norn. I'll do anything, if you just keep those things away.
        self.assertEqual(gw2api.encode_chat_link("text", id=999),
                         "[&A+cDAAA=]")

        # Point of Interest: Dr. Bleent's Encampment (Id: 56)
        self.assertEqual(gw2api.encode_chat_link("map", id=56),
                         "[&BDgAAAA=]")

        # Desider Atum Waypoint (Id: 72)
        self.assertEqual(gw2api.encode_chat_link("map", id=72),
                         "[&BEgAAAA=]")

        # Caudecus' Estate Waypoint (Id: 825)
        self.assertEqual(gw2api.encode_chat_link("map", id=825),
                         "[&BDkDAAA=]")

        # Skill: Blood Curse (Id: 10698)
        self.assertEqual(gw2api.encode_chat_link("skill", id=10698),
                         "[&BsopAAA=]")

        # Skill: Dusk Strike (Id: 29705)
        self.assertEqual(gw2api.encode_chat_link("skill", id=29705),
                         "[&Bgl0AAA=]")

        # Trait: Furious Demise (Id: 803)
        self.assertEqual(gw2api.encode_chat_link("trait", id=803),
                         "[&ByMDAAA=]")

        # Recipe: Soft Wood Plank (Id: 1)
        self.assertEqual(gw2api.encode_chat_link("recipe", id=1),
                         "[&CQEAAAA=]")

        # Recipe: Ancient Wood Planks (Id: 2)
        self.assertEqual(gw2api.encode_chat_link("recipe", id=2),
                         "[&CQIAAAA=]")

        # Recipe: Bolts of Cotton (Id: 7)")
        self.assertEqual(gw2api.encode_chat_link("recipe", id=7),
                         "[&CQcAAAA=]")

        # Skin: Chainmail Leggings (Id: 1)
        self.assertEqual(gw2api.encode_chat_link("skin", id=1),
                         "[&CgEAAAA=]")

        # Skin: Chainmail Chestpiece (Id: 2)
        self.assertEqual(gw2api.encode_chat_link("skin", id=2),
                         "[&CgIAAAA=]")

        # Cook's Outfit
        self.assertEqual(gw2api.encode_chat_link("outfit", id=1),
                         "[&CwEAAAA=]")

        # Witch's Outfit
        self.assertEqual(gw2api.encode_chat_link("outfit", id=4),
                         "[&CwQAAAA=]")

        # Y'lan Academy
        objective = gw2api.encode_chat_link("objective",
                                            objective_id=102, map_id=1102)
        self.assertEqual(objective, "[&DGYAAABOBAAA]")

        # Temple of Lost Prayers
        objective = gw2api.encode_chat_link("objective",
                                            objective_id=62, map_id=96)
        self.assertEqual(objective, "[&DD4AAABgAAAA]")

        with self.assertRaises(Exception) as context:
            gw2api.encode_chat_link(0xff)
        self.assertEqual(str(context.exception), "Unknown link type 0xff")

        with self.assertRaises(Exception) as context:
            gw2api.encode_chat_link("invalid")
        self.assertEqual(str(context.exception), "Unknown link type 'invalid'")

    def test_decode_chat_link(self):
        self.assertEqual(gw2api.decode_chat_link("[&AQAAAAA=]"),
                         ("coin", {"amount": 0}))
        self.assertEqual(gw2api.decode_chat_link("[&AQEAAAA=]"),
                         ("coin", {"amount": 1}))
        self.assertEqual(gw2api.decode_chat_link("[&AdsnAAA=]"),
                         ("coin", {"amount": 10203}))
        self.assertEqual(gw2api.decode_chat_link("[&AckAAAA=]"),
                         ("coin", {"amount": 201}))
        self.assertEqual(gw2api.decode_chat_link("[&AgH1WQAA]"),
                         ("item", {"id": 23029, "number": 1}))
        self.assertEqual(gw2api.decode_chat_link("[&AgH2WQAA]"),
                         ("item", {"id": 23030, "number": 1}))
        self.assertEqual(gw2api.decode_chat_link("[&AgH3WQAA]"),
                         ("item", {"id": 23031, "number": 1}))
        self.assertEqual(gw2api.decode_chat_link("[&AgEAWgAA]"),
                         ("item", {"id": 23040, "number": 1}))

        decoded = gw2api.decode_chat_link("[&AgGqtgDgfQ4AAP9fAAAnYAAA]")
        self.assertEqual(decoded,
                         ("item", {"id": 46762, "skin_id": 3709, "number": 1,
                                   "upgrade1": 24575, "upgrade2": 24615}))

        self.assertEqual(gw2api.decode_chat_link("[&AgHSBAAA]"),
                         ("item", {"id": 1234, "number": 1}))
        self.assertEqual(gw2api.decode_chat_link("[&AyADAAA=]"),
                         ("text", {"id": 800}))
        self.assertEqual(gw2api.decode_chat_link("[&A4QDAAA=]"),
                         ("text", {"id": 900}))
        self.assertEqual(gw2api.decode_chat_link("[&A+cDAAA=]"),
                         ("text", {"id": 999}))
        self.assertEqual(gw2api.decode_chat_link("[&BDgAAAA=]"),
                         ("map", {"id": 56}))
        self.assertEqual(gw2api.decode_chat_link("[&BEgAAAA=]"),
                         ("map", {"id": 72}))
        self.assertEqual(gw2api.decode_chat_link("[&BDkDAAA=]"),
                         ("map", {"id": 825}))
        self.assertEqual(gw2api.decode_chat_link("[&B+cCAAA=]"),
                         ("trait", {"id": 743}))
        self.assertEqual(gw2api.decode_chat_link("[&B3MVAAA=]"),
                         ("trait", {"id": 5491}))
        self.assertEqual(gw2api.decode_chat_link("[&B30VAAA=]"),
                         ("trait", {"id": 5501}))
        self.assertEqual(gw2api.decode_chat_link("[&CQEAAAA=]"),
                         ("recipe", {"id": 1}))
        self.assertEqual(gw2api.decode_chat_link("[&CQIAAAA=]"),
                         ("recipe", {"id": 2}))
        self.assertEqual(gw2api.decode_chat_link("[&CQcAAAA=]"),
                         ("recipe", {"id": 7}))
        self.assertEqual(gw2api.decode_chat_link("[&CgEAAAA=]"),
                         ("skin", {"id": 1}))
        self.assertEqual(gw2api.decode_chat_link("[&CgIAAAA=]"),
                         ("skin", {"id": 2}))
        self.assertEqual(gw2api.decode_chat_link("[&CgcAAAA=]"),
                         ("skin", {"id": 7}))
        self.assertEqual(gw2api.decode_chat_link("[&CwQAAAA=]"),
                         ("outfit", {"id": 4}))

        self.assertEqual(gw2api.decode_chat_link("[&DGYAAABOBAAA]"),
                         ("objective", {"objective_id": 102, "map_id": 1102}))
        self.assertEqual(gw2api.decode_chat_link("[&DD4AAABgAAAA]"),
                         ("objective", {"objective_id": 62, "map_id": 96}))

    def test_cache(self):
        class CacheMockSession(MockSession):
            def __init__(self):
                super(CacheMockSession, self).__init__()
                self.get_called = 0

            def get(self, url, **kwargs):
                self.get_called += 1
                return super(CacheMockSession, self).get(url, **kwargs)

        session = CacheMockSession()
        session.add_mock_response("get", gw2api.BASE_URL + "test.json",
                                  "{\"foo\": \"bar\"}")

        cache_dir = tempfile.mkdtemp()
        cache_file = os.path.join(cache_dir, "test.json")

        try:
            gw2api.set_cache_dir(cache_dir)
            gw2api.set_cache_time(3600)
            gw2api.set_session(session)

            self.assertFalse(os.path.exists(cache_file),
                             "cache file exists before request")

            # Call the webservice, test if the cache file is created.
            response = gw2api.util.get_cached("test.json")
            self.assertEqual(response, {"foo": "bar"}, "invalid response")
            self.assertEqual(session.get_called, 1, "invalid request count")
            self.assertTrue(os.path.exists(cache_file),
                            "cache file does not exist")

            # Call the webservice again, test that the cache is used instead.
            response = gw2api.util.get_cached("test.json")
            self.assertEqual(response, {"foo": "bar"}, "invalid response")
            self.assertEqual(session.get_called, 1, "invalid request count")

            # Temporarily disable, test that the service is called.
            response = gw2api.util.get_cached("test.json", False)
            self.assertEqual(response, {"foo": "bar"}, "invalid response")
            self.assertEqual(session.get_called, 2, "invalid request count")

        finally:
            if os.path.exists(cache_file):
                os.unlink(cache_file)
            os.rmdir(cache_dir)

            gw2api.set_cache_dir(None)

    def test_set_cache_dir(self):
        temp_dir = tempfile.mkdtemp()
        cache_dir = os.path.join(temp_dir, "test")
        temp_file = os.path.join(temp_dir, "file")

        try:
            self.assertFalse(os.path.exists(cache_dir))
            gw2api.set_cache_dir(cache_dir)
            self.assertTrue(os.path.exists(cache_dir))

            with open(temp_file, "w"):
                pass

            with self.assertRaises(ValueError) as context:
                gw2api.set_cache_dir(temp_file)
            self.assertEqual(str(context.exception), "not a directory")

        finally:
            if os.path.exists(cache_dir):
                os.rmdir(cache_dir)
            if os.path.exists(temp_file):
                os.unlink(temp_file)

            os.rmdir(temp_dir)

            gw2api.set_cache_dir(None)

    def test_error_extraction(self):
        gw2api.set_session(requests.Session())

        with self.assertRaises(requests.HTTPError) as context:
            gw2api.util.get_cached("unknown")
        self.assertIn("404 Client Error", str(context.exception))

        with self.assertRaises(requests.HTTPError) as context:
            gw2api.util.get_cached("map_floor.json")
        self.assertIn("missing continent_id or floor", str(context.exception))

    def test_list_wrapper(self):
        pages = [[1, 2], [3, 4], [5, 6]]

        class Endpoint(object):
            def page(self, page, *args):
                data = pages[page]
                return gw2api.v2.util.ListWrapper(self, page, data, args)

        endpoint = Endpoint()
        p0 = endpoint.page(0)
        self.assertEqual(p0, [1, 2])

        p1 = p0.next_page()
        self.assertEqual(p1, [3, 4])

        self.assertEqual(p0, p1.previous_page())
