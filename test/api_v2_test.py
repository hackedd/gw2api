import unittest

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
