import requests

import gw2api.v2
from gw2api.v2.endpoint import EndpointBase, LocaleAwareEndpoint
from gw2api.v2.account import AuthenticatedMixin


def get_prefixed_endpoints(prefix, endpoint):
    endpoints = {}

    for name in dir(endpoint):
        if name.startswith("get_"):
            path = prefix + name[4:].replace("_", "/")
            endpoints[path] = getattr(endpoint, name)
            path = prefix + name[4:].replace("_", "")
            endpoints[path] = getattr(endpoint, name)

    return endpoints


def get_endpoints():
    endpoints = {}

    for name in dir(gw2api.v2):
        value = getattr(gw2api.v2, name)
        if isinstance(value, EndpointBase):
            endpoints[value.name] = value

    endpoints.update(get_prefixed_endpoints("account/",
                                            gw2api.v2.account))
    endpoints.update(get_prefixed_endpoints("achievements/",
                                            gw2api.v2.achievements))
    endpoints.update(get_prefixed_endpoints("characters/:id/",
                                            gw2api.v2.characters))
    endpoints.update(get_prefixed_endpoints("guild/:id/",
                                            gw2api.v2.guild))
    endpoints.update(get_prefixed_endpoints("pvp/seasons/:id/",
                                            gw2api.v2.pvp_seasons))

    return endpoints


def check_endpoint(endpoint, route):
    assert endpoint is not None, "no endpoint for %s" % route["path"]

    if not isinstance(endpoint, EndpointBase):
        return

    if route["lang"]:
        msg = "endpoint for %s is not locale aware" % route["path"]
        assert isinstance(endpoint, LocaleAwareEndpoint), msg
    else:
        msg = "endpoint for %s should not be locale aware" % route["path"]
        assert not isinstance(endpoint, LocaleAwareEndpoint), msg

    if route["auth"]:
        msg = "endpoint for %s is not authenticated" % route["path"]
        assert isinstance(endpoint, AuthenticatedMixin), msg
    else:
        msg = "endpoint for %s should not be authenticated" % route["path"]
        assert not isinstance(endpoint, AuthenticatedMixin), msg


def test_endpoints():
    ignored_endpoints = [
        "emblem", "pvp", "traits-beta", "pvp/games/:id",
        "pvp/seasons/:id", "pvp/standings/:id", "guild/:id",
        "guild/search",
        "pvp/seasons/:id/leaderboards/:board",
        "pvp/seasons/:id/leaderboards/:board/:region",
        "wvw/matches/stats/:id/guilds/:guild_id",
        "wvw/matches/stats/:id/teams/:team/top/kdr",
        "wvw/matches/stats/:id/teams/:team/top/kills",
    ]
    endpoints = get_endpoints()

    v2 = requests.get("https://api.guildwars2.com/v2.json").json()
    for route in v2["routes"]:
        if not route["active"]:
            continue

        endpoint_name = route["path"][4:]  # remove /v2/ from path

        if endpoint_name in ignored_endpoints:
            continue

        endpoint = endpoints.get(endpoint_name)

        yield check_endpoint, endpoint, route
