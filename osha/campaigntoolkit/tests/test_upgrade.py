# -*- coding: utf-8 -*-
"""Test Osha Campaign Toolkit upgrades."""

from osha.campaigntoolkit.tests.base import IntegrationTestCase
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID

import unittest2 as unittest


class TestMigratePagesToToolExample(IntegrationTestCase):
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

    def test_upgrade_001_to_002(self):
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


def test_suite():
    """This sets up a test suite that actually runs the tests in the classes
    above."""
    return unittest.defaultTestLoader.loadTestsFromName(__name__)
