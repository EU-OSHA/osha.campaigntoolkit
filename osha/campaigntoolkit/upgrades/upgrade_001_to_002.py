# -*- coding: utf-8 -*-
"""Upgrade from version 001 to version 002."""

from Acquisition import aq_inner
from Acquisition import aq_parent
from plone.app.textfield.value import RichTextValue
from Products.CMFCore.utils import getToolByName
from zope.app.component.hooks import getSite

import transaction
import logging

logger = logging.getLogger('osha.campaigntoolkit.upgrades')


def upgrade(context):
    """Migrate all tool examples that were created as Pages to ToolExample
    objects.
    """
    portal = getSite()
    catalog = getToolByName(portal, 'portal_catalog')
    path = portal.getPhysicalPath()
    path = "/".join(path) + '/tools'
    pages = catalog(portal_type='Document', path=path)

    logger.info('Starting migration of pages to ToolExample objects...')

    for page in pages:
        page = aq_inner(page.getObject())
        text = page.getText()
        container = aq_parent(page)
        obj_id = page.getId()
        tmp_id = obj_id + '.tmp'
        rich_text = RichTextValue(text.decode('utf-8'), 'text/html',
                                  'text/x-html-safe', 'utf-8')

        logger.info('Migrating page at %s' % page.absolute_url())

        # Create a new toolexample with a temp id
        container.invokeFactory(
            type_name='osha.campaigntoolkit.toolexample',
            title=page.Title(),
            text=rich_text,
            id=tmp_id)

        # Delete the page
        del container[obj_id]

        # This is needed otherwise we get an error when renaming
        # See http://plone.293351.n2.nabble.com/File-object-migration-how-to-change-id-of-new-object-programatically-2-5-5-td4174543.html
        transaction.savepoint(1)

        # Rename the toolexample object
        container.manage_renameObject(tmp_id, obj_id)

    logger.info('Migration done.')
