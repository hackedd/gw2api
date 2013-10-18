from .util import get_cached


__all__ = ("build", "colors", "files")


def build():
    """This resource returns the current build id of the game.
    The result of this function is not cached.

    """
    return get_cached("build.json", False).get("build_id")


def colors(lang="en"):
    """This resource returns all dyes in the game, including localized names
    and their color component information.

    :param lang: The language to query the names for.

    The response is a dictionary where color ids are mapped to an dictionary
    containing the following properties:

    name (string):
        The name of the dye.

    base_rgb (list):
        The base RGB values.

    cloth (object):
        Detailed information on its appearance when applied on cloth armor.

    leather (object):
        Detailed information on its appearance when applied on leather armor.

    metal (object):
        Detailed information on its appearance when applied on metal armor.

    The detailed information object contains the following properties:

    brightness (number):
        The brightness.

    contrast (number):
        The contrast.

    hue (number):
        The hue in the HSL colorspace.

    saturation (number):
        The saturation in the HSL colorspace.

    lightness (number):
        The lightness in the HSL colorspace.

    rgb (list):
        A list containing precalculated RGB values.

    """
    cache_name = "colors.%s.json" % lang
    data = get_cached("colors.json", cache_name, params=dict(lang=lang))
    return data["colors"]


def files():
    """This resource returns commonly requested in-game assets that may be
    used to enhance API-derived applications. The returned information can be
    used with the render service to retrieve assets.

    The response is an object where file identifiers are mapped to an object
    containing the following properties:

    file_id (string):
        The file id to be used with the render service.

    signature (string):
        The file signature to be used with the render service.

    """
    return get_cached("files.json")
