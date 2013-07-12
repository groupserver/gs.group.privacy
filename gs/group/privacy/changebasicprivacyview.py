# -*- coding: utf-8 -*-
'''Change the Basic Privacy Settings of a GroupServer Group
'''
from zope.cachedescriptors.property import Lazy
from zope.component import createObject
from zope.formlib import form
from Products.Five.browser.pagetemplatefile import ZopeTwoPageTemplateFile
from Products.XWFCore.XWFUtils import get_the_actual_instance_from_zope
from gs.group.messages.post.postcontentprovider import GSPostContentProvider
from Products.GSGroup.interfacesprivacy import IGSGroupBasicPrivacySettings
from gs.content.form.radio import radio_widget
from gs.group.base import GroupForm
from interfaces import IGSChangePrivacy, IGSGroupVisibility


class GSGroupChangeBasicPrivacyForm(GroupForm):
    label = u'Change Group Privacy'
    pageTemplateFileName = 'browser/templates/change_basic_privacy.pt'
    template = ZopeTwoPageTemplateFile(pageTemplateFileName)

    def __init__(self, context, request):
        super(GSGroupChangeBasicPrivacyForm, self).__init__(context, request)
        self.__admin = self.__groupsInfo = None

    def setUpWidgets(self, ignore_request=False):
        vis = IGSGroupVisibility(self.groupInfo).visibility
        data = {'basicPrivacy': vis}
        self.widgets = form.setUpWidgets(
            self.form_fields, self.prefix, self.context,
            self.request, form=self, data=data,
            ignore_request=ignore_request)

    @Lazy
    def form_fields(self):
        retval = form.Fields(IGSGroupBasicPrivacySettings, render_context=False)
        retval['basicPrivacy'].custom_widget = radio_widget
        assert retval
        return retval

    @Lazy
    def groupsInfo(self):
        ctx = get_the_actual_instance_from_zope(self.context)
        retval = createObject('groupserver.GroupsInfo', ctx)
        assert retval
        return retval

    @form.action(label=u'Change', failure='handle_change_action_failure')
    def handle_change(self, action, data):
        assert self.context
        assert self.form_fields

        privacyController = IGSChangePrivacy(self.groupInfo)
        p = data['basicPrivacy']
        {'public': privacyController.set_group_public,
          'private': privacyController.set_group_private,
          'secret': privacyController.set_group_secret}[p]()
        m = u'Changed the privacy setting for {0} to <strong>{1}.</strong>'
        self.status = m.format(self.groupInfo.name, p)

        self.groupsInfo.clear_groups_cache()
        GSPostContentProvider.cookedTemplates.clear()
        assert self.status
        assert type(self.status) == unicode

    def handle_change_action_failure(self, action, data, errors):
        if len(errors) == 1:
            self.status = u'<p>There is an error:</p>'
        else:
            self.status = u'<p>There are errors:</p>'

    @Lazy
    def admin(self):
        usr = self.loggedInUser.user
        roles = usr.getRolesInContext(self.groupInfo.groupObj)
        # FIXME: Change to a permission denied error
        assert ('GroupAdmin' in roles) or ('DivisionAdmin' in roles), \
              '%s is not a group admin' % self.loggedInUser.id
        retval = self.loggedInUser
        assert retval
        return retval
