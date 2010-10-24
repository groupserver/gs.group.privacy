#coding: utf-8
'''Change the Basic Privacy Settings of a GroupServer Group
'''
# TODO: Move GSGroupJoining here
from Products.GSGroup.interfacesprivacy import IGSGroupBasicPrivacySettings
from Products.GSGroup.joining import GSGroupJoining
from Products.GSGroup.utils import clear_visibility_cache
from interfaces import IGSGroupVisibility

ACI = 'Access contents information'
EVERYONE = ['Anonymous', 'Authenticated', 'DivisionMember',
            'DivisionAdmin', 'GroupAdmin', 'GroupMember', 'Manager', 
            'Owner']
GROUP = ['DivisionAdmin', 'GroupAdmin', 'GroupMember', 'Manager', 
         'Owner']


class GSGroupChangeBasicPrivacy(object):

    def __init__(self, groupInfo):
        self.groupInfo = groupInfo

    @property
    def groupVisibility(self):
        return IGSGroupVisibility(self.groupInfo)

    def set_group_public(self):
        self.set_group_visibility(EVERYONE)
        self.set_messages_visibility(EVERYONE)
        self.set_files_visibility(EVERYONE)
        self.set_members_visibility(EVERYONE)
        self.set_joinability_anyone()
        assert self.groupVisibility.isPublic, \
            'Visibility of %s (%s) is %s, not public' % \
            (self.groupInfo.name, self.groupInfo.id, vis)
        
    def set_group_private(self):
        self.set_group_visibility(EVERYONE)
        self.set_messages_visibility(GROUP)
        self.set_files_visibility(GROUP)
        self.set_members_visibility(GROUP)
        self.set_joinability_request()
        assert self.groupVisibility.isPrivate, \
            'Visibility of %s (%s) is %s, not private' % \
            (self.groupInfo.name, self.groupInfo.id, vis)

    def set_group_secret(self):
        self.set_group_visibility(GROUP)
        self.set_messages_visibility(GROUP)
        self.set_files_visibility(GROUP)
        self.set_members_visibility(GROUP)
        self.set_joinability_invite()
        assert self.groupVisibility.isSecret, \
            'Visibility of %s (%s) is %s, not secret' % \
            (self.groupInfo.name, self.groupInfo.id, vis)

    def set_group_visibility(self, roles):
        assert type(roles) == list
        assert self.groupInfo
        assert self.groupInfo.groupObj
        # TODO: Audit
        group = self.groupInfo.groupObj
        group.manage_permission('View', roles)
        group.manage_permission(ACI, roles)
        clear_visibility_cache(group)
    
    def set_messages_visibility(self, roles):
        assert type(roles) == list
        assert self.groupInfo
        assert self.groupInfo.groupObj
        assert self.groupInfo.groupObj.messages
        # TODO: Audit
        messages = self.groupInfo.groupObj.messages
        messages.manage_permission('View', roles)
        messages.manage_permission(ACI, roles)
        clear_visibility_cache(messages)
        
    def set_files_visibility(self, roles):
        assert self.groupInfo
        assert self.groupInfo.groupObj
        assert self.groupInfo.groupObj.files
        # TODO: Audit
        files = self.groupInfo.groupObj.files
        files.manage_permission('View', roles)
        files.manage_permission(ACI, roles)
        clear_visibility_cache(files)
    
    def set_members_visibility(self, roles):
        assert self.groupInfo
        assert self.groupInfo.groupObj
        # TODO: Audit
        if hasattr(self.groupInfo.groupObj, 'members'):
            members = self.groupInfo.groupObj.members
            members.manage_permission('View', roles)
            members.manage_permission(ACI, roles)
            clear_visibility_cache(members)
        
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
        assert self.joinability == 'request', 'Joinability not set to request'
        # TODO: Audit

    def set_joinability_invite(self):
        self.__set_list_subscribe('')
        self.__set_grp_invite('invite')
        assert self.joinability == 'invite', 'Joinability not set to invite'
        # TODO: Audit

    def __set_list_subscribe(self, val):
        mailingList = getattr(self.groupInfo.groupObj.ListManager, self.groupInfo.id)
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

