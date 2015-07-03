# -*- coding: utf-8 -*-
############################################################################
#
# Copyright © 2014, 2015 OnlineGroups.net and Contributors.
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
from zope.schema import ASCIILine, Text, Bool, Choice
from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm


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
    'Adaptors that change the group privacy implement this interface'

    def set_group_public():
        'Make the group a *public* group.'

    def set_group_private():
        'Make the group a *private* group.'

    def set_group_restricted():
        'Make the group a *restricted* group.'

    def set_group_secret():
        'Make the group a *secret* group.'


class IGSGroupVisibility(Interface):
    '''The base-class of the more specific visibility interfaces'''
    visibility = ASCIILine(
        title='Visibility',
        description='The visibility of the group')

    isPublic = Bool(
        title='Is Public',
        description='True if the group is public')

    isPrivate = Bool(
        title='Is Private',
        description='True if the group is private')

    isPublicToSite = Bool(
        title='Is restricted (public to site members)',
        description='True if the group is restricted to site members')

    isSecret = Bool(
        title='Is Secret',
        description='True if the group is secret')

    isOdd = Bool(
        title='Is Odd',
        description='True if the group is not public, private or secret')


# Interfaces for the four group visibilities. The group-visibility class
# will have one of these.


class IPublic(IGSGroupVisibility):
    '''This is a public group; anyone can view the group, and anyone can
view the posts.'''


class IPublicToSiteMember(IGSGroupVisibility):
    '''This is a public group, if (and only if) you are an existing site
member.'''


class IPrivate(IGSGroupVisibility):
    '''This is a private group, so you must be a member to view the posts,
but anyone can see the group.'''


class ISecret(IGSGroupVisibility):
    '''Only group members can see the group and the posts.'''


class IOdd(IGSGroupVisibility):
    '''The group does not fit into a category.'''


secruityVocab = SimpleVocabulary([
    SimpleTerm(
        'public', 'public',
        'Public: Everyone can view the group, view the posts, and '
        'join the group.'),
    SimpleTerm(
        'private', 'private',
        'Private: Everyone can view the group, but only group members '
        'can view the posts. Anyone can request to become a member.'),
    SimpleTerm(
        'site', 'site',
        'Restricted: All site members can view the group and posts. '
        'Anyone can request to become a member.'),
    SimpleTerm(
        'secret', 'secret',
        'Secret: Only group members can view the group and posts. '
        'People must be invited to join the group.'), ])


class IGroupPrivacySettings(Interface):
    'The schema for the Change privacy form'
    privacy = Choice(
        title='Group privacy',
        description='This setting determines who can view the group, view '
                    'the posts made to the group, and join the group. Only '
                    'members of the group can add posts to the group.',
        vocabulary=secruityVocab,
        required=True)
