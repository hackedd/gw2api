import requests

import gw2api.v2
from gw2api.v2.endpoint import EndpointBase, LocaleAwareEndpoint


def get_prefixed_endpoints(prefix, endpoint):
    endpoints = {}

    for name in dir(endpoint):
        if name.startswith("get_"):
            path = prefix + name[4:].replace("_", "/")
            endpoints[path] = endpoint

    return endpoints


def get_endpoints():
    endpoints = {}

    for name in dir(gw2api.v2):
        value = getattr(gw2api.v2, name)
        if isinstance(value, EndpointBase):
            endpoints[value.name] = value

    endpoints.update(get_prefixed_endpoints("account/",
                                            gw2api.v2.AccountEndpoint))
    endpoints.update(get_prefixed_endpoints("achievements/",
                                            gw2api.v2.AchievementEndpoint))
    endpoints.update(get_prefixed_endpoints("characters/:id/",
                                            gw2api.v2.CharacterEndpoint))
    endpoints.update(get_prefixed_endpoints("guild/:id/",
                                            gw2api.v2.GuildEndpoint))

    return endpoints


def check_endpoint(endpoint, route):
    assert endpoint is not None, "no endpoint for %s" % route["path"]

    if route["lang"]:
        msg = "endpoint for %s is not locale aware" % route["path"]
        assert isinstance(endpoint, LocaleAwareEndpoint), msg
    else:
        msg = "endpoint for %s should not be locale aware" % route["path"]
        assert not isinstance(endpoint, LocaleAwareEndpoint), msg


def test_endpoints():
    ignored_endpoints = ["emblem", "pvp", "traits-beta", "pvp/games/:id",
                         "pvp/seasons/:id", "pvp/standings/:id", "guild/:id",
                         "guild/search"]
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
