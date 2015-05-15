import urllib
import warnings

from .endpoint import EndpointBase

import gw2api


class AuthenticationHelper(object):
    authorization_url = "https://account.guildwars2.com/oauth2/authorization"
    token_url = "https://account.guildwars2.com/oauth2/token"

    def __init__(self, client_id, client_secret, redirect_uri):
        super(AuthenticationHelper, self).__init__()
        warnings.warn("OAuth2 has been deprecated and will be disabled on "
                      "Thursday, June 4th (http://tinyurl.com/gw2oauth).",
                      stacklevel=2)

        self.client_id = client_id
        self.client_secret = client_secret
        self.redirect_uri = redirect_uri

    def authorize_url(self, scope="account offline", **kwargs):
        params = {
            "redirect_uri": self.redirect_uri,
            "client_id": self.client_id,
            "response_type": "code",
            "scope": scope,
        }
        params.update(kwargs)
        return self.authorization_url + "?" + urllib.urlencode(params)

    def get_token(self, code, **kwargs):
        params = {
            "redirect_uri": self.redirect_uri,
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "grant_type": "authorization_code",
            "code": code,
        }
        params.update(kwargs)

        r = gw2api.session.post(self.token_url, data=params)
        r.raise_for_status()
        return r.json()


class AuthenticatedEndpointBase(EndpointBase):
    token = None

    @classmethod
    def set_token(cls, token):
        cls.token = token

    def _get(self, path, **kwargs):
        if self.token:
            headers = kwargs.setdefault("headers", {})
            headers.setdefault("Authorization", "Bearer " + self.token)
        return super(AuthenticatedEndpointBase, self)._get(path, **kwargs)


class AccountEndpoint(AuthenticatedEndpointBase):
    def get(self):
        return self.get_cached(self.name, None)
