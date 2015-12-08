import unittest
import requests

import gw2api.v2


class TestApi2(unittest.TestCase):
    def test_getting_quaggan_ids(self):
        ids = gw2api.v2.quaggans.get_ids()
        self.assertIsInstance(ids, list)
        self.assertIn("breakfast", ids)
        self.assertIn("bubble", ids)
        self.assertIn("cake", ids)

    def test_getting_guaggans(self):
        breakfast = gw2api.v2.quaggans.get_one("breakfast")
        self.assertEqual("breakfast", breakfast["id"])

        bubble = gw2api.v2.quaggans.get_one("bubble")
        self.assertEqual("bubble", bubble["id"])

        # calling `get` with one id should call get_one
        cake = gw2api.v2.quaggans.get("cake")
        self.assertEqual("cake", cake["id"])

        quaggans = gw2api.v2.quaggans.get("breakfast", "bubble", "cake")
        self.assertEqual(len(quaggans), 3)
        self.assertIn(breakfast, quaggans)
        self.assertIn(bubble, quaggans)
        self.assertIn(cake, quaggans)

        quaggans2 = gw2api.v2.quaggans.get(["breakfast", "bubble", "cake"])
        self.assertEqual(quaggans, quaggans2)

    def test_getting_paginated_guaggans(self):
        page = gw2api.v2.quaggans.page(page_size=5)
        self.assertEqual(len(page), 5)

        ids = gw2api.v2.quaggans.get_ids()
        self.assertEqual([q["id"] for q in page], ids[0:5])

        page2 = gw2api.v2.quaggans.page(1, page_size=5)
        self.assertEqual([q["id"] for q in page2], ids[5:10])

    def test_getting_all_guaggans(self):
        ids = gw2api.v2.quaggans.get_ids()
        quaggans = gw2api.v2.quaggans.get_all()
        self.assertEqual(len(ids), len(quaggans))

    def test_quaggan_metadata(self):
        page = gw2api.v2.quaggans.page(page_size=5)
        self.assertEqual(len(page), 5)

        self.assertEqual(page.meta["self"], "/v2/quaggans?page=0&page_size=5")
        self.assertEqual(page.meta["next"], "/v2/quaggans?page=1&page_size=5")
        self.assertEqual(page.meta["first"], "/v2/quaggans?page=0&page_size=5")
        self.assertEqual(page.meta["last"], "/v2/quaggans?page=6&page_size=5")

        self.assertEqual(page.meta["page_size"], 5)
        self.assertEqual(page.meta["page_total"], 7)
        self.assertEqual(page.meta["result_total"], 35)
        self.assertEqual(page.meta["result_count"], 5)

    def test_getting_color_ids(self):
        color_ids = gw2api.v2.colors.get_ids()
        self.assertIsInstance(color_ids, list)
        self.assertIn(1, color_ids)

    def test_getting_colors(self):
        dye_remover = gw2api.v2.colors.get_one(1)
        self.assertEqual("Dye Remover", dye_remover["name"])

        black = gw2api.v2.colors.get(2)
        self.assertEqual("Black", black["name"])

        dye_remover_fr = gw2api.v2.colors.get(1, lang="fr")
        self.assertEqual("Dissolvant pour teinture", dye_remover_fr["name"])

        colors = gw2api.v2.colors.get(1, 2, 3)
        self.assertEqual(["Dye Remover", "Black", "Chalk"],
                         [c["name"] for c in colors])

        colors2 = gw2api.v2.colors.get([1, 2, 3])
        self.assertEqual(["Dye Remover", "Black", "Chalk"],
                         [c["name"] for c in colors2])

        colors_fr = gw2api.v2.colors.get(1, 2, 3, lang="fr")
        self.assertEqual(["Dissolvant pour teinture", "Noir", "Craie"],
                         [c["name"] for c in colors_fr])

    def test_getting_paginated_colors(self):
        page_en = gw2api.v2.colors.page(page_size=5)
        self.assertEqual(len(page_en), 5)

        page_fr = gw2api.v2.colors.page(page_size=5, lang="fr")
        self.assertEqual(len(page_fr), 5)

        ids = gw2api.v2.colors.get_ids()
        self.assertEqual([q["id"] for q in page_en], ids[0:5])
        self.assertEqual([q["id"] for q in page_fr], ids[0:5])

        page2_en = gw2api.v2.colors.page(1, page_size=5)
        self.assertEqual([q["id"] for q in page2_en], ids[5:10])

        page2_fr = gw2api.v2.colors.page(1, page_size=5, lang="fr")
        self.assertEqual([q["id"] for q in page2_fr], ids[5:10])

    def test_getting_all_colors(self):
        ids = gw2api.v2.colors.get_ids()
        colors_en = gw2api.v2.colors.get_all()
        self.assertEqual(len(ids), len(colors_en))
        colors_fr = gw2api.v2.colors.get_all(lang="fr")
        self.assertEqual(len(ids), len(colors_fr))

    def test_recipe_search(self):
        gold_ore_id = 19698
        gold_ingot_id = 19682

        recipe_ids = gw2api.v2.recipe_search.input(gold_ore_id)
        self.assertTrue(len(recipe_ids) >= 1)
        for recipe_id in recipe_ids:
            recipe = gw2api.v2.recipes.get(recipe_id)
            self.assertIn(gold_ore_id,
                          [i["item_id"] for i in recipe["ingredients"]])

        recipes = gw2api.v2.recipe_search.input(gold_ore_id, details=True)
        self.assertEqual(len(recipe_ids), len(recipes))
        for recipe in recipes:
            self.assertIn(gold_ore_id,
                          [i["item_id"] for i in recipe["ingredients"]])

        recipe_ids = gw2api.v2.recipe_search.output(gold_ingot_id)
        self.assertTrue(len(recipe_ids) >= 1)
        for recipe_id in recipe_ids:
            recipe = gw2api.v2.recipes.get(recipe_id)
            self.assertEqual(recipe["output_item_id"], gold_ingot_id)

        recipes = gw2api.v2.recipe_search.output(gold_ingot_id, details=True)
        self.assertEqual(len(recipe_ids), len(recipes))
        for recipe in recipes:
            self.assertEqual(recipe["output_item_id"], gold_ingot_id)

    def test_currencies(self):
        currencies = gw2api.v2.currencies.get_all()
        self.assertIsInstance(currencies, list)

        coin = gw2api.v2.currencies.get(1)
        self.assertIn(coin, currencies)
        self.assertEqual("Coin", coin["name"])

    def test_wvw(self):
        objective_ids = gw2api.v2.wvw_objectives.get_ids()
        self.assertIsInstance(objective_ids, list)

        objective = gw2api.v2.wvw_objectives.get(objective_ids[0])
        self.assertIn("name", objective)
        self.assertIn("type", objective)
        # self.assertIn("coord", objective)

        match_ids = gw2api.v2.wvw_matches.get_ids()
        self.assertIsInstance(match_ids, list)

        match = gw2api.v2.wvw_matches.get(match_ids[0])
        self.assertIn("id", match)
        self.assertIn("start_time", match)
        self.assertIn("end_time", match)

        match = gw2api.v2.wvw_matches.world(1007)
        self.assertIn("id", match)
        self.assertIn("start_time", match)
        self.assertIn("end_time", match)

    def test_achievements(self):
        achievement_ids = gw2api.v2.achievements.get_ids()
        self.assertIsInstance(achievement_ids, list)

        achievement = gw2api.v2.achievements.get(achievement_ids[0])
        self.assertIsInstance(achievement, dict)
        self.assertIn("name", achievement)
        self.assertIn("requirement", achievement)

        daily_achievements = gw2api.v2.achievements.get("daily")
        self.assertIsInstance(daily_achievements, dict)
        self.assertEqual(["pve", "pvp", "wvw"],
                         sorted(daily_achievements.keys()))

    def test_achievement_groups(self):
        story_group_id = "A4ED8379-5B6B-4ECC-B6E1-70C350C902D2"
        self.assertIn(story_group_id, gw2api.v2.achievement_groups.get_ids())
        story_group = gw2api.v2.achievement_groups.get(story_group_id)
        self.assertEqual("Story Journal", story_group["name"])

    def test_achievement_categories(self):
        self.assertIn(1, gw2api.v2.achievement_categories.get_ids())
        story_group = gw2api.v2.achievement_categories.get(1)
        self.assertEqual("Slayer", story_group["name"])

    def test_minis(self):
        mini = gw2api.v2.minis.get(1)
        self.assertEqual("Miniature Rytlock", mini["name"])
        self.assertEqual(21047, mini["item_id"])

    def test_emblems(self):
        foreground = gw2api.v2.emblem_foregrounds.get(71)
        self.assertIn("id", foreground)
        self.assertIn("layers", foreground)

        background = gw2api.v2.emblem_foregrounds.get(2)
        self.assertIn("id", background)
        self.assertIn("layers", background)

    def test_guild_upgrades(self):
        upgrade = gw2api.v2.guild_upgrades.get(38)
        self.assertEqual("Guild Armorer 1", upgrade["name"])
        self.assertIn("description", upgrade)
        self.assertIn("icon", upgrade)
        self.assertIn("costs", upgrade)
        self.assertIn("prerequisites", upgrade)
