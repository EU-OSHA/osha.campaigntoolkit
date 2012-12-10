# -*- coding: utf-8 -*-
from zope.interface import Interface
from plone.theme.interfaces import IDefaultPloneLayer


class ICanShowToolExamples(Interface):
    """Marker interface for content that can display the ToolExamples
    viewlet.
    """


class ICampaignToolkitLayer(IDefaultPloneLayer):
    """Marker interface that defines a Zope 3 browser layer."""
