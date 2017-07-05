from .endpoint import EndpointBase, Endpoint


class AuthenticatedMixin(object):
    token = None

    @staticmethod
    def set_token(token):
        AuthenticatedMixin.token = token

    def _get(self, path, **kwargs):
        token = kwargs.pop("token") if "token" in kwargs else self.token
        if token:
            headers = kwargs.setdefault("headers", {})
            headers.setdefault("Authorization", "Bearer " + token)
        return super(AuthenticatedMixin, self)._get(path, **kwargs)


class AuthenticatedEndpoint(AuthenticatedMixin, Endpoint):
    pass


class AccountAchievementsEndpoint(AuthenticatedEndpoint):
    def get_one(self, id):
        # /v2/account/achievements does not support accessing by ID using the
        # path (/v2/account/achievements/:id) but requires an id parameter.
        cache_name = "%s.%s.json" % (self.name, id)
        return self.get_cached(self.name, cache_name, params={"id": id})


class AccountEndpoint(AuthenticatedMixin, EndpointBase):
    def __init__(self, name):
        super(AccountEndpoint, self).__init__(name)
        self.achievements = AccountAchievementsEndpoint(name + "/achievements")

    def get(self):
        return self.get_cached(self.name, None)

    def get_bank(self):
        return self.get_cached(self.name + "/bank", None)

    def get_materials(self):
        return self.get_cached(self.name + "/materials", None)

    def get_dyes(self):
        return self.get_cached(self.name + "/dyes", None)

    def get_skins(self):
        return self.get_cached(self.name + "/skins", None)

    def get_wallet(self):
        return self.get_cached(self.name + "/wallet", None)

    def get_minis(self):
        return self.get_cached(self.name + "/minis", None)

    def get_achievements(self):
        return self.achievements.get_all()

    def get_inventory(self):
        return self.get_cached(self.name + "/inventory", None)

    def get_titles(self):
        return self.get_cached(self.name + "/titles", None)

    def get_finishers(self):
        return self.get_cached(self.name + "/finishers", None)

    def get_masteries(self):
        return self.get_cached(self.name + "/masteries", None)

    def get_outfits(self):
        return self.get_cached(self.name + "/outfits", None)

    def get_recipes(self):
        return self.get_cached(self.name + "/recipes", None)

    def get_dungeons(self):
        return self.get_cached(self.name + "/dungeons", None)

    def get_raids(self):
        return self.get_cached(self.name + "/raids", None)

    def get_home_nodes(self):
        return self.get_cached(self.name + "/home/nodes", None)

    def get_home_cats(self):
        return self.get_cached(self.name + "/home/cats", None)

    def get_gliders(self):
        return self.get_cached(self.name + "/gliders", None)

    def get_mail_carriers(self):
        return self.get_cached(self.name + "/mailcarriers", None)

    def get_pvp_heroes(self):
        return self.get_cached(self.name + "/pvp/heroes", None)

    def get_mastery_points(self):
        return self.get_cached(self.name + "/mastery/points", None)


class TokenInfoEndpoint(AuthenticatedMixin, EndpointBase):
    def get(self, token=None):
        return self.get_cached(self.name, None, token=token)


class CharacterEndpoint(AuthenticatedEndpoint):
    def get_core(self, id):
        name = "%s/%s/core" % (self.name, id)
        return self.get_cached(name, None)

    def get_crafting(self, id):
        name = "%s/%s/crafting" % (self.name, id)
        return self.get_cached(name, None).get("crafting")

    def get_inventory(self, id):
        name = "%s/%s/inventory" % (self.name, id)
        return self.get_cached(name, None).get("bags")

    def get_equipment(self, id):
        name = "%s/%s/equipment" % (self.name, id)
        return self.get_cached(name, None).get("equipment")

    def get_specializations(self, id):
        name = "%s/%s/specializations" % (self.name, id)
        return self.get_cached(name, None).get("specializations")

    def get_recipes(self, id):
        name = "%s/%s/recipes" % (self.name, id)
        return self.get_cached(name, None).get("recipes")

    def get_backstory(self, id):
        name = "%s/%s/backstory" % (self.name, id)
        return self.get_cached(name, None).get("backstory")

    def get_heropoints(self, id):
        name = "%s/%s/heropoints" % (self.name, id)
        return self.get_cached(name, None)

    def get_training(self, id):
        name = "%s/%s/training" % (self.name, id)
        return self.get_cached(name, None).get("training")

    def get_skills(self, id):
        name = "%s/%s/skills" % (self.name, id)
        return self.get_cached(name, None).get("skills")

    def get_sab(self, id):
        name = "%s/%s/sab" % (self.name, id)
        return self.get_cached(name, None)


class PvpStatsEndpoint(AuthenticatedMixin, EndpointBase):
    def get(self):
        return self.get_cached(self.name, None)


class GuildEndpoint(AuthenticatedEndpoint):
    def get_ranks(self, id):
        name = "%s/%s/ranks" % (self.name, id)
        return self.get_cached(name, None)

    def get_members(self, id):
        name = "%s/%s/members" % (self.name, id)
        return self.get_cached(name, None)

    def get_stash(self, id):
        name = "%s/%s/stash" % (self.name, id)
        return self.get_cached(name, None)

    def get_treasury(self, id):
        name = "%s/%s/treasury" % (self.name, id)
        return self.get_cached(name, None)

    def get_storage(self, id):
        name = "%s/%s/storage" % (self.name, id)
        return self.get_cached(name, None)

    def get_upgrades(self, id):
        name = "%s/%s/upgrades" % (self.name, id)
        return self.get_cached(name, None)

    def get_log(self, id, since=None):
        name = "%s/%s/log" % (self.name, id)
        params = {"since": since} if since else {}
        return self.get_cached(name, None, params=params)

    def get_teams(self, id):
        name = "%s/%s/teams" % (self.name, id)
        return self.get_cached(name, None)

    def search(self, name):
        return self.get_cached(self.name + "/search", None,
                               params={"name": name})
