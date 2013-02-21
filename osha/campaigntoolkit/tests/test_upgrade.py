# -*- coding: utf-8 -*-
"""Test Osha Campaign Toolkit upgrades."""

from osha.campaigntoolkit.tests.base import IntegrationTestCase
from plone import api
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.app.textfield.value import RichTextValue

import unittest2 as unittest


class TestUpgrade001to002(IntegrationTestCase):
    """Test migration to ToolExample objects."""

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        self._create_content()

    def _create_content(self):
        """Create content for testing - two folders, one normal page and one
        'ToolExample' page.

        portal
         |--> page1
         |--> tools
               |--> folder2
                     |--> facebook-osha

        """
        setRoles(self.portal, TEST_USER_ID, ('Manager',))

        self.portal.invokeFactory('Folder', 'tools')
        self.portal.invokeFactory('Document', 'page1')
        self.portal['tools'].invokeFactory('Folder', 'folder2')
        self.portal['tools']['folder2'].invokeFactory(
            'Document',
            'facebook-osha',
            title='Facebook for EU-OSHA photo competition',
            text=u'<dl> <dt>Organisation</dt> <dd>EU-OSHA</dd><dt>Country'
            '</dt> <dd>International</dd> <dt>Description</dt> <dd><b>'
            'Facebook</b> page of the EU-OSHA photo competition</dd> '
            '<dt>Link</dt> <dd>'
            '<a href="https://www.facebook.com/euoshaphotocompetition">'
            'https://www.facebook.com/euoshaphotocompetition"</a></dd>'
            '</dl>'
        )

    def test_upgrade(self):
        """Test migration of pages to toolexamples."""
        from osha.campaigntoolkit.upgrades import upgrade_001_to_002

        # Run the migration
        upgrade_001_to_002.upgrade(self.portal)
        page = self.portal['page1']
        toolexample = self.portal['tools']['folder2']['facebook-osha']

        # The normal page should stay as it was
        self.assertEqual(page.portal_type, 'Document')

        # The 'ToolExample' page should be migrated to ToolExample
        self.assertEqual(toolexample.portal_type,
                         'osha.campaigntoolkit.toolexample')
        self.assertEqual(toolexample.id,
                         'facebook-osha')
        self.assertEqual(toolexample.title,
                         'Facebook for EU-OSHA photo competition')
        self.assertEqual(
            toolexample.text.output,
            u'<dl> <dt>Organisation</dt> <dd>EU-OSHA</dd><dt>Country'
            '</dt> <dd>International</dd> <dt>Description</dt> <dd><b>'
            'Facebook</b> page of the EU-OSHA photo competition</dd> '
            '<dt>Link</dt> <dd>'
            '<a href="https://www.facebook.com/euoshaphotocompetition">'
            'https://www.facebook.com/euoshaphotocompetition"</a></dd>'
            '</dl>')

        # The .tmp object shouldn't be there
        self.assertEquals(self.portal['tools']['folder2'].keys(),
                          ['facebook-osha'])


class TestUpgrade003to004(IntegrationTestCase):
    """Test migration of index pages from ToolExample objects to Documents.
    """

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        self._create_content()

    def _create_content(self):
        """Create content for testing - two folders, one normal tool example
        and one tool example that is set as default view for the folder.

        portal
         |--> tool1
         |--> folder1
               |--> folder2
                     |--> tool2 (set as default view for folder2)

        """
        setRoles(self.portal, TEST_USER_ID, ('Manager',))

        self.folder1 = api.content.create(
            container=self.portal, type='Folder', id='folder1')
        self.tool1 = api.content.create(
            container=self.portal,
            type='osha.campaigntoolkit.toolexample',
            id='tool1'
        )
        self.folder2 = api.content.create(
            container=self.folder1, type='Folder', id='folder2')
        self.tool2 = api.content.create(
            container=self.folder2,
            type='osha.campaigntoolkit.toolexample',
            id='tool2',
            title='Facebook for EU-OSHA photo competition',
            text=RichTextValue(
                u'<dl> <dt>Organisation</dt> <dd>EU-OSHA</dd><dt>Country'
                '</dt> <dd>International</dd> <dt>Description</dt> <dd><b>'
                'Facebook</b> page of the EU-OSHA photo competition</dd> '
                '<dt>Link</dt> <dd>'
                '<a href="https://www.facebook.com/euoshaphotocompetition">'
                'https://www.facebook.com/euoshaphotocompetition"</a></dd>'
                '</dl>'
            )
        )
        self.folder2.default_page = self.tool2.id

    def test_migrate_index_pages(self):
        """Test migration of pages to toolexamples."""
        from osha.campaigntoolkit.upgrades.upgrade_003_to_004 import \
            migrate_index_pages

        # migrate pages
        migrate_index_pages()
        tool1 = self.portal['tool1']
        tool2 = self.folder2['tool2']

        # The normal toolexample should stay as it was
        self.assertEqual(
            tool1.portal_type, 'osha.campaigntoolkit.toolexample')

        # The ToolExample index page should be migrated to a Document
        self.assertEqual(tool2.portal_type, 'Document')
        self.assertEqual(tool2.id, 'tool2')
        self.assertEqual(tool2.title, 'Facebook for EU-OSHA photo competition')
        self.assertEqual(
            tool2.getText(),
            u'<dl> <dt>Organisation</dt> <dd>EU-OSHA</dd><dt>Country'
            '</dt> <dd>International</dd> <dt>Description</dt> <dd><b>'
            'Facebook</b> page of the EU-OSHA photo competition</dd> '
            '<dt>Link</dt> <dd>'
            '<a href="https://www.facebook.com/euoshaphotocompetition">'
            'https://www.facebook.com/euoshaphotocompetition"</a></dd>'
            '</dl>')
        self.assertEqual(len(self.folder2.keys()), 1)


def test_suite():
    """This sets up a test suite that actually runs the tests in the classes
    above."""
    return unittest.defaultTestLoader.loadTestsFromName(__name__)
