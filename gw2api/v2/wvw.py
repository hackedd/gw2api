from .endpoint import Endpoint


class WvwMatchesEndpoint(Endpoint):
    def world(self, world_id):
        params = {"world": world_id}
        cache_name = "wvw_matches_world_%(world)s.json" % params
        return self.get_cached(self.name, cache_name, params=params)


class WvwMatchStatsEndpoint(WvwMatchesEndpoint):
    def guild(self, match_id, guild_id):
        path = "%s/%s/guilds/%s" % (self.name, match_id, guild_id)
        cache_name = "wvw_matches_guild_%s_%s.json" % (match_id, guild_id)
        return self.get_cached(path, cache_name)

    def team_top_kdr(self, match_id, team_id):
        path = "%s/%s/teams/%s/top/kdr" % (self.name, match_id, team_id)
        cache_name = "wvw_matches_team_kdr_%s_%s.json" % (match_id, team_id)
        return self.get_cached(path, cache_name)

    def team_top_kills(self, match_id, team_id):
        path = "%s/%s/teams/%s/top/kills" % (self.name, match_id, team_id)
        cache_name = "wvw_matches_team_kills_%s_%s.json" % (match_id, team_id)
        return self.get_cached(path, cache_name)
