# -*- coding: utf-8 -*-
"""The ToolExample content type."""

from five import grok
from osha.campaigntoolkit import  _
from plone.app.textfield import RichText
from plone.app.dexterity.behaviors.exclfromnav import IExcludeFromNavigation
from plone.directives import dexterity, form
from plone.namedfile.field import NamedBlobImage
from plone.namedfile.interfaces import IImageScaleTraversable


class IToolExample(form.Schema, IImageScaleTraversable):
    """Definition of the ToolExample schema."""

    body = RichText(
        title=_(u"Body Text"),
        required=False
    )

    image = NamedBlobImage(
        title=_(u"Image"),
        required=False
    )


class ToolExample(dexterity.Container):
    """Example of a campaign tool."""
    grok.implements(IToolExample)


class View(grok.View):
    """Default view for the ToolExample"""
    grok.context(IToolExample)
    grok.require('zope2.View')


@form.default_value(field=IExcludeFromNavigation['exclude_from_nav'])
def exclude_from_nav_default(data):
    """Exclude ToolExample objects from navigation."""
    return data.request.URL.endswith('++add++osha.campaigntoolkit.toolexample')
