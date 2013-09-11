# -*- coding: utf-8 -*-
from five import grok
from zope.interface import Interface
from plone.theme.interfaces import IDefaultPloneLayer
from gomobiletheme.basic.interfaces import IThemeLayer as IGomobileThemeLayer


class ICanShowToolExamples(Interface):
    """Marker interface for content that can display the ToolExamples
    viewlet.
    """


class ICampaignToolkitLayer(IDefaultPloneLayer):
    """Marker interface that defines a Zope 3 browser layer."""


class IMobileCampaignToolkitLayer(IGomobileThemeLayer):
    """Marker interface for the mobile browser layer."""
