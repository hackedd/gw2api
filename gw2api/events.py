from .util import get_cached


__all__ = ("events", "event_names", "event_details")


def events(world_id=None, map_id=None, event_id=None):
    """This resource returns a list of events and their status that match the
    given filter. *The results are not cached.*

    :param world_id: Only list events for that world.
    :param map_id: Only list events in that map.
    :param event_id: Only list this event.

    The response is a list of events, each of which contains the following:

    world_id (number)
        The world on which the event is running.

    map_id (number)
        The map on which the event is running.

    event_id (string)
        The event GUID identifying the event.

    state (string)
        The current state of the event.

        The state can be one of the following values:

        ``Inactive``
            The event is not running.

        ``Active``
            The event is running now.

        ``Success``
            The event has succeeded.

        ``Fail``
            The event has failed.

        ``Warmup``
            The event is inactive and waiting for certain criteria to be met
            before becoming `Active`.

        ``Preparation``
            The criteria for the event to start have been met, but certain
            activities (such as an NPC dialogue) have not completed yet. After
            the activites have been completed, the event will become `Active`.

    """
    params = {}
    if world_id:
        params["world_id"] = world_id
    if map_id:
        params["map_id"] = map_id
    if event_id:
        params["event_id"] = event_id

    data = get_cached("events.json", False, params=params)
    return data["events"]


def event_names(lang="en"):
    """This resource returns an unordered list of the localized event names
    for the specified language.

    :param lang: The language to query the names for.
    :return: A dictionary where the key is the event id and the value is the
             name of the event in the specified language.

    """
    cache_name = "event_names.%s.json" % lang
    data = get_cached("event_names.json", cache_name, params=dict(lang=lang))
    return dict([(event["id"], event["name"]) for event in data])


def event_details(event_id=None, lang="en"):
    """This resource returns static details about available events.

    :param event_id: Only list this event.
    :param lang: Show localized texts in the specified language.

    The response is a dictionary where the key is the event id, and the value
    is a dictionary containing the following properties:

    name (string)
        The name of the event.

    level (int)
        The event level.

    map_id (int)
        The map where the event takes place.

    flags (list)
        A list of additional flags. Possible flags are:

        ``group_event``
            For group events

        ``map_wide``
            For map-wide events.

    location (object)
        The location of the event.

        type (string)
            The type of the event location, can be ``sphere``, ``cylinder`` or
            ``poly``.

        center (list)
            X, Y, Z coordinates of the event location.

        radius (number) (type ``sphere`` and ``cylinder``)
            Radius of the event location.

        z_range (list) (type ``poly``)
            List of Minimum and Maximum Z coordinate.

        points (list) (type ``poly``)
            List of Points (X, Y) denoting the event location perimeter.

    """
    if event_id:
        cache_name = "event_details.%s.%s.json" % (event_id, lang)
        params = {"event_id": event_id, "lang": lang}
    else:
        cache_name = "event_details.%s.json" % lang
        params = {"lang": lang}

    data = get_cached("event_details.json", cache_name, params=params)
    return data["events"]
