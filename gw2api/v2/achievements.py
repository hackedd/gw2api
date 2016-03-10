from .endpoint import LocaleAwareEndpoint


class AchievementEndpoint(LocaleAwareEndpoint):
    def get_daily(self):
        return self.get("daily")

    def get_daily_tomorrow(self):
        return self.get("daily/tomorrow")
