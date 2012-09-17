from osha.campaigntoolkit import  _
from plone.app.portlets.portlets import base
from plone.portlets.interfaces import IPortletDataProvider
from Products.CMFCore.utils import getToolByName
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from zope.interface import implements


class IDownloadsPortlet(IPortletDataProvider):
    """Portlet that displays a list of download links for files or images,
    contained in the (folderish) context object.
    """


class Assignment(base.Assignment):
    """Portlet assignment.

    This is what is actually managed through the portlets UI and associated
    with columns.
    """

    implements(IDownloadsPortlet)

    def __init__(self):
        pass

    @property
    def title(self):
        """This property is used to give the title of the portlet in the
        'manage portlets' screen.
        """
        return _(u"Downloads portlet")


class Renderer(base.Renderer):
    """Portlet renderer."""
    render = ViewPageTemplateFile('downloadsportlet.pt')

    @property
    def available(self):
        """Don't show the portlet if there are no downloads."""
        return len(self.downloads()) > 0

    def downloads(self):
        """Return a list of images and files, contained in the context object.
        """
        catalog = getToolByName(self.context, 'portal_catalog')
        return catalog(
            path={'query': '/'.join(self.context.getPhysicalPath()),
                  'depth': 1},
            portal_type=('File', 'Image',),
            sort_on='getObjPositionInParent')


class AddForm(base.NullAddForm):
    """Portlet add form."""

    def create(self):
        return Assignment()
