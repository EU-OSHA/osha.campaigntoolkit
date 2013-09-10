# -*- coding: utf-8 -*-
"""Upgrade from version 003 to version 004."""

from plone import api
import logging

logger = logging.getLogger('osha.policy.upgrades')


def upgrade(context):
    qi = api.portal.get_tool("portal_quickinstaller")

    # Install mobile packages
    for product in ("gomobile.mobile", "gomobiletheme.basic"):
        if not qi.isProductInstalled(product):
            logger.info("Installing Products.%s" % product)
            qi.installProduct(product)

    # Load mobile_properties
    context.runImportStepFromProfile(
        'profile-osha.campaigntoolkit:default', 'propertiestool')
