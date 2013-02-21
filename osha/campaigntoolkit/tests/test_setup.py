# -*- coding: utf-8 -*-
"""Setup/installation tests for this package."""

from osha.campaigntoolkit.tests.base import IntegrationTestCase
from Products.CMFCore.utils import getToolByName

import unittest2 as unittest


class TestInstall(IntegrationTestCase):
    """Test installation of osha.campaigntoolkit into Plone."""

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        self.installer = getToolByName(self.portal, 'portal_quickinstaller')

    def test_product_installed(self):
        """Test if osha.campaigntoolkit is installed with
        portal_quickinstaller.
        """
        self.failUnless(self.installer.isProductInstalled(
            'osha.campaigntoolkit'))

    def test_uninstall(self):
        """Test if osha.campaigntoolkit is cleanly uninstalled."""
        self.installer.uninstallProducts(['osha.campaigntoolkit'])
        self.failIf(self.installer.isProductInstalled('osha.campaigntoolkit'))

    # actions.xml
    def test_site_actions(self):
        """Test if site actions have been set correctly."""
        site_actions = self.portal['portal_actions']['site_actions']

        self.assertEquals(
            site_actions['accessibility'].url_expr,
            'string:${globals_view/navigationRootUrl}/accessibility-info')
        self.assertEquals(site_actions['accessibility'].visible, True)

        self.assertEquals(
            site_actions['disclaimer'].url_expr,
            'string:http://osha.europa.eu/en/disclaimer')
        self.assertEquals(site_actions['disclaimer'].visible, True)

        self.assertEquals(
            site_actions['copyright'].url_expr,
            'string:${globals_view/navigationRootUrl}/copyright')
        self.assertEquals(site_actions['copyright'].visible, True)

        self.assertEquals(
            site_actions['contact'].url_expr,
            'string:${globals_view/navigationRootUrl}/contact-info')
        self.assertEquals(site_actions['contact'].visible, True)
        self.assertEquals(site_actions['contact'].title, 'Contact us')

    # Folder.xml
    def test_additional_views_for_folder(self):
        """Test that additional views are available in the Folder's display
        drop-down menu.
        """
        folder_views = self.portal.portal_types.Folder.view_methods
        self.assertIn('overview', folder_views)
        self.assertIn('readmore-view', folder_views)

        # test that default drop-down menu items are still there
        self.assertIn('folder_summary_view', folder_views)


def test_suite():
    """This sets up a test suite that actually runs the tests in the class
    above."""
    return unittest.defaultTestLoader.loadTestsFromName(__name__)
