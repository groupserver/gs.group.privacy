# -*- coding: utf-8 -*-
############################################################################
#
# Copyright © 2014, 2015 OnlineGroups.net and Contributors.
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
from zope.component import createObject
from zope.formlib import form
from Products.Five.browser.pagetemplatefile import ZopeTwoPageTemplateFile
from Products.XWFCore.XWFUtils import get_the_actual_instance_from_zope
# from gs.group.messages.post.base.postcontentprovider import GSPostContentProvider
from gs.content.form.base import radio_widget
from gs.group.base import GroupForm
from .interfaces import IGSChangePrivacy, IGSGroupVisibility, IGroupPrivacySettings
from . import GSMessageFactory as _


class GSGroupChangeBasicPrivacyForm(GroupForm):
    label = _('Change group privacy')
    pageTemplateFileName = 'browser/templates/change_basic_privacy.pt'
    template = ZopeTwoPageTemplateFile(pageTemplateFileName)

    def __init__(self, context, request):
        super(GSGroupChangeBasicPrivacyForm, self).__init__(context, request)

    def setUpWidgets(self, ignore_request=False):
        vis = IGSGroupVisibility(self.groupInfo).visibility
        data = {'privacy': vis}
        self.widgets = form.setUpWidgets(
            self.form_fields, self.prefix, self.context,
            self.request, form=self, data=data,
            ignore_request=ignore_request)

    @Lazy
    def form_fields(self):
        retval = form.Fields(IGroupPrivacySettings,
                             render_context=False)
        retval['privacy'].custom_widget = radio_widget
        assert retval
        return retval

    @Lazy
    def groupsInfo(self):
        ctx = get_the_actual_instance_from_zope(self.context)
        retval = createObject('groupserver.GroupsInfo', ctx)
        assert retval
        return retval

    @form.action(label='Change', name='change',
                 failure='handle_change_action_failure')
    def handle_change(self, action, data):
        assert self.context
        assert self.form_fields

        privacyController = IGSChangePrivacy(self.groupInfo)
        p = data['privacy']
        {'public': privacyController.set_group_public,
         'private': privacyController.set_group_private,
         'site': privacyController.set_group_restricted,
         'secret': privacyController.set_group_secret}[p]()
        m = 'Changed the privacy setting for {0} to <strong>{1}.</strong>'
        self.status = m.format(self.groupInfo.name, p)

        self.groupsInfo.clear_groups_cache()
        # GSPostContentProvider.cookedTemplates.clear()
        assert self.status

    def handle_change_action_failure(self, action, data, errors):
        if len(errors) == 1:
            self.status = '<p>There is an error:</p>'
        else:
            self.status = '<p>There are errors:</p>'

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
