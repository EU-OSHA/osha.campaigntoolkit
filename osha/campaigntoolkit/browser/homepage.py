from Products.Five.browser import BrowserView
from zope.interface import implements
from Products.Archetypes.interfaces.base import IBaseContent, IBaseFolder
from Products.Archetypes.utils import OrderedDict
from Products.ATContentTypes.interface.image import IATImage
from Products.CMFCore.utils import getToolByName
from DateTime import DateTime
from Acquisition import aq_parent, aq_inner, aq_base
from plone.memoize.instance import memoize


class HomepageView(BrowserView):


    def __call__(self):
        return self.index()