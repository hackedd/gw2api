from .util import get_cached


__all__ = ("event_names", "event_details")


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

    If a event_id is given, only the values for that event are returned.

    """
    if event_id:
        cache_name = "event_details.%s.%s.json" % (event_id, lang)
        params = {"event_id": event_id, "lang": lang}
    else:
        cache_name = "event_details.%s.json" % lang
        params = {"lang": lang}

    data = get_cached("event_details.json", cache_name, params=params)
    events = data["events"]
    return events.get(event_id) if event_id else events
