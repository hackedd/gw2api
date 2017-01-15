from .endpoint import Endpoint, LocaleAwareEndpoint


class PvpSeasonLeaderboardEndpoint(Endpoint):
    default_page_size = 50


class PvpSeasonEndpoint(LocaleAwareEndpoint):
    def get_leaderboards(self, season_id):
        name = "%s/%s/leaderboards" % (self.name, season_id)
        cache_name = "%s.%s.leaderboards.json" % (self.name, season_id)
        return self.get_cached(name, cache_name)

    def get_leaderboard_endpoint(self, season_id, board, region=None):
        name = "%s/%s/leaderboards/%s" % (self.name, season_id, board)
        if region:
            name += "/" + region
        return PvpSeasonLeaderboardEndpoint(name)

    def get_leaderboard(self, season_id, board, region=None, page=0, page_size=None):
        endpoint = self.get_leaderboard_endpoint(season_id, board, region)
        return endpoint.page(page, page_size)
