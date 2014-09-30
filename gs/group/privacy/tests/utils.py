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
import gs.group.privacy.utils  # lint:ok


class FauxGroup(object):
    'This is not a group'


class TestUtils(TestCase):

    @staticmethod
    def visibility_tester(v):
        with patch('gs.group.privacy.utils.rolesForPermissionOn') as rfpo:
            rfpo.return_value = v
            g = FauxGroup()
            retval = get_visibility(g)
        return retval

    def test_anon(self):
        v = ['Anonymous', 'Authenticated']
        r = self.visibility_tester(v)
        self.assertEqual(r, PERM_ANN)

    def test_anon_noauth(self):
        'Ensure that if we are not authenticated we do not have any perms'
        v = ['Anonymous']
        r = self.visibility_tester(v)
        self.assertEqual(r, PERM_ODD)

    def test_site_member(self):
        'Ensure that site members are seen as such'
        v = ['DivisionMember', 'EthylTheFrog']
        r = self.visibility_tester(v)
        self.assertEqual(r, PERM_SIT)

    def test_group_member(self):
        'Ensure that site members are seen as such'
        v = ['GroupMember', 'ToadTheWetSproket']
        r = self.visibility_tester(v)
        self.assertEqual(r, PERM_GRP)

    def test_odd(self):
        'Test that odd things are odd'
        v = ['Tonight we look a violence']
        r = self.visibility_tester(v)
        self.assertEqual(r, PERM_ODD)
