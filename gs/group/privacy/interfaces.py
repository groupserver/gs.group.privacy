# coding=utf-8
from zope.interface import Interface
from zope.schema import *

class IGSGroupPrivacyContentProvider( Interface ):
    groupId = ASCIILine(title=u'Group Identifier',
        description=u'The identifier for the group',
        required=True)

    pageTemplateFileName = Text(title=u"Page Template File Name",
        description=u'The name of the ZPT file that is used to '\
        u'render the status message.',
        required=False,
        default=u"browser/templates/groupprivacycontentprovider.pt")

