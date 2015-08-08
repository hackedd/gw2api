import unittest
import warnings
from datetime import datetime

import gw2api


class TestApi(unittest.TestCase):
    def setUp(self):
        super(TestApi, self).setUp()

    def test_map(self):
        map_names = gw2api.continents()
        self.assertIsInstance(map_names, dict)
        keys = ["continent_dims", "floors", "max_zoom", "min_zoom", "name"]
        for continent_id, continent in map_names.iteritems():
            self.assertEqual(sorted(continent.keys()), keys)

        map_names = gw2api.map_names()
        self.assertIsInstance(map_names, dict)
        key, value = map_names.items()[0]
        self.assertIsInstance(key, basestring)
        self.assertIsInstance(value, basestring)

        maps = gw2api.maps()
        self.assertIsInstance(maps, dict)
        key, value = maps.items()[0]
        self.assertIsInstance(key, basestring)
        self.assertIsInstance(value, dict)

        map_data = gw2api.maps(map_id=50)
        self.assertIsInstance(map_data, dict)
        self.assertEqual(map_data["map_name"], "Lion's Arch")

        # Floor 34 in Tyria contains Sanctum Sprint
        map_floor_data = gw2api.map_floor(1, 34)
        self.assertEqual(sorted(map_floor_data.keys()),
                         ["clamped_view", "regions", "texture_dims"])

    def test_misc(self):
        build = gw2api.build()
        self.assertIsInstance(build, int)

        colors = gw2api.colors()
        self.assertIsInstance(colors, dict)
        key, value = colors.items()[0]
        self.assertIsInstance(key, basestring)
        self.assertIsInstance(value, dict)
        self.assertEqual(sorted(value.keys()),
                         ["base_rgb", "cloth", "leather", "metal", "name"])
        self.assertEqual(sorted(value["cloth"].keys()),
                         ["brightness", "contrast", "hue", "lightness", "rgb",
                          "saturation"])

        files = gw2api.files()
        self.assertIsInstance(files, dict)
        key, value = files.items()[0]
        self.assertIsInstance(key, basestring)
        self.assertIsInstance(value, dict)
        self.assertEqual(sorted(value.keys()), ["file_id", "signature"])

    def test_skins(self):
        skins = gw2api.skins()
        self.assertIsInstance(skins, list)
        self.assertIsInstance(skins[0], int)

        skin_details = gw2api.skin_details(skins[0])
        self.assertIsInstance(skin_details, dict)
        self.assertEqual(int(skin_details["skin_id"]), skins[0])
        self.assertIn("name", skin_details)

    def test_items(self):
        items = gw2api.items()
        self.assertIsInstance(items, list)
        self.assertIsInstance(items[0], int)

        item_details = gw2api.item_details(items[0])
        self.assertIsInstance(item_details, dict)
        self.assertEqual(int(item_details["item_id"]), items[0])
        self.assertIn("name", item_details)

    def test_recipes(self):
        recipes = gw2api.recipes()
        self.assertIsInstance(recipes, list)
        self.assertIsInstance(recipes[0], int)

        recipe_details = gw2api.recipe_details(recipes[0])
        self.assertIsInstance(recipe_details, dict)
        self.assertEqual(int(recipe_details["recipe_id"]), recipes[0])
        self.assertIn("ingredients", recipe_details)

    def test_events(self):
        event_names = gw2api.event_names()
        self.assertIsInstance(event_names, dict)

        event_id = "5161DE97-FAB6-4916-8788-65E9F4FAF333"
        event_name = "Recover the stolen LUM0009 golems from the Inquest."

        event_details = gw2api.event_details()
        self.assertIsInstance(event_details, dict)
        self.assertIn(event_id, event_details)

        event_details = gw2api.event_details(event_id)
        self.assertIsInstance(event_details, dict)
        self.assertIn("name", event_details)
        self.assertEqual(event_details["name"], event_name)

    def test_guild(self):
        keys = ["emblem", "guild_id", "guild_name", "tag"]

        guild_details = gw2api.guild_details(name="Half Digested Mass Effect")
        self.assertEqual(sorted(guild_details.keys()), keys)

        guild_id = "93ED2714-9E30-4E78-AC39-AE79FD603F03"
        guild_details = gw2api.guild_details(guild_id)
        self.assertEqual(sorted(guild_details.keys()), keys)

        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")

            gw2api.guild_details(guild_id, "Half Digested Mass Effect")

            self.assertEqual(len(w), 1)
            self.assertIn("both guild_id and name are specified",
                          str(w[0].message))

        with self.assertRaises(Exception) as context:
            gw2api.guild_details()
        self.assertEquals(str(context.exception),
                          "specify either guild_id or name")

    def test_wvw(self):
        keys = ["blue_world_id", "end_time", "green_world_id", "red_world_id",
                "start_time", "wvw_match_id"]

        matches = gw2api.matches()
        self.assertEqual(sorted(matches[0].keys()), keys)
        self.assertIsInstance(matches[0]["start_time"], datetime)
        self.assertIsInstance(matches[0]["end_time"], datetime)

        match_details = gw2api.match_details(matches[0]["wvw_match_id"])
        self.assertEqual(sorted(match_details.keys()),
                         ["maps", "match_id", "scores"])

        objectives = gw2api.objective_names()
        self.assertIsInstance(objectives, dict)
