# -*- coding: utf-8 -*-
"""Upgrade from version 002 to version 003."""

from Products.CMFCore.utils import getToolByName


def upgrade(context):
    """Remove 'Exclude from navigation' behavior from all Tool Example
    content types.
    """
    catalog = getToolByName(context, "portal_catalog")

    brains = catalog(portal_type="osha.campaigntoolkit.toolexample")
    for b in brains:
        obj = b.getObject()
        obj.exclude_from_nav = False
        obj.reindexObject()

    context.runImportStepFromProfile(
        'profile-osha.campaigntoolkit:default',
        'typeinfo'
    )

    context.runImportStepFromProfile(
        'profile-osha.campaigntoolkit:default',
        'catalog'
    )

    context.runImportStepFromProfile(
        'profile-osha.campaigntoolkit:default',
        'viewlets'
    )
