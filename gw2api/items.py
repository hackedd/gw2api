from .util import get_cached


__all__ = ("items", "recipes", "item_details", "recipe_details")


def items():
    """This resource returns a list of items that were discovered by players
    in the game. Details about a single item can be obtained using the
    :func:`item_details` resource.

    """
    return get_cached("items.json").get("items")


def recipes():
    """This resource returns a list of recipes that were discovered by players
    in the game. Details about a single recipe can be obtained using the
    :func:`recipe_details` resource.
    """
    return get_cached("recipes.json").get("recipes")


def item_details(item_id, lang="en"):
    """This resource returns a details about a single item.

    :param item_id: The item to query for.
    :param lang: The language to display the texts in.

    The response is an object with at least the following properties. Note that
    the availability of some properties depends on the type of the item.

    item_id (number):
        The item id.

    name (string):
        The name of the item.

    description (string):
        The item description.

    type (string):
        The item type.

    level (integer):
        The required level.

    rarity (string):
        The rarity. On of ``Junk``, ``Basic``, ``Fine``, ``Masterwork``,
        ``Rare``, ``Exotic``, ``Ascended`` or ``Legendary``.

    vendor_value (integer):
        The value in coins when selling to a vendor.

    icon_file_id (string):
        The icon file id to be used with the render service.

    icon_file_signature (string):
        The icon file signature to be used with the render service.

    game_types (list):
        The game types where the item is usable.
        Currently known game types are: ``Activity``, ``Dungeon``, ``Pve``,
        ``Pvp``, ``PvpLobby`` and ``WvW``

    flags (list):
        Additional item flags.
        Currently known item flags are: ``AccountBound``, ``HideSuffix``,
        ``NoMysticForge``, ``NoSalvage``, ``NoSell``, ``NotUpgradeable``,
        ``NoUnderwater``, ``SoulbindOnAcquire``, ``SoulBindOnUse`` and
        ``Unique``

    restrictions (list):
        Race restrictions: ``Asura``, ``Charr``, ``Human``, ``Norn`` and
        ``Sylvari``.

    Each item type has an `additional key`_ with information specific to that
    item type.

    .. _additional key: item-properties.html

    """
    params = {"item_id": item_id, "lang": lang}
    cache_name = "item_details.%(item_id)s.%(lang)s.json" % params
    return get_cached("item_details.json", cache_name, params=params)


def recipe_details(recipe_id, lang="en"):
    """This resource returns a details about a single recipe.

    :param recipe_id: The recipe to query for.
    :param lang: The language to display the texts in.

    The response is an object with the following properties:

    recipe_id (number):
        The recipe id.

    type (string):
        The type of the produced item.

    output_item_id (string):
        The item id of the produced item.

    output_item_count (string):
        The amount of items produced.

    min_rating (string):
        The minimum rating of the recipe.

    time_to_craft_ms (string):
        The time it takes to craft the item.

    disciplines (list):
        A list of crafting disciplines that can use the recipe.

    flags (list):
        Additional recipe flags. Known flags:

        ``AutoLearned``:
            Set for recipes that don't have to be discovered.

        ``LearnedFromItem``:
            Set for recipes that need a recipe sheet.

    ingredients (list):
        A list of objects describing the ingredients for this recipe. Each
        object contains the following properties:

        item_id (string):
            The item id of the ingredient.

        count (string):
            The amount of ingredients required.

    """
    params = {"recipe_id": recipe_id, "lang": lang}
    cache_name = "recipe_details.%(recipe_id)s.%(lang)s.json" % params
    return get_cached("recipe_details.json", cache_name, params=params)
