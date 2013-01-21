from Acquisition import aq_parent, aq_inner
from plone.app.layout.viewlets import common as base
from Products.Five.browser import BrowserView
from plone.app.contentlisting.interfaces import IContentListing

# Number of latest toolexamples to show in the viewlet
LIMIT = 4


def get_examples(context, limit=None, osh_related_only=False):
    """Return ToolExample objects contained in the provided context or its
    parent.

    :param context: object where to look for tool examples. If context is
        set as default view for its parent folder, we look in that parent
        folder
    :param limit: limit the number of results
    :returns: A list of published tool examples, sorted by date, latest first.
    :rtype: ContentListing object
    """
    if (
        hasattr(context.__parent__, 'default_page') and
        context.__parent__.default_page == context.id
    ):
        folder = aq_parent(context)
    else:
        folder = aq_inner(context)
    path = folder.getPhysicalPath()
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

    if folder == context.portal_url.getPortalObject():
        return IContentListing(context.portal_catalog(query)[:limit])

    if limit is not None:
        query['sort_limit'] = limit
        return folder.restrictedTraverse('@@folderListing')(**query)[:limit]
    else:
        return folder.restrictedTraverse('@@folderListing')(**query)


class ToolExampleView(BrowserView):
    """View for the ToolExample type."""

    def __call__(self):
        return self.index()

    def examples(self):
        """Return tool examples contained in this folder.

        OSH related examples have sorting precedence over the others.
        """
        examples = get_examples(self.context)

        # OSH related examples should come first
        # (NOTE: items in list are already sorted by date)
        osh_related, others = [], []

        for item in examples:
            if item.OSH_related:
                osh_related.append(item)
            else:
                others.append(item)

        return osh_related + others


class ToolExamplesViewlet(base.ViewletBase):
    """Viewlet which shows the latest tool examples."""

    def latest_examples(self):
        """Return the latest OSH related tool examples
        contained in this folder.
        """
        return get_examples(self.context, limit=LIMIT, osh_related_only=True)
