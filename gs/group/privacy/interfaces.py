# -*- coding: utf-8 -*-
from zope.interface import Interface
from zope.contentprovider.interfaces import IContentProvider
from zope.schema import *


class IGSGroupPrivacyContentProvider(IContentProvider):
    groupId = ASCIILine(title=u'Group Identifier',
        description=u'The identifier for the group',
        required=True)

    pageTemplateFileName = Text(title=u"Page Template File Name",
        description=u'The name of the ZPT file that is used to '
            u'render the status message.',
        required=False,
        default=u"browser/templates/groupprivacycontentprovider.pt")


class IGSChangePrivacy(Interface):
    def set_group_public():
        pass

    def set_group_private():
        pass

    def set_group_secret():
        pass


class IGSGroupVisibility(Interface):
    visibility = ASCIILine(title=u'Visibility',
        description=u'The visibility of the group')

    isPublic = Bool(title=u'Is Public',
        description=u'True if the group is public')

    isPrivate = Bool(title=u'Is Private',
        description=u'True if the group is private')

    isSecret = Bool(title=u'Is Secret',
        description=u'True if the group is secret')

    isOdd = Bool(title=u'Is Odd',
        description=u'True if the group is not public, private or secret')
