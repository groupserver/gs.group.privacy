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
from mock import patch
from unittest import TestCase
from gs.group.privacy.utils import (get_visibility, PERM_ODD, PERM_ANN,
                                    PERM_GRP, PERM_SIT)
import gs.group.privacy.utils
from gs.group.list.command.tests.faux import FauxGroup


class FauxSiteInfo(object):
    name = 'An Example Site'
    id = 'example'


class FauxGroupInfo(object):
    name = 'An Example Group'
    id = 'example_group'
    siteInfo = FauxSiteInfo()


class FauxUserInfo(object):
    name = 'An Example user'
    id = 'exampleuser'


class TestUtils(TestCase):

    @patch.object(gs.group.privacy.utils, 'rolesForPermissionOn')
    def test_anon(self, mocked_rfpo):
        mocked_rfpo.return_value = ['Anonymous', 'Authenticated']
        g = FauxGroup()
        r = get_visibility(g)
        self.assertEqual(r, PERM_ANN)

    @patch.object(gs.group.privacy.utils, 'rolesForPermissionOn')
    def test_anon_noauth(self, mocked_rfpo):
        'Ensure that if we are not authenticated we do not have any perms'
        mocked_rfpo.return_value = ['Anonymous']
        g = FauxGroup()
        r = get_visibility(g)
        self.assertEqual(r, PERM_ODD)

    @patch.object(gs.group.privacy.utils, 'rolesForPermissionOn')
    def test_site_member(self, mocked_rfpo):
        'Ensure that site members are seen as such'
        mocked_rfpo.return_value = ['DivisionMember', 'EthylTheFrog']
        g = FauxGroup()
        r = get_visibility(g)
        self.assertEqual(r, PERM_SIT)

    @patch.object(gs.group.privacy.utils, 'rolesForPermissionOn')
    def test_group_member(self, mocked_rfpo):
        'Ensure that site members are seen as such'
        mocked_rfpo.return_value = ['GroupMember', 'ToadTheWetSproket']
        g = FauxGroup()
        r = get_visibility(g)
        self.assertEqual(r, PERM_GRP)
