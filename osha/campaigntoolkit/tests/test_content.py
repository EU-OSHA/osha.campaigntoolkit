# -*- coding: utf-8 -*-
"""Test the Osha Campaign Toolkit content types."""

from osha.campaigntoolkit.tests.base import IntegrationTestCase
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID

import unittest2 as unittest


class TestContent(IntegrationTestCase):
    """Test osha.campaigntoolkit content types."""

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']

    def test_hierarchy(self):
        """Ensure that we can create the various content types without error.
        """
        setRoles(self.portal, TEST_USER_ID, ('Manager',))

        self.portal.invokeFactory(
            'osha.campaigntoolkit.toolexample',
            'hammer',
            title=u'Hammer',
            text=u'A hammer is a tool meant to deliver an impact to an object'
        )


def test_suite():
    """This sets up a test suite that actually runs the tests in the class
    above."""
    return unittest.defaultTestLoader.loadTestsFromName(__name__)
