from Acquisition import aq_parent
from plone.app.layout.viewlets import common as base
from Products.CMFPlone.utils import isDefaultPage
from Products.Five.browser import BrowserView
from plone.app.contentlisting.interfaces import IContentListing

# Number of latest toolexamples to show in the viewlet
LIMIT = 4


def get_examples(context, limit=None, osh_related_only=False):
    """Return ToolExample objects contained in the provided context.

    :param context: object where to look for tool examples.
    :param limit: limit the number of results
    :returns: A list of published tool examples, sorted by date, latest first.
    :rtype: ContentListing object
    """
    path = context.getPhysicalPath()
    path = "/".join(path)
    query = {
        'path': {"query": path},
        'portal_type': 'osha.campaigntoolkit.toolexample',
        'review_state': 'published',
        'sort_on': 'Date',
        'sort_order': 'reverse'
    }
    if osh_related_only:
        query['OSH_related'] = True

    if context == context.portal_url.getPortalObject():
        return IContentListing(context.portal_catalog(query)[:limit])

    if not context.restrictedTraverse('@@folderListing', None):
        return None
    if limit is not None:
        query['sort_limit'] = limit
        return context.restrictedTraverse('@@folderListing')(**query)[:limit]
    else:
        return context.restrictedTraverse('@@folderListing')(**query)


class ToolExampleView(BrowserView):
    """View for the ToolExample type."""

    def __call__(self):
        return self.index()


class ToolExamplesHighlightsViewlet(base.ViewletBase):
    """Viewlet which shows the latest tool examples, useful for displaying
    e.g. on the front page.
    """

    def latest_examples(self):
        """Return the latest OSH related tool examples contained in this
        folder (and subfolders).
        """
        if isDefaultPage(self.context, self.request):
            obj = aq_parent(self.context)
        else:
            obj = self.context
        return get_examples(obj, limit=LIMIT, osh_related_only=True)


class ToolExamplesViewlet(base.ViewletBase):
    """Viewlet which shows the latest tool examples on the tool example index
    page.
    """

    def __init__(self, context, request, view, manager=None):
        super(ToolExamplesViewlet, self).__init__(
            context, request, view, manager)
        self.examples = self._latest_examples()

    def _latest_examples(self):
        """Return the latest OSH related tool examples contained in this
        folder (and subfolders).

        OSH related examples have sorting precedence over the others.
        """
        if not isDefaultPage(self.context, self.request):
            return

        # OSH related examples should come first
        # (NOTE: items in list are already sorted by date)
        osh_related, others = [], []

        for item in get_examples(aq_parent(self.context), limit=LIMIT):
            if item.OSH_related:
                osh_related.append(item)
            else:
                others.append(item)

        return osh_related + others

    def render(self):
        """Render the viewlet only if there is at least one tool example in
        the folder and this page is set as default view for this folder.
        """
        if (
            isDefaultPage(self.context, self.request) and
            len(self.examples) > 0
        ):
            return super(ToolExamplesViewlet, self).render()
        return ""
