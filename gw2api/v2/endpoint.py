import os
import time
import json

import gw2api
from .util import ListWrapper
from ..util import mtime


class EndpointBase(object):
    def __init__(self, name):
        super(EndpointBase, self).__init__()
        self.name = name

    def has_cached(self, cache_name):
        if gw2api.cache_dir and gw2api.cache_time and cache_name:
            cache_file = os.path.join(gw2api.cache_dir, cache_name)
            return mtime(cache_file) >= time.time() - gw2api.cache_time
        else:
            return False

    def get_cached(self, path, cache_name, **kwargs):
        """Request a resource form the API, first checking if there is a cached
        response available. Returns the parsed JSON data.
        """
        if gw2api.cache_dir and gw2api.cache_time and cache_name:
            cache_file = os.path.join(gw2api.cache_dir, cache_name)
            if mtime(cache_file) >= time.time() - gw2api.cache_time:
                with open(cache_file, "r") as fp:
                    return json.load(fp)
        else:
            cache_file = None

        data = self._get(path, **kwargs)

        if cache_file:
            with open(cache_file, "w") as fp:
                json.dump(data, fp, indent=2)

        return data

    def _get(self, path, **kwargs):
        r = gw2api.session.get(gw2api.v2.BASE_URL + path, **kwargs)

        if not r.ok:
            try:
                response = r.json()
            except ValueError:  # pragma: no cover
                response = None

            if isinstance(response, dict) and "text" in response:
                r.reason = response["text"]

        r.raise_for_status()
        return r.json()


class Endpoint(EndpointBase):
    def get_ids(self):
        return self.get_cached(self.name, self.name + ".json")

    def get_all(self):
        cache_name = self.name + ".all.json"
        return self.get_cached(self.name, cache_name, params={"ids": "all"})

    def get(self, *args):
        if len(args) == 1:
            if isinstance(args[0], (list, tuple)):
                args = args[0]
            else:
                return self.get_one(args[0])

        params = {"ids": ",".join(map(str, args))}
        cache_name = self.name + ".%(ids)s.json" % params

        return self.get_cached(self.name, cache_name, params=params)

    def get_one(self, id):
        name = "%s/%s" % (self.name, id)
        cache_name = "%s.%s.json" % (self.name, id)
        return self.get_cached(name, cache_name)

    def page(self, page=0, page_size=20):
        params = {"page": page, "page_size": page_size}
        cache_name = self.name + ".page-%(page)d.%(page_size)d.json" % params
        data = self.get_cached(self.name, cache_name, params=params)
        return ListWrapper(self, page, data, args=(page_size, ))


class LocaleAwareEndpoint(Endpoint):
    default_language = "en"

    def get_all(self, lang=None):
        if lang is None:
            lang = self.default_language

        params = {"ids": "all", "lang": lang}
        cache_name = self.name + "." + lang + ".all.json"
        return self.get_cached(self.name, cache_name, params=params)

    def get(self, *args, **kwargs):
        lang = kwargs.get("lang") or self.default_language

        if len(args) == 1:
            if isinstance(args[0], (list, tuple)):
                args = args[0]
            else:
                return self.get_one(args[0], lang)

        params = {"ids": ",".join(map(str, args)), "lang": lang}
        cache_name = self.name + ".%(lang)s.%(ids)s.json" % params

        return self.get_cached(self.name, cache_name, params=params)

    def get_one(self, id, lang=None):
        if lang is None:
            lang = self.default_language
        name = "%s/%s" % (self.name, id)
        cache_name = "%s.%s.%s.json" % (self.name, lang, id)
        return self.get_cached(name, cache_name, params={"lang": lang})

    def page(self, page=0, page_size=20, lang=None):
        if lang is None:
            lang = self.default_language

        params = {"page": page, "page_size": page_size, "lang": lang}
        cache_name = (self.name + "." + lang +
                      ".page-%(page)d.%(page_size)d.json" % params)
        data = self.get_cached(self.name, cache_name, params=params)
        return ListWrapper(self, page, data, args=(page_size, lang))
