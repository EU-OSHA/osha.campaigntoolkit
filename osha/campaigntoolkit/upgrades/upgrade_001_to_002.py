# -*- coding: utf-8 -*-
"""Upgrade from version 001 to version 002."""

from Products.CMFCore.utils import getToolByName


def upgrade(context):
    """Upgrade steps from 001 to 002."""
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
