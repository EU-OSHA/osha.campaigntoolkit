# -*- coding: utf-8 -*-

from five import grok
from gomobiletheme.basic import viewlets as gomobileviewlets
from plone.app.layout.viewlets.common import ViewletBase
from zope.interface import Interface

from osha.campaigntoolkit.browser.interfaces import IMobileCampaignToolkitLayer

grok.templatedir("templates")


class GoogletranslateViewlet(ViewletBase):
    pass


class GotocorporateViewlet(ViewletBase):
    pass


class AdditionalHead(gomobileviewlets.AdditionalHead):
    grok.template('additionalhead')
    grok.layer(IMobileCampaignToolkitLayer)
    grok.context(Interface)
    grok.viewletmanager(gomobileviewlets.MainViewletManager)
