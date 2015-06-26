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


class AccountEndpoint(AuthenticatedMixin, EndpointBase):
    def get(self):
        return self.get_cached(self.name, None)

    def get_bank(self):
        return self.get_cached(self.name + "/bank", None)

    def get_materials(self):
        return self.get_cached(self.name + "/materials", None)


class TokenInfoEndpoint(AuthenticatedMixin, EndpointBase):
    def get(self, token=None):
        return self.get_cached(self.name, None, token=token)


class CharacterEndpoint(AuthenticatedMixin, Endpoint):
    def get_inventory(self, id):
        name = "%s/%s/inventory" % (self.name, id)
        return self.get_cached(name, None).get("bags")

    def get_equipment(self, id):
        name = "%s/%s/equipment" % (self.name, id)
        return self.get_cached(name, None).get("equipment")
