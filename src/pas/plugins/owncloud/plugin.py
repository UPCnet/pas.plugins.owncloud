"""Class: OwncloudHelper
"""

from AccessControl.SecurityInfo import ClassSecurityInfo
from App.class_init import default__class_init__ as InitializeClass

from Products.PluggableAuthService.plugins.BasePlugin import BasePlugin
from Products.PluggableAuthService.interfaces import plugins as pas_interfaces

from pas.plugins.owncloud.interfaces import IPreauthTask, IOwncloudHelper

import logging
from zope.interface import implements
from zope.component import getAdapters

from ulearn5.owncloud.utilities import IOwncloudClient
from zope.component import getUtility
from plone import api

logger = logging.getLogger('pas.plugins.owncloud')


class OwncloudHelper(BasePlugin):
    """PreAuth Multi-plugin"""
    meta_type = 'owncloud Helper'
    security = ClassSecurityInfo()

    implements(IOwncloudHelper, pas_interfaces.IAuthenticationPlugin)

    def __init__(self, id, title=None):
        self._setId(id)
        self.title = title

    security.declarePublic('authenticateCredentials')
    def authenticateCredentials(self, credentials):
        """credentials -> (userid, login)

        o 'credentials' will be a mapping, as returned by IExtractionPlugin.

        o Return a tuple consisting of user ID (which may be different
          from the login name) and login

        o If the credentials cannot be authenticated, return None.
        """
        user = credentials.get('login')
        password = credentials.get('password')

        if not (user and password):
            return None

        logger.debug('credentials: %s' % credentials)

        # Do the tasks defined by all the registered adapters for IPreauthTask
        tasks = list(getAdapters((self,), IPreauthTask))
        for name, task in tasks:
            # IPreauthTask adapters must implement execute method
            task.execute(credentials)

        owncloud = getUtility(IOwncloudClient)
        owncloud.create_new_connection(user, password)

        username = api.portal.get_registry_record('ulearn5.owncloud.controlpanel.IOCSettings.connector_username')
        password = api.portal.get_registry_record('ulearn5.owncloud.controlpanel.IOCSettings.connector_password')
        owncloud.create_new_connection_admin(username, password)

        # Ejemplo para utilizar la utility de owncloud
        # client = getUtility(IOwncloudClient)
        # valor = client.connection()
        # valor.list('Documents', depth=1)

        # Return None always
        return None


InitializeClass(OwncloudHelper)
