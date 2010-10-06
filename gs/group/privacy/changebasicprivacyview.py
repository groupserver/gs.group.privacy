#coding: utf-8
'''Change the Basic Privacy Settings of a GroupServer Group
'''
try:
    from Products.Five.formlib.formbase import PageForm
except ImportError:
    from five.formlib.formbase import PageForm
from zope.component import createObject
from zope.formlib import form
from Products.Five.browser.pagetemplatefile import ZopeTwoPageTemplateFile
from zope.app.form.browser import RadioWidget
from zope.app.form.browser.widget import renderElement
from Products.XWFCore.XWFUtils import get_the_actual_instance_from_zope
from Products.XWFMailingListManager.postContentProvider import \
  GSPostContentProvider
from Products.GSGroup.interfacesprivacy import IGSGroupBasicPrivacySettings
from Products.GSGroup.joining import GSGroupJoining
from Products.GSGroup.utils import clear_visibility_cache
from interfaces import IGSChangePrivacy, IGSGroupVisibility

# TODO: Move out
class NotBrokenRadioWidget(RadioWidget):
    _joinButtonToMessageTemplate = u'%s&nbsp;%s\n'
    def renderItem(self, index, text, value, name, cssClass):
        widgetId = '%s.%s' % (name, index)
        elem = renderElement(u'input',
                             type="radio",
                             cssClass=cssClass,
                             name=name,
                             id=widgetId,
                             value=value)
        label = '<label class="radioLabel" for="%s">%s</label>' % \
          (widgetId, text)
        return self._joinButtonToMessageTemplate % (elem, label)

    def renderSelectedItem(self, index, text, value, name, cssClass):
        """Render a selected item of the list."""
        widgetId = '%s.%s' % (name, index)
        elem = renderElement(u'input',
                             value=value,
                             name=name,
                             id=widgetId,
                             cssClass=cssClass,
                             checked="checked",
                             type='radio')
        label = '<label class="radioLabel" for="%s">%s</label>' % \
          (widgetId, text)
        return self._joinButtonToMessageTemplate % (elem, label)

def radio_widget(field, request):
    return NotBrokenRadioWidget(field,
                                field.vocabulary,
                                request)

class GSGroupChangeBasicPrivacyForm(PageForm):
    label = u'Change Group Privacy'
    pageTemplateFileName = 'browser/templates/change_basic_privacy.pt'
    template = ZopeTwoPageTemplateFile(pageTemplateFileName)

    def __init__(self, context, request):
        PageForm.__init__(self, context, request)
        self.siteInfo = createObject('groupserver.SiteInfo', context)
        groupInfo = self.groupInfo = \
          createObject('groupserver.GroupInfo', context)
        self.__admin = self.__groupsInfo = self.__formFields = None

    def setUpWidgets(self, ignore_request=False):
        vis = IGSGroupVisibility(self.groupInfo).visibility
        data = {'basicPrivacy': vis}
        self.widgets = form.setUpWidgets(
            self.form_fields, self.prefix, self.context,
            self.request, form=self, data=data,
            ignore_request=ignore_request)

    @property
    def form_fields(self):
        if self.__formFields == None:
            self.__formFields = form.Fields(IGSGroupBasicPrivacySettings,
                                  render_context=False)
            self.__formFields['basicPrivacy'].custom_widget = \
                radio_widget
        assert self.__formFields != None
        return self.__formFields

    @property
    def groupsInfo(self):
        if self.__groupsInfo == None:
            ctx = get_the_actual_instance_from_zope(self.context)
            self.__groupsInfo = createObject('groupserver.GroupsInfo', 
                                    ctx)
        assert self.__groupsInfo != None
        return self.__groupsInfo

    @form.action(label=u'Change', failure='handle_change_action_failure')
    def handle_change(self, action, data):
        assert self.context
        assert self.form_fields

        privacyController = IGSChangePrivacy(self.groupInfo)
        p = data['basicPrivacy']
        {
          'public':  privacyController.set_group_public,
          'private': privacyController.set_group_private,
          'secret':  privacyController.set_group_secret}[p]()
        self.status = u'TODO: I should set the status'
        
        self.groupsInfo.clear_groups_cache()
        GSPostContentProvider.cookedTemplates.clear()
        GSPostContentProvider.cookedResult.clear()
        assert self.status
        assert type(self.status) == unicode

    def handle_change_action_failure(self, action, data, errors):
        if len(errors) == 1:
            self.status = u'<p>There is an error:</p>'
        else:
            self.status = u'<p>There are errors:</p>'
    @property
    def admin(self):
        if not(self.__admin):
            loggedInUser = createObject('groupserver.LoggedInUser',
                self.context)
            roles = loggedInUser.user.getRolesInContext(self.groupInfo.groupObj)
            assert ('GroupAdmin' in roles) or ('DivisionAdmin' in roles), \
              '%s is not a group admin' % loggedInUser
            self.__admin = loggedInUser
        assert self.__admin
        return self.__admin

