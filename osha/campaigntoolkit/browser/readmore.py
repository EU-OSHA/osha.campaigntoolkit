from Products.Five.browser import BrowserView


class ReadMoreView(BrowserView):
    """View for displaying the content of all pages in the folder on one
    page, with collapsible sections.
    """

    def __call__(self):
        return self.index()
