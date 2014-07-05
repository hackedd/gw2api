from .util import get_cached


__all__ = ("skins", "skin_details")


def skins():
    """This resource returns a list of skins that were discovered by players
    in the game. Details about a single skin can be obtained using the
    :func:`skin_details` resource.

    """
    return get_cached("skins.json").get("skins")


def skin_details(skin_id, lang="en"):
    """This resource returns details about a single skin.

    :param skin_id: The skin to query for.
    :param lang: The language to display the texts in.

    The response is an object with at least the following properties. Note that
    the availability of some properties depends on the type of item the skin
    applies to.

    skin_id (number):
        The skin id.

    name (string):
        The name of the skin.

    type (string):
        The type of item the skin applies to. One of ``Armor``, ``Back`` or
        ``Weapon``.

    flags (list):
        Skin flags. Currently known skin flags are ``ShowInWardrobe``,
        ``HideIfLocked`` and ``NoCost``.

    restrictions (list):
        Race restrictions: ``Asura``, ``Charr``, ``Human``, ``Norn`` and
        ``Sylvari``.

    icon_file_id (string):
        The icon file id to be used with the render service.

    icon_file_signature (string):
        The icon file signature to be used with the render service.

    """
    params = {"skin_id": skin_id, "lang": lang}
    cache_name = "skin_details.%(skin_id)s.%(lang)s.json" % params
    return get_cached("skin_details.json", cache_name, params=params)
