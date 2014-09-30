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
from __future__ import unicode_literals
from AccessControl.PermissionRole import rolesForPermissionOn
PERM_ODD = 0
PERM_ANN = 1
PERM_GRP = 2
PERM_SIT = 3


def get_visibility(instance):
    retval = PERM_ODD
    roles = rolesForPermissionOn('View', instance)
    if (('Anonymous' in roles) and ('Authenticated' in roles)):
        retval = PERM_ANN
    elif ('DivisionMember' in roles):
        retval = PERM_SIT
    elif ('GroupMember' in roles):
        retval = PERM_GRP
    assert type(retval) == int
    assert retval in (PERM_ODD, PERM_ANN, PERM_SIT, PERM_GRP)
    return retval
