# -*- coding: utf-8 -*-
# from Products.CMFPlone.interfaces import INonInstallable
# from zope.interface import implementer


# @implementer(INonInstallable)
# class HiddenProfiles(object):

#     def getNonInstallableProfiles(self):
#         """Hide uninstall profile from site-creation and quickinstaller."""
#         return [
#             'pas.plugins.owncloud:uninstall',
#         ]


# def post_install(context):
#     """Post install script"""
#     # Do something at the end of the installation of this package.


# def uninstall(context):
#     """Uninstall script"""
#     # Do something at the end of the uninstallation of this package.
from pas.plugins.owncloud.plugin import OwncloudHelper

TITLE = 'Owncloud PreAuth plugin (pas.plugins.owncloud)'


def isNotThisProfile(context):
    return context.readDataFile("owncloud_marker.txt") is None


def _addPlugin(pas, pluginid='owncloudpreauth'):
    installed = pas.objectIds()
    if pluginid in installed:
        return TITLE + " already installed."
    plugin = OwncloudHelper(pluginid, title=TITLE)
    pas._setObject(pluginid, plugin)
    plugin = pas[plugin.getId()]  # get plugin acquisition wrapped!
    for info in pas.plugins.listPluginTypeInfo():
        interface = info['interface']
        if not interface.providedBy(plugin):
            continue
        pas.plugins.activatePlugin(interface, plugin.getId())
        pas.plugins.movePluginsDown(
            interface,
            [x[0] for x in pas.plugins.listPlugins(interface)[:-1]],
        )


def setupPlugin(context):
    if isNotThisProfile(context):
        return
    site = context.getSite()
    pas = site.acl_users
    _addPlugin(pas)
