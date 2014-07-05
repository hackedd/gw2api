from .util import get_cached


__all__ = ("continents", "map_names", "maps", "map_floor")


def continents():
    """This resource returns static information about the continents used with
    the map_floor resource.

    The response is a dictionary where the key is the continent id, and the
    value is a dictionary containing the following properties:

    name (string):
        The name of the continent.

    continent_dims (dimension):
        The width and height dimensions of the continent.

    min_zoom (number):
        The minimal zoom level for use with the map tile service.

    max_zoom (number):
        The maximum zoom level for use with the map tile service.

    floors (list):
        A list of floors available for this continent.

    *Note: There are only two continents, Tyria and Mists.*

    """
    return get_cached("continents.json").get("continents")


def map_names(lang="en"):
    """This resource returns an dictionary of the localized map names for
    the specified language. Only maps with events are listed - if you need a
    list of all maps, use ``maps.json`` instead.

    :param lang: The language to query the names for.
    :return: the response is a dictionary where the key is the map id and the
             value is the name of the map in the specified language.

    """
    cache_name = "map_names.%s.json" % lang
    data = get_cached("map_names.json", cache_name, params=dict(lang=lang))
    return dict([(item["id"], item["name"]) for item in data])


def maps(map_id=None, lang="en"):
    """This resource returns details about maps in the game, including details
    about floor and translation data on how to translate between world
    coordinates and map coordinates.

    :param map_id: Only list this map.
    :param lang: Show localized texts in the specified language.

    The response is a dictionary where the key is the map id and the value is
    a dictionary containing the following properties:

    map_name (string)
        The map name.

    min_level (number)
        The minimal level of this map.

    max_level (number)
        The maximum level of this map.

    default_floor (number)
        The default floor of this map.

    floors (list)
        A list of available floors for this map.

    region_id (number)
        The id of the region this map belongs to.

    region_name (string)
        The name of the region this map belongs to.

    continent_id (number)
        The id of the continent this map belongs to.

    continent_name (string)
        The name of the continent this map belongs to.

    map_rect (rect)
        The dimensions of the map.

    continent_rect (rect)
        The dimensions of the map within the continent coordinate system.

    If a map_id is given, only the values for that map are returned.

    """
    if map_id:
        cache_name = "maps.%s.%s.json" % (map_id, lang)
        params = {"map_id": map_id, "lang": lang}
    else:
        cache_name = "maps.%s.json" % lang
        params = {"lang": lang}

    data = get_cached("maps.json", cache_name, params=params).get("maps")
    return data.get(str(map_id)) if map_id else data


def map_floor(continent_id, floor, lang="en"):
    """This resource returns details about a map floor, used to populate a
    world map. All coordinates are map coordinates.

    The returned data only contains static content. Dynamic content, such as
    vendors, is not currently available.

    :param continent_id: The continent.
    :param floor: The map floor.
    :param lang: Show localized texts in the specified language.

    The response is an object with the following properties:

    texture_dims (dimension)
        The dimensions of the texture.

    clamped_view (rect)
        If present, it represents a rectangle of downloadable textures. Every
        tile coordinate outside this rectangle is not available on the tile
        server.

    regions (object)
        A mapping from region id to an object.

    Each region object contains the following properties:

    name (string)
        The region name.

    label_coord (coordinate)
        The coordinates of the region label.

    maps (object)
        A mapping from the map id to an object.

        Each map object contains the following properties:

        name (string)
            The map name.

        min_level (number)
            The minimum level of the map.

        max_level (number)
            The maximum level of the map.

        default_floor (number)
            The default floor of the map.

        map_rect (rect)
            The dimensions of the map.

        continent_rect (rect)
            The dimensions of the map within the continent coordinate system.

        points_of_interest (list)
            A list of points of interest (landmarks, waypoints and vistas)

            Each points of interest object contains the following properties:

            poi_id (number)
                The point of interest id.

            name (string)
                The name of the point of interest.

            type (string)
                The type. This can be either "landmark" for actual points of
                interest, "waypoint" for waypoints, or "vista" for vistas.

            floor (number)
                The floor of this object.

            coord (coordinate)
                The coordinates of this object.

        tasks (list)
            A list of renown hearts.

            Each task object contains the following properties:

            task_id (number)
                The renown heart id.

            objective (string)
                The objective or name of the heart.

            level (number)
                The level of the heart.

            coord (coordinate)
                The coordinates where it takes place.

        skill_challenges (list)
            A list of skill challenges.

            Each skill challenge object contains the following properties:

            coord (coordinate)
                The coordinates of this skill challenge.

        sectors (list)
            A list of areas within the map.

            Each sector object contains the following properties:

            sector_id (number)
                The area id.

            name (string)
                The name of the area.

            level (number)
                The level of the area.

            coord (coordinate)
                The coordinates of this area (this is usually the center
                position).

    Special types:
    Dimension properties are two-element lists of width and height.
    Coordinate properties are two-element lists of the x and y position.
    Rect properties are two-element lists of coordinates of the upper-left and
    lower-right coordinates.

    """
    cache_name = "map_floor.%s-%s.%s.json" % (continent_id, floor, lang)
    params = {"continent_id": continent_id, "floor": floor, "lang": lang}
    return get_cached("map_floor.json", cache_name, params=params)
