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
from .account import AccountEndpoint, TokenInfoEndpoint, CharacterEndpoint
from .transactions import TransactionEndpoint


build = Endpoint("build")
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
specializations = Endpoint("specializations")
traits = Endpoint("traits-beta")
worlds = LocaleAwareEndpoint("worlds")
wvw_matches = Endpoint("wvw/matches")
wvw_objectives = LocaleAwareEndpoint("wvw/objectives")
materials = LocaleAwareEndpoint("materials")
currencies = Endpoint("currencies")

account = AccountEndpoint("account")
token_info = TokenInfoEndpoint("tokeninfo")
characters = CharacterEndpoint("characters")
transactions = TransactionEndpoint("commerce/transactions")
