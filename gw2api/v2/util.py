class ListWrapper(list):
    def __init__(self, endpoint, page, data, args):
        super(ListWrapper, self).__init__(data)
        self.endpoint = endpoint
        self.page = page
        self.args = args
        self.meta = getattr(data, "meta", None)

    def previous_page(self):
        return self.endpoint.page(self.page - 1, *self.args)

    def next_page(self):
        return self.endpoint.page(self.page + 1, *self.args)
