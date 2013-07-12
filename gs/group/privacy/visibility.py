# -*- coding: utf-8 -*-
# TODO: Move from Products.GSGroup to here
from Products.GSGroup.utils import get_visibility, PERM_ANN, PERM_GRP

ODD = 'odd'
PUBLIC = 'public'
PRIVATE = 'private'
SECRET = 'secret'


class GroupVisibility(object):

    def __init__(self, groupInfo):
        self.groupInfo = groupInfo

    @property
    def visibility(self):
        # TODO: Move to a utility
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
        elif ((msgsVis == PERM_GRP)
            and (filesVis == PERM_GRP)
            and (grpVis == PERM_ANN)):
            retval = PRIVATE
        elif ((msgsVis == PERM_GRP)
            and (filesVis == PERM_GRP)
            and (grpVis == PERM_GRP)):
            retval = SECRET

        assert type(retval) == str
        assert retval in [ODD, PUBLIC, PRIVATE, SECRET]
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
    def isOdd(self):
        retval = self.visibility == ODD
        assert type(retval) == bool
        return retval
