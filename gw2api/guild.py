import warnings

from .util import get_cached


__all__ = ("guild_details", )


def guild_details(guild_id=None, name=None):
    """This resource returns details about a guild.

    :param guild_id: The guild id to query for.
    :param name: The guild name to query for.

    *Note: Only one parameter is required; if both are set, the guild Id takes
    precedence and a warning will be logged.*

    The response is a dictionary with the following keys:

    guild_id (string):
        The guild id.

    guild_name (string):
        The guild name.

    tag (string):
        The guild tag.

    emblem (object):
        If present, it holds detailed information about the guilds emblem.

    The emblem dictionary contains the following information:

    background_id (number):
        The id of the background image.

    foreground_id (number):
        The id of the foreground image.

    flags (list):
        A list of additional flags, possible values are:
        ``FlipBackgroundHorizontal``, ``FlipBackgroundVertical``,
        ``FlipForegroundHorizontal`` and ``FlipForegroundVertical``.

    background_color_id (number):
        The background color id.

    foreground_primary_color_id (number):
        The primary foreground color id.

    foreground_secondary_color_id (number):
        The secondary foreground color id.

    """
    if guild_id and name:
        warnings.warn("both guild_id and name are specified, "
                      "name will be ignored")

    if guild_id:
        params = {"guild_id": guild_id}
        cache_name = "guild_details.%s.json" % guild_id
    elif name:
        params = {"guild_name": name}
        cache_name = "guild_details.%s.json" % name
    else:
        raise Exception("specify either guild_id or name")

    return get_cached("guild_details.json", cache_name, params=params)
