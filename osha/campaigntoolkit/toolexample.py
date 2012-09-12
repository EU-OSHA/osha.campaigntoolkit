# -*- coding: utf-8 -*-
"""The ToolExample content type."""

from five import grok
from osha.campaigntoolkit import  _
from plone.directives import dexterity, form
from plone.namedfile.interfaces import IImageScaleTraversable
from zope import schema


class IToolExample(form.Schema, IImageScaleTraversable):
    """Definition of the ToolExample schema."""

    organisation = schema.TextLine(
        title=_(u"Organisation"),
        description=_(u"Please enter the organisation."),
    )

    country = schema.TextLine(
        title=_(u"Country"),
        description=_(u"Please enter the country."),
    )

    link = schema.URI(
        title=_(u"Link"),
        description=_(u"Please enter the link to the tool example."),
    )


class ToolExample(dexterity.Container):
    """Example of a campaign tool."""
    grok.implements(IToolExample)


class View(grok.View):
    """Default view for the ToolExample"""
    grok.context(IToolExample)
    grok.require('zope2.View')
