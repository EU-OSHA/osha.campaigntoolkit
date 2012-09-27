from Acquisition import aq_parent, aq_inner
from plone.app.layout.viewlets import common as base
from Products.CMFCore.interfaces import IFolderish
from Products.Five.browser import BrowserView

# Number of latest toolexamples to show in the viewlet
LIMIT = 4


class ToolExampleView(BrowserView):
    def __call__(self):
        return self.index()


class ToolExamplesView(BrowserView):
    """View for the default page of the folder that contains tool
    examples."""

    def __call__(self):
        return self.index()


class ToolExamplesViewlet(base.ViewletBase):
    """Viewlet which shows the latest tool examples."""

    def latest_examples(self):
        if IFolderish.providedBy(self.context):
            folder = aq_inner(self.context)
        else:
            folder = aq_parent(self.context)
        path = folder.getPhysicalPath()
        path = "/".join(path)

        return folder.restrictedTraverse('@@folderListing')(
            path={"query": path, "depth": 1},
            portal_type='osha.campaigntoolkit.toolexample',
            review_state='published',
            sort_on='Date',
            sort_order='reverse',
            sort_limit=LIMIT)[:LIMIT]
