from .endpoint import Endpoint


class WvwMatchesEndpoint(Endpoint):
    def world(self, world_id):
        params = {"world": world_id}
        cache_name = "wvw_matches_world_%(world)s.json" % params
        return self.get_cached(self.name, cache_name, params=params)
