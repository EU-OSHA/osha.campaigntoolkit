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
    """View for the ToolExample type.

    Note that ToolExample type and the accompanying view are used in two
    related, but different scenarios:
     - to show general information about a Tool Example (e.g. 'Poster') with
       a list of practical examples
     - to show a practical example (e.g. 'Tips for the safe use of gloves')

    We have the following structure:

        Folder with Tool Examples -> toolexample1 as default view
          |
          |--toolexample1 -> ToolExampleView (tool example overview with a
                                              list of practical examples)
          |--toolexample2 -> ToolExampleView (practical example view)
          |--toolexample3 -> ToolExampleView (practical example view)
          |..

    """

    def __call__(self):
        return self.index()

    def examples(self):
        """Return tool examples contained in the parent folder.

        Search for results only if context is set as default view on the
        parent folder, otherwise return an empty list.

        OSH related examples have sorting precedence over the others.
        """
        if not self._context_is_default_view():
            return []

        # OSH related examples should come first
        # (NOTE: items in list are already sorted by date)
        osh_related, others = [], []

        for item in get_examples(aq_parent(self.context)):
            # don't include the context
            if item.id == self.context.id:
                continue
            if item.OSH_related:
                osh_related.append(item)
            else:
                others.append(item)

        return osh_related + others

    def _context_is_default_view(self):
        """Check if context is set as default view on the parent folder.
        """
        if (
            hasattr(self.context.__parent__, 'default_page') and
            self.context.__parent__.default_page == self.context.id
        ):
            return True
        else:
            return False


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
