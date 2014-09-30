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
from zope.cachedescriptors.property import Lazy
from zope.interface import alsoProvides
from .utils import get_visibility, PERM_ANN, PERM_GRP, PERM_SIT
from .interfaces import (IPublic, IPublicToSiteMember, IPrivate, ISecret,
                         IOdd)
ODD = 'odd'
PUBLIC = 'public'
PRIVATE = 'private'
SECRET = 'secret'
SITE = 'site'


class GroupVisibility(object):

    interfaces = {
        PUBLIC: IPublic,
        SITE: IPublicToSiteMember,
        PRIVATE: IPrivate,
        SECRET: ISecret,
        ODD: IOdd}

    def __init__(self, groupInfo):
        self.groupInfo = groupInfo

        interface = self.interfaces[self.visibility]
        alsoProvides(self, interface)

    @Lazy
    def visibility(self):
        grp = self.groupInfo.groupObj
        msgs = getattr(grp, 'messages', None)
        msgsVis = get_visibility(msgs)
        files = getattr(grp, 'files', None)
        filesVis = get_visibility(files)
        grpVis = get_visibility(grp)

        retval = ODD
        if ((msgsVis == PERM_ANN)
                and (filesVis == PERM_ANN)
                and (grpVis == PERM_ANN)):
            retval = PUBLIC
        elif ((msgsVis == PERM_SIT)
                and (filesVis == PERM_SIT)
                and (grpVis == PERM_SIT)):
            retval = SITE
        elif ((msgsVis == PERM_GRP)
                and (filesVis == PERM_GRP)
                and (grpVis == PERM_ANN)):
            retval = PRIVATE
        elif ((msgsVis == PERM_GRP)
                and (filesVis == PERM_GRP)
                and (grpVis == PERM_GRP)):
            retval = SECRET

        assert retval in [ODD, PUBLIC, SITE, PRIVATE, SECRET]
        return retval

    @property
    def isSecret(self):
        retval = self.visibility == SECRET
        assert type(retval) == bool
        return retval

    @property
    def isPrivate(self):
        retval = self.visibility == PRIVATE
        assert type(retval) == bool
        return retval

    @property
    def isPublic(self):
        retval = self.visibility == PUBLIC
        assert type(retval) == bool
        return retval

    @property
    def isPublicToSite(self):
        retval = self.visibility == SITE
        assert type(retval) == bool
        return retval

    @property
    def isOdd(self):
        retval = self.visibility == ODD
        assert type(retval) == bool
        return retval
