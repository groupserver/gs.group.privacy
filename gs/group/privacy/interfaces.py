# -*- coding: utf-8 -*-
############################################################################
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
############################################################################
from __future__ import absolute_import, unicode_literals
from zope.interface import Interface
from zope.contentprovider.interfaces import IContentProvider
from zope.schema import ASCIILine, Text, Bool


class IGSGroupPrivacyContentProvider(IContentProvider):
    groupId = ASCIILine(
        title='Group Identifier',
        description='The identifier for the group',
        required=True)

    pageTemplateFileName = Text(
        title="Page Template File Name",
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
    visibility = ASCIILine(
        title='Visibility',
        description='The visibility of the group')

    isPublic = Bool(
        title='Is Public',
        description='True if the group is public')

    isPrivate = Bool(
        title='Is Private',
        description='True if the group is private')

    isSecret = Bool(
        title='Is Secret',
        description='True if the group is secret')

    isOdd = Bool(
        title='Is Odd',
        description='True if the group is not public, private or secret')


# Interfaces for the four group visibilities. The group-visibility class
# will have one of these.


class IPublic(IGSGroupVisibility):
    '''This is a public group that anyone can join, anyone can view the
group, and anyone can view the posts.'''


class IPublicToSiteMember(IGSGroupVisibility):
    '''This is a public group, if (and only if) you are an existing site
member. If you are a site member then you can join the group, view the
group, and view the posts.'''


class IPrivate(IGSGroupVisibility):
    '''This is a private group, so you must be a member to view the posts,
but anyone can see the group. People can request to be members.'''


class ISecret(IGSGroupVisibility):
    '''Only group members can see the group and the posts. People must be
invited to become members.'''


class IOdd(IGSGroupVisibility):
    '''The group does not fit into a category.'''
