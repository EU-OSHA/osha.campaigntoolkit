# -*- coding: utf-8 -*-
"""Upgrade from version 003 to version 004."""

from plone import api
from zope.globalrequest import getRequest


def upgrade(context):
    """Upgrade from version 003 to version 004."""

    # Apply browser layer so z3c.jbot comes in effect
    context.runImportStepFromProfile(
        'profile-osha.campaigntoolkit:default', 'browserlayer')

    # Import relevant import steps to make the 'Read more' view work - #6699
    context.runImportStepFromProfile(
        'profile-osha.campaigntoolkit:default',
        'typeinfo'
    )
    context.runImportStepFromProfile(
        'profile-osha.campaigntoolkit:default',
        'jsregistry'
    )

    migrate_index_pages()


def migrate_index_pages():
    """Convert index pages from Tool Examples to Documents."""
    catalog = api.portal.get_tool('portal_catalog')
    brains = catalog(portal_type='Folder')

    for b in brains:
        folder = b.getObject()

        default_page_helper = api.content.get_view(
            name='default_page',
            context=folder,
            request=getRequest()
        )
        page_name = default_page_helper.getDefaultPage(folder)

        if page_name:
            default_page = folder[page_name]

            if default_page.portal_type == 'osha.campaigntoolkit.toolexample':
                new_default_page = api.content.create(
                    container=folder,
                    type='Document',
                    title=default_page.title,
                    text=default_page.text.raw,
                    description=default_page.description,
                )

                default_page_id = default_page.id
                del folder[default_page_id]
                api.content.rename(
                    obj=new_default_page, new_id=default_page_id)
