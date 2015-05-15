from .endpoint import EndpointBase


class RecipeSearchEndpoint(EndpointBase):
    def __init__(self, recipe_endpoint):
        super(RecipeSearchEndpoint, self).__init__("recipes/search")
        self.recipe_endpoint = recipe_endpoint

    def input(self, item_id, details=False):
        params = {"input": item_id}
        cache_name = "recipes_input_%(input)s.json" % params
        recipe_ids = self.get_cached(self.name, cache_name, params=params)
        return self.recipe_endpoint.get(recipe_ids) if details else recipe_ids

    def output(self, item_id, details=False):
        params = {"output": item_id}
        cache_name = "recipes_output_%(output)s.json" % params
        recipe_ids = self.get_cached(self.name, cache_name, params=params)
        return self.recipe_endpoint.get(recipe_ids) if details else recipe_ids
