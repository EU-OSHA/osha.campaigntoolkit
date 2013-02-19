# -*- coding: utf-8 -*-
"""Test Osha Campaign Toolkit views."""

from osha.campaigntoolkit.tests.base import IntegrationTestCase
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from Products.CMFCore.utils import getToolByName

import unittest2 as unittest


class TestToolExampleViews(IntegrationTestCase):
    """Test various methods, views and viewlets in browser/toolexample.py"""

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        self.portal_workflow = getToolByName(self.portal, 'portal_workflow')
        self._create_content()

    def _create_content(self):
        """Create content for testing."""
        setRoles(self.portal, TEST_USER_ID, ('Manager',))

        # Create a couple of tool examples and publish them
        self.portal['folder'].invokeFactory(
            'osha.campaigntoolkit.toolexample',
            'example1',
        )
        self.portal['folder'].invokeFactory(
            'osha.campaigntoolkit.toolexample',
            'example2',
        )
        self.portal['folder'].invokeFactory(
            'osha.campaigntoolkit.toolexample',
            'example3',
        )
        self.portal_workflow.setDefaultChain('simple_publication_workflow')
        self.portal_workflow.doActionFor(
            self.portal['folder']['example1'], 'publish')
        self.portal_workflow.doActionFor(
            self.portal['folder']['example2'], 'publish')
        self.portal_workflow.doActionFor(
            self.portal['folder']['example3'], 'publish')

        # Create some other objects as well
        self.portal['folder'].invokeFactory('Document', 'page1')
        self.portal['folder'].invokeFactory('Folder', 'folder1')

    def test_get_examples_no_limit(self):
        """Test get_examples method without a limit."""
        from osha.campaigntoolkit.browser.toolexample import get_examples

        examples = get_examples(self.portal.folder)

        self.assertEqual(len(examples), 3)
        self.assertEqual(examples[0].getId(), 'example1')
        self.assertEqual(examples[1].getId(), 'example2')
        self.assertEqual(examples[2].getId(), 'example3')

    def test_get_examples_with_limit(self):
        """Test get_examples method with a limit."""
        from osha.campaigntoolkit.browser.toolexample import get_examples

        examples = get_examples(self.portal.folder, limit=2)

        # We should get only the latest two examples
        self.assertEqual(len(examples), 2)
        self.assertEqual(examples[0].getId(), 'example3')
        self.assertEqual(examples[1].getId(), 'example2')


def test_suite():
    """This sets up a test suite that actually runs the tests in the classes
    above."""
    return unittest.defaultTestLoader.loadTestsFromName(__name__)
