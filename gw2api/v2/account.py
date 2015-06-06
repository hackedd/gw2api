from .endpoint import EndpointBase, Endpoint


class AuthenticatedMixin(object):
    token = None

    @classmethod
    def set_token(cls, token):
        cls.token = token

    def _get(self, path, **kwargs):
        if self.token:
            headers = kwargs.setdefault("headers", {})
            headers.setdefault("Authorization", "Bearer " + self.token)
        return super(AuthenticatedMixin, self)._get(path, **kwargs)


class AccountEndpoint(AuthenticatedMixin, EndpointBase):
    def get(self):
        return self.get_cached(self.name, None)


class CharacterEndpoint(AuthenticatedMixin, Endpoint):
    pass
