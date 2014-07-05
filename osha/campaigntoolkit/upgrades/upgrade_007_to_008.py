# -*- coding: utf-8 -*-
"""Upgrade from version 003 to version 004."""

from plone import api
from osha.campaigntoolkit.setuphandlers import _setup_password_policy


def upgrade(context):
    portal = api.portal.get()
    _setup_password_policy(portal)
