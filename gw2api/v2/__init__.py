VERSION = "v2"
BASE_URL = "https://api.guildwars2.com/%s/" % VERSION
LANGUAGES = {
    "en": "English",
    "es": "Spanish",
    "de": "German",
    "fr": "French",
    "ko": "Korean",
    "zh": "Chinese"
}


from .endpoint import Endpoint, LocaleAwareEndpoint
from .recipes import RecipeSearchEndpoint


accounts = Endpoint("accounts")
build = Endpoint("build")
characters = Endpoint("characters")
colors = LocaleAwareEndpoint("colors")
exchange = Endpoint("commerce/exchange")
listings = Endpoint("commerce/listings")
prices = Endpoint("commerce/prices")
continents = Endpoint("continents")
events = LocaleAwareEndpoint("events")
events_state = Endpoint("events-state")
files = Endpoint("files")
floors = LocaleAwareEndpoint("floors")
items = LocaleAwareEndpoint("items")
leaderboards = Endpoint("leaderboards")
maps = LocaleAwareEndpoint("maps")
quaggans = Endpoint("quaggans")
recipes = Endpoint("recipes")
recipe_search = RecipeSearchEndpoint(recipes)
skins = LocaleAwareEndpoint("skins")
worlds = LocaleAwareEndpoint("worlds")
wvw_matches = Endpoint("wvw/matches")
wvw_objectives = LocaleAwareEndpoint("wvw/objectives")
