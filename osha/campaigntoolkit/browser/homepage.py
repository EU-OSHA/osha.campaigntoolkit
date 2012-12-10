from Products.Five.browser import BrowserView


class HomepageView(BrowserView):

    def __call__(self):
        return self.index()
