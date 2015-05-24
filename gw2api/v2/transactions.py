from .endpoint import EndpointBase
from .account import AuthenticatedMixin
from .util import ListWrapper


class TransactionEndpoint(AuthenticatedMixin, EndpointBase):
    def page(self, page, page_size, suffix):
        path = self.name + "/" + suffix
        params = {"page": page, "page_size": page_size}
        data = self.get_cached(path, None, params=params)
        return ListWrapper(self, page, data, args=(page_size, suffix))

    def current_buys(self, page=0, page_size=20):
        return self.page(page, page_size, "current/buys")

    def current_sells(self, page=0, page_size=20):
        return self.page(page, page_size, "current/sells")

    def history_buys(self, page=0, page_size=20):
        return self.page(page, page_size, "history/buys")

    def history_sells(self, page=0, page_size=20):
        return self.page(page, page_size, "history/sells")
