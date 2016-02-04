import os
import requests


VERSION = "v1"
BASE_URL = "https://api.guildwars2.com/%s/" % VERSION
LANGUAGES = {"en": "English", "es": "Spanish", "de": "German", "fr": "French"}
TYPE_COIN, TYPE_ITEM, TYPE_TEXT, TYPE_MAP = 1, 2, 3, 4
TYPE_SKILL, TYPE_TRAIT = 6, 7
TYPE_RECIPE, TYPE_SKIN, TYPE_OUTFIT = 9, 10, 11
LINK_TYPES = {
    "coin": TYPE_COIN,
    "item": TYPE_ITEM,
    "text": TYPE_TEXT,
    "map": TYPE_MAP,
    "skill": TYPE_SKILL,
    "trait": TYPE_TRAIT,
    "recipe": TYPE_RECIPE,
    "skin": TYPE_SKIN,
    "outfit": TYPE_OUTFIT,
}

session = requests.Session()
cache_dir = None
cache_time = 14 * 24 * 3600


def set_session(sess):
    """Set the requests.Session to use for all API requests.
    """
    global session
    session = sess


def set_cache_dir(directory):
    """Set the directory to cache JSON responses from most API endpoints.
    """
    global cache_dir

    if directory is None:
        cache_dir = None
        return

    if not os.path.exists(directory):
        os.makedirs(directory)
    if not os.path.isdir(directory):
        raise ValueError("not a directory")
    cache_dir = directory


def set_cache_time(time):
    """Set the maximum lifetime for a cached JSON response.
    """
    global cache_time
    cache_time = time


def get_mumble_link():
    from .mumble import gw2link
    return gw2link


from .map import *
from .misc import *
from .items import *
from .skins import *
from .events import *
from .guild import *
from .wvw import *
from .util import *
