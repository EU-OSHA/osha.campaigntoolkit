# -*- coding: utf-8 -*-
"""Upgrade from version 003 to version 004."""

from plone import api
from zope.globalrequest import getRequest


def upgrade(self):
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
                    text=default_page.text,
                    description=default_page.description,
                )

                default_page_id = default_page.id
                del folder[default_page_id]
                api.content.rename(
                    obj=new_default_page, new_id=default_page_id)
