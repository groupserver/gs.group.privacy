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
# TODO: Move GSGroupJoining here
from __future__ import absolute_import, unicode_literals
from Products.GSGroup.joining import GSGroupJoining
from .interfaces import IGSGroupVisibility

ACI = 'Access contents information'

#: The roles we talk about when we say "Group member"
GROUP = ['DivisionAdmin', 'GroupAdmin', 'GroupMember', 'Manager',
         'Owner']

#: The roles involved when we talk about site members
SITE = ['DivisionMember', ] + GROUP

#: The roles involved when we talk about "Everyone"
EVERYONE = ['Anonymous', 'Authenticated', ] + SITE


class PermissionNotChanged(ValueError):
    'The permission was not changed'


class GSGroupChangeBasicPrivacy(object):

    def __init__(self, groupInfo):
        self.groupInfo = groupInfo

    @property
    def groupVisibility(self):
        retval = IGSGroupVisibility(self.groupInfo)
        return retval

    def get_error_msg(self, shouldBe):
        m = 'Visibility of {0} ({1}) is {2}, not {3}'
        retval = m.format(self.groupInfo.name, self.groupInfo.id,
                          self.groupVisibility.visibility, shouldBe)
        return retval

    def set_group_public(self):
        self.set_group_visibility(EVERYONE)
        self.set_messages_visibility(EVERYONE)
        self.set_files_visibility(EVERYONE)
        self.set_members_visibility(EVERYONE)
        self.set_joinability_anyone()

        if not self.groupVisibility.isPublic:
            msg = self.get_error_msg('public')
            raise PermissionNotChanged(msg)

    def set_group_private(self):
        self.set_group_visibility(EVERYONE)
        self.set_messages_visibility(GROUP)
        self.set_files_visibility(GROUP)
        self.set_members_visibility(GROUP)
        self.set_joinability_request()

        if not self.groupVisibility.isPrivate:
            msg = self.get_error_msg('private')
            raise PermissionNotChanged(msg)

    def set_group_restricted(self):
        self.set_group_visibility(SITE)
        self.set_messages_visibility(SITE)
        self.set_files_visibility(SITE)
        self.set_members_visibility(SITE)
        self.set_joinability_request()

        if not self.groupVisibility.isPublicToSite:
            msg = self.get_error_msg('restricted')
            raise PermissionNotChanged(msg)

    def set_group_secret(self):
        self.set_group_visibility(GROUP)
        self.set_messages_visibility(GROUP)
        self.set_files_visibility(GROUP)
        self.set_members_visibility(GROUP)
        self.set_joinability_invite()

        if not self.groupVisibility.isSecret:
            msg = self.get_error_msg('secret')
            raise PermissionNotChanged(msg)

    def set_group_visibility(self, roles):
        assert type(roles) == list
        assert self.groupInfo
        assert self.groupInfo.groupObj
        # TODO: Audit
        group = self.groupInfo.groupObj
        group.manage_permission('View', roles)
        group.manage_permission(ACI, roles)

    def set_messages_visibility(self, roles):
        assert type(roles) == list
        assert self.groupInfo
        assert self.groupInfo.groupObj
        assert self.groupInfo.groupObj.messages
        # TODO: Audit
        messages = self.groupInfo.groupObj.messages
        messages.manage_permission('View', roles)
        messages.manage_permission(ACI, roles)

    def set_files_visibility(self, roles):
        assert self.groupInfo
        assert self.groupInfo.groupObj
        assert self.groupInfo.groupObj.files
        # TODO: Audit
        files = self.groupInfo.groupObj.files
        files.manage_permission('View', roles)
        files.manage_permission(ACI, roles)

    def set_members_visibility(self, roles):
        assert self.groupInfo
        assert self.groupInfo.groupObj
        # TODO: Audit
        if hasattr(self.groupInfo.groupObj, 'members'):
            members = self.groupInfo.groupObj.members
            members.manage_permission('View', roles)
            members.manage_permission(ACI, roles)

    @property
    def joinability(self):
        retval = GSGroupJoining(self.groupInfo.groupObj).joinability
        return retval

    def set_joinability_anyone(self):
        self.__set_list_subscribe('subscribe')
        self.__set_grp_invite('')
        assert self.joinability == 'anyone', 'Joinability not set to anyone'
        # TODO: Audit

    def set_joinability_request(self):
        self.__set_list_subscribe('')
        self.__set_grp_invite('apply')
        assert self.joinability == 'request', \
            'Joinability not set to request'
        # TODO: Audit

    def set_joinability_invite(self):
        self.__set_list_subscribe('')
        self.__set_grp_invite('invite')
        assert self.joinability == 'invite', 'Joinability not set to invite'
        # TODO: Audit

    def __set_list_subscribe(self, val):
        mailingList = getattr(self.groupInfo.groupObj.ListManager,
                              self.groupInfo.id)
        if mailingList.hasProperty('subscribe'):
            mailingList.manage_changeProperties(subscribe=val)
        else:
            mailingList.manage_addProperty('subscribe', val, 'string')

        assert mailingList.getProperty('subscribe') == val, \
            'Subscribe property of the mailing list not set'
        # TODO: Audit

    def __set_grp_invite(self, val):
        grp = self.groupInfo.groupObj
        if grp.hasProperty('join_condition'):
            grp.manage_changeProperties(join_condition=val)
        else:
            grp.manage_addProperty('join_condition', val, 'string')

        assert grp.getProperty('join_condition') == val, \
            'Join condition of the group not set'
        # TODO: Audit
