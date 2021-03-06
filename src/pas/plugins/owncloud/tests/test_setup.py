# -*- coding: utf-8 -*-
"""Setup tests for this package."""
from plone import api
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from pas.plugins.owncloud.testing import PAS_PLUGINS_OWNCLOUD_INTEGRATION_TESTING  # noqa

import unittest


class TestSetup(unittest.TestCase):
    """Test that pas.plugins.owncloud is properly installed."""

    layer = PAS_PLUGINS_OWNCLOUD_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        self.installer = api.portal.get_tool('portal_quickinstaller')

    def test_product_installed(self):
        """Test if pas.plugins.owncloud is installed."""
        self.assertTrue(self.installer.isProductInstalled(
            'pas.plugins.owncloud'))

    def test_browserlayer(self):
        """Test that IPasPluginsOwncloudLayer is registered."""
        from pas.plugins.owncloud.interfaces import (
            IPasPluginsOwncloudLayer)
        from plone.browserlayer import utils
        self.assertIn(
            IPasPluginsOwncloudLayer,
            utils.registered_layers())


class TestUninstall(unittest.TestCase):

    layer = PAS_PLUGINS_OWNCLOUD_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.installer = api.portal.get_tool('portal_quickinstaller')
        roles_before = api.user.get_roles(TEST_USER_ID)
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.installer.uninstallProducts(['pas.plugins.owncloud'])
        setRoles(self.portal, TEST_USER_ID, roles_before)

    def test_product_uninstalled(self):
        """Test if pas.plugins.owncloud is cleanly uninstalled."""
        self.assertFalse(self.installer.isProductInstalled(
            'pas.plugins.owncloud'))

    def test_browserlayer_removed(self):
        """Test that IPasPluginsOwncloudLayer is removed."""
        from pas.plugins.owncloud.interfaces import \
            IPasPluginsOwncloudLayer
        from plone.browserlayer import utils
        self.assertNotIn(
            IPasPluginsOwncloudLayer,
            utils.registered_layers())
