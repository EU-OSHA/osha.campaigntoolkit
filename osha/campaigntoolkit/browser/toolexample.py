from Acquisition import aq_parent, aq_inner
from plone.app.layout.viewlets import common as base
from Products.CMFCore.interfaces import IFolderish
from Products.Five.browser import BrowserView

# Number of latest toolexamples to show in the viewlet
LIMIT = 4


def get_examples(context, limit=None):
    """Return ToolExample objects contained in the provided context or its
    parent.

    :param context: object where to look for tool examples. If context is
        not folderish, we look in its parent (useful if we use this method on
        folder's default view)
    :param limit: limit the number of results
    :returns: A list of published tool examples, sorted by date, latest first.
    :rtype: ContentListing object
    """
    if IFolderish.providedBy(context):
        folder = aq_inner(context)
    else:
        folder = aq_parent(context)
    path = folder.getPhysicalPath()
    path = "/".join(path)
    query = {
        'path': {"query": path, "depth": 1},
        'portal_type': 'osha.campaigntoolkit.toolexample',
        'review_state': 'published',
        'sort_on': 'Date',
        'sort_order': 'reverse'
    }

    if limit is not None:
        query['sort_limit'] = limit
        return folder.restrictedTraverse('@@folderListing')(**query)[:limit]
    else:
        return folder.restrictedTraverse('@@folderListing')(**query)


class ToolExampleView(BrowserView):
    def __call__(self):
        return self.index()


class ToolExamplesView(BrowserView):
    """View for the default page of the folder that contains tool
    examples."""

    def __call__(self):
        return self.index()

    def examples(self):
        """Return tool examples contained in this folder."""
        return get_examples(self.context)


class ToolExamplesViewlet(base.ViewletBase):
    """Viewlet which shows the latest tool examples."""

    def latest_examples(self):
        """Return the latest tool examples contained in this folder."""
        return get_examples(self.context, limit=LIMIT)
