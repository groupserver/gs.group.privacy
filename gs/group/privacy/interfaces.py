# -*- coding: utf-8 -*-
##############################################################################
#
# Copyright © 2014 OnlineGroups.net and Contributors.
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#
###############################################################################
from __future__ import absolute_import, unicode_literals
from zope.interface import Interface
from zope.contentprovider.interfaces import IContentProvider
from zope.schema import ASCIILine, Text, Bool


class IGSGroupPrivacyContentProvider(IContentProvider):
    groupId = ASCIILine(title='Group Identifier',
        description='The identifier for the group',
        required=True)

    pageTemplateFileName = Text(title="Page Template File Name",
        description='The name of the ZPT file that is used to '
            'render the status message.',
        required=False,
        default="browser/templates/groupprivacycontentprovider.pt")


class IGSChangePrivacy(Interface):
    def set_group_public():
        pass

    def set_group_private():
        pass

    def set_group_secret():
        pass


class IGSGroupVisibility(Interface):
    visibility = ASCIILine(title='Visibility',
        description='The visibility of the group')

    isPublic = Bool(title='Is Public',
        description='True if the group is public')

    isPrivate = Bool(title='Is Private',
        description='True if the group is private')

    isSecret = Bool(title='Is Secret',
        description='True if the group is secret')

    isOdd = Bool(title='Is Odd',
        description='True if the group is not public, private or secret')
