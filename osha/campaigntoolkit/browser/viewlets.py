# -*- coding: utf-8 -*-

from five import grok
from gomobiletheme.basic import viewlets as gomobileviewlets
from plone.app.layout.viewlets.common import ViewletBase
from zope.interface import Interface

from osha.campaigntoolkit.browser.interfaces import IMobileCampaignToolkitLayer

grok.templatedir("templates_mobile")


class GoogletranslateViewlet(ViewletBase):
    pass


class GotocorporateViewlet(ViewletBase):
    pass


# Mobile viewlets

class AdditionalHead(gomobileviewlets.AdditionalHead):
    grok.template('additionalhead')
    grok.layer(IMobileCampaignToolkitLayer)
    grok.context(Interface)
    grok.viewletmanager(gomobileviewlets.MainViewletManager)


class Logo(gomobileviewlets.Logo):
    grok.layer(IMobileCampaignToolkitLayer)
    grok.context(Interface)
    grok.viewletmanager(gomobileviewlets.MainViewletManager)

    def getLogoPath(self):
        return "++resource++osha.campaigntoolkit.resources/logo.gif"


class FooterText(gomobileviewlets.FooterText):
    grok.template('footertext')
    grok.layer(IMobileCampaignToolkitLayer)
    grok.context(Interface)
    grok.viewletmanager(gomobileviewlets.MainViewletManager)


class Header(gomobileviewlets.Header):
    grok.template('header')
    grok.layer(IMobileCampaignToolkitLayer)
    grok.context(Interface)
    grok.viewletmanager(gomobileviewlets.MainViewletManager)
