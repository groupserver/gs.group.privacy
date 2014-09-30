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
from functools import reduce
from mock import patch
from unittest import TestCase
from zope.interface import providedBy
from gs.group.privacy.interfaces import (IPublic, IPublicToSiteMember,
                                         IPrivate, ISecret, IOdd)
from gs.group.privacy.utils import (PERM_ANN, PERM_GRP, PERM_SIT)
from gs.group.privacy.visibility import (GroupVisibility, ODD, PUBLIC,
                                         PRIVATE, SECRET, SITE)
import gs.group.privacy.visibility  # lint:ok


class FauxGroup(object):
    'This is not a group'
    files = 'Durk'
    messages = 'Dinsdale'


class FauxGroupInfo(object):
    groupObj = FauxGroup()


class TestVisibility(TestCase):

    def assertHasInterface(self, obj, interface):
        m = '{0} fails to provide the interface {1}'
        msg = m.format(obj, interface)
        self.assertEqual([interface], list(providedBy(obj)), msg)

    def assertHighlander(self, v):
        '''Count how many of the ``GroupVisibility.is*`` methods return
``True``, and assert that the count is ``1``.'''
        truthyness = [v.isPublic, v.isPrivate, v.isSecret, v.isOdd,
                      v.isPublicToSite]
        c = reduce(lambda a, b: a + int(b), truthyness, False)
        self.assertEqual(1, c, 'There is more than one ({0})'.format(c))

    def test_public(self):
        perms = [PERM_ANN, PERM_ANN, PERM_ANN]
        f = FauxGroupInfo()
        with patch('gs.group.privacy.visibility.get_visibility') as gv:
            gv.side_effect = perms
            v = GroupVisibility(f)
            self.assertTrue(v.isPublic)
            self.assertHighlander(v)
            self.assertEqual(v.visibility, PUBLIC)
            self.assertHasInterface(v, IPublic)

    def test_private(self):
        perms = [PERM_GRP, PERM_GRP, PERM_ANN]
        f = FauxGroupInfo()
        with patch('gs.group.privacy.visibility.get_visibility') as gv:
            gv.side_effect = perms
            v = GroupVisibility(f)
            self.assertTrue(v.isPrivate)
            self.assertHighlander(v)
            self.assertEqual(v.visibility, PRIVATE)
            self.assertHasInterface(v, IPrivate)

    def test_secret(self):
        perms = [PERM_GRP, PERM_GRP, PERM_GRP]
        f = FauxGroupInfo()
        with patch('gs.group.privacy.visibility.get_visibility') as gv:
            gv.side_effect = perms
            v = GroupVisibility(f)
            self.assertTrue(v.isSecret)
            self.assertHighlander(v)
            self.assertEqual(v.visibility, SECRET)
            self.assertHasInterface(v, ISecret)

    def test_public_to_site(self):
        perms = [PERM_SIT, PERM_SIT, PERM_SIT]
        f = FauxGroupInfo()
        with patch('gs.group.privacy.visibility.get_visibility') as gv:
            gv.side_effect = perms
            v = GroupVisibility(f)
            self.assertTrue(v.isPublicToSite)
            self.assertHighlander(v)
            self.assertEqual(v.visibility, SITE)
            self.assertHasInterface(v, IPublicToSiteMember)

    def odd_test(self, perms):
        f = FauxGroupInfo()
        with patch('gs.group.privacy.visibility.get_visibility') as gv:
            gv.side_effect = perms
            v = GroupVisibility(f)
            self.assertTrue(v.isOdd)
            self.assertHighlander(v)
            self.assertEqual(v.visibility, ODD)
            self.assertHasInterface(v, IOdd)

    def test_odd_site(self):
        '''Test the odd situation of site-perms on messages and files, but
group-perms for everything below that.'''
        self.odd_test([PERM_SIT, PERM_SIT, PERM_GRP])

    def test_odd_ann(self):
        '''Test the odd situation of anonymous-perms on messages and files,
but group-perms for the group.'''
        self.odd_test([PERM_ANN, PERM_ANN, PERM_GRP])

    def test_odd_ann_site(self):
        '''Test the odd situation of anonymous-perms on messages and files,
but site-perms for the group.'''
        self.odd_test([PERM_ANN, PERM_ANN, PERM_SIT])
