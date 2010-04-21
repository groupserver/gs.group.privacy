# coding=utf-8
from zope.component import createObject, provideAdapter, adapts
from zope.pagetemplate.pagetemplatefile import PageTemplateFile
from zope.contentprovider.interfaces import UpdateNotCalled
from zope.interface import Interface, implements
from zope.publisher.interfaces.browser import IDefaultBrowserLayer
from AccessControl.PermissionRole import rolesForPermissionOn
from interfaces import IGSGroupPrivacyContentProvider

class Views(object):
    def __init__(self, instance):
        roles = rolesForPermissionOn('View', instance)
        self.anon = 'Anonymous' in roles
        self.siteMember = 'DivisionMember' in roles
        
        self.siteMemberOnly = not(self.anon) and self.siteMember
        self.groupMemberOnly = not(self.anon or self.siteMember)
        
        # --=mpj17=-- I am tempted to assert that the GroupMember has
        #   the view role, but I won't.
        assert type(self.anon) == bool
        assert type(self.siteMember) == bool
        
class GroupPrivacyContentProvider(object):

    implements( IGSGroupPrivacyContentProvider )
    adapts(Interface,
        IDefaultBrowserLayer,
        Interface)
    
    def __init__(self, context, request, view):
        self.__parent__ = self.view = view
        self.__updated = False

        self.context = context
        self.request = request
        
    def update(self):
        self.__updated = True

        self.groupInfo = createObject('groupserver.GroupInfo', 
          self.context, self.groupId)

        group = self.groupInfo.groupObj
        self.groupView = Views(group)
        messages = getattr(group, 'messages')
        self.messagesView = Views(messages)

        if self.groupView.anon and self.messagesView.anon:
            self.groupType = u'public'
        elif self.groupView.anon and not(self.messagesView.anon):
            self.groupType = u'private'
        elif not(self.groupView.anon):
            self.groupType = u'secret'
        else:
            self.groupType = u'specialised'
            
    def render(self):
        if not self.__updated:
            raise UpdateNotCalled

        pageTemplate = PageTemplateFile(self.pageTemplateFileName)
        return pageTemplate(view=self)
        
    #########################################
    # Non standard methods below this point #
    #########################################

