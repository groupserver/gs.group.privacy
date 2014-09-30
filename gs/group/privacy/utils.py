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

#: The object has an odd permission
PERM_ODD = 0

#: The object can be seen by the anonymous user
PERM_ANN = 1

#: The object can be seen by group members
PERM_GRP = 2

#: The object can be seen by site members
PERM_SIT = 3


def get_visibility(instance):
    '''Get the visibility for an object.

:param object instance: An instance of an object
:returns: The visibility of the object. It will be one of
          :const:`PERM_ODD`, :const:`PERM_ANN`, :const:`PERM_GRP`, or
          :const:`PERM_SIT`.
:rtype: int

The :func:`.get_visibility` function wraps the even-lower
:func:`AccessControl.PermissionRole.rolesForPermissionOn` function to
determine who can see an object.'''
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
