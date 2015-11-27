from .endpoint import Endpoint


class EmblemEndpoint(Endpoint):
    def get_one(self, id):
        # Workaround; https://api.guildwars2.com/v2/emblem/foregrounds/1 gives
        # a 404 but https://api.guildwars2.com/v2/emblem/foregrounds?id=1 works
        cache_name = "%s.%s.json" % (self.name, id)
        return self.get_cached(self.name, cache_name, params={"id": id})
