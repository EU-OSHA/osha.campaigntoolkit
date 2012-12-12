# -*- coding: utf-8 -*-
"""The ToolExample content type."""

from osha.campaigntoolkit import _
from plone.app.textfield import RichText
from plone.directives import dexterity, form
from plone.namedfile.field import NamedBlobImage
from plone.namedfile.interfaces import IImageScaleTraversable
from zope.interface import implements
from zope.schema import Bool


class IToolExample(form.Schema, IImageScaleTraversable):
    """Definition of the ToolExample schema."""

    text = RichText(
        title=_(u"Body Text"),
        required=False
    )

    image = NamedBlobImage(
        title=_(u"Image"),
        required=False
    )

    OSH_related = Bool(
        title=_(u"OSH related"),
        description=_(u"Check to display this item higher in the listings.")
    )


class ToolExample(dexterity.Container):
    """Example of a campaign tool."""
    implements(IToolExample)
