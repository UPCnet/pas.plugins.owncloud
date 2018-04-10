# -*- coding: utf-8 -*-
"""Module where all interfaces, events and exceptions live."""

from zope.interface import Interface


class IOwncloudHelper(Interface):
    """Interface for OwncloudHelper."""


class IPreauthTask(Interface):
    """Interface for pre auth tasks"""

    def execute(credentials):
        """The method to execute before the user gets authenticated"""
