# -*- coding: utf-8 -*-
"""Test Osha Campaign Toolkit upgrades."""

from osha.campaigntoolkit.tests.base import IntegrationTestCase
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from Products.CMFCore.utils import getToolByName

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

    def test_upgrade_exists(self):
        """Test if the migrate_pages_to_toolexamples upgrade exists."""
        portal_setup = getToolByName(self.portal, 'portal_setup')
        upgrades = portal_setup.listUpgrades(
            'osha.campaigntoolkit:default')
        self.assertEqual(
            upgrades[0]['title'],
            'Migrate pages to ToolExample objects')

    def test_migrate_pages_to_toolexamples(self):
        """Test the upgrade."""
        from osha.campaigntoolkit.upgrade import migrate_pages_to_toolexample

        # Run the migration
        migrate_pages_to_toolexample(self.portal)
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
