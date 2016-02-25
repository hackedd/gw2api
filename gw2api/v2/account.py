from .endpoint import EndpointBase, Endpoint


class AuthenticatedMixin(object):
    token = None

    @classmethod
    def set_token(cls, token):
        cls.token = token

    def _get(self, path, **kwargs):
        token = kwargs.pop("token") if "token" in kwargs else self.token
        if token:
            headers = kwargs.setdefault("headers", {})
            headers.setdefault("Authorization", "Bearer " + token)
        return super(AuthenticatedMixin, self)._get(path, **kwargs)


class AuthenticatedEndpoint(AuthenticatedMixin, Endpoint):
    pass


class AccountEndpoint(AuthenticatedMixin, EndpointBase):
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
        return self.get_cached(self.name + "/achievements", None)

    def get_inventory(self):
        return self.get_cached(self.name + "/inventory", None)


class TokenInfoEndpoint(AuthenticatedMixin, EndpointBase):
    def get(self, token=None):
        return self.get_cached(self.name, None, token=token)


class CharacterEndpoint(AuthenticatedEndpoint):
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

    def get_upgrades(self, id):
        name = "%s/%s/upgrades" % (self.name, id)
        return self.get_cached(name, None)

    def get_log(self, id):
        name = "%s/%s/log" % (self.name, id)
        return self.get_cached(name, None)

    def get_teams(self, id):
        name = "%s/%s/teams" % (self.name, id)
        return self.get_cached(name, None)
