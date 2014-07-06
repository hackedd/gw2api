from datetime import datetime

from .util import get_cached


__all__ = ("matches", "match_details", "objective_names")


def parse_datetime(date_string):
    """Parse a datetime string as returned by the ``matches`` endpoint to a
    datetime object.

    >>> parse_datetime('2014-07-04T18:00:00Z')
    datetime.datetime(2014, 7, 4, 18, 0)

    """
    return datetime.strptime(date_string, "%Y-%m-%dT%H:%M:%SZ")


def matches():
    """This resource returns a list of the currently running WvW matches, with
    the participating worlds included in the result. Further details about a
    match can be requested using the ``match_details`` function.

    The response is a list of match objects, each of which contains the
    following properties:

    wvw_match_id (string):
        The WvW match id.

    red_world_id (number):
        The world id of the red world.

    blue_world_id (number):
        The world id of the blue world.

    green_world_id (number):
        The world id of the green world.

    start_time (datetime):
        A timestamp of when the match started.

    end_time (datetime):
        A timestamp of when the match ends.

    """
    wvw_matches = get_cached("wvw/matches.json", False).get("wvw_matches")
    for match in wvw_matches:
        match["start_time"] = parse_datetime(match["start_time"])
        match["end_time"] = parse_datetime(match["end_time"])
    return wvw_matches


def match_details(match_id):
    """This resource returns further details about the specified match,
    including the total score and further details for each map.

    :param match_id: The WvW match to query for.

    The response is an object with the following properties:

    match_id (string):
        The WvW match id.

    scores (list):
        A list of the three total scores (order: red, blue, green).

    maps (list):
        A list of objects containing detailed information about each of the
        four maps.

    The map detail objects contain the following properties:

    type (string):
        The identifier for the map. Can be either RedHome, GreenHome or
        BlueHome for the borderlands or Center for Eternal Battlegrounds.

    scores (list):
        A list of the three individual scores for this map; in the order red,
        blue, green.

    objectives (list):
        A list of objective objects for this map. Each object contains the
        following properties:

        id (number):
            The objective id.

        owner (string):
            The current owner of the objective. Can be any one of Red, Green,
            Blue or Neutral.

        owner_guild (string):
            The guild id of the guild currently claiming the objective. This
            property is missing if the objective is not claimed.

    bonuses (list):
        A list of all bonuses being granted by this map. If no player team
        owns a bonus from the map, this list is empty.

        type (string):
            A shorthand name for the bonus. Currently the only known bonus
            type is ``bloodlust``: `Borderlands Bloodlust`_

        owner (string):
            The current owner of the bonus. Can be any one of Red, Green, or
            Blue. Neutral-owned bonuses are not listed.

    .. _Borderlands Bloodlust:
       http://wiki.guildwars2.com/wiki/Borderlands_Bloodlust

    """
    return get_cached("wvw/match_details.json", False,
                      params={"match_id": match_id})


def objective_names(lang="en"):
    """This resource returns a list of the localized WvW objective names for
    the specified language.

    :param lang: The language to query the names for.
    :return: A dictionary mapping the objective Ids to the names.

    *Note that these are not the names displayed in the game, but rather the
    abstract type.*

    """
    params = {"lang": lang}
    cache_name = "objective_names.%(lang)s.json" % params
    data = get_cached("wvw/objective_names.json", cache_name, params=params)
    return dict([(objective["id"], objective["name"]) for objective in data])
