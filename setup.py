# -*- coding: utf-8 -*-
############################################################################
#
# Copyright © 2010, 2011, 2012, 2013, 2014 OnlineGroups.net and
# Contributors.
#
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
import codecs
import os
from setuptools import setup, find_packages
from version import get_version

version = get_version()

with codecs.open('README.rst', encoding='utf-8') as f:
    long_description = f.read()
with codecs.open(os.path.join("docs", "HISTORY.rst"),
                 encoding='utf-8') as f:
    long_description += '\n' + f.read()

setup(
    name='gs.group.privacy',
    version=version,
    description="GroupServer group-privacy settings",
    long_description=long_description,
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        "Environment :: Web Environment",
        "Framework :: Zope2",
        "Intended Audience :: Developers",
        'License :: OSI Approved :: Zope Public License',
        "Natural Language :: English",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: Implementation :: CPython",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    keywords='group, privacy, permissions, visibility',
    author='Michael JasonSmith',
    author_email='mpj17@onlinegroups.net',
    url='https://github.com/groupserver/gs.group.privacy/',
    license='ZPL 2.1',
    packages=find_packages(exclude=['ez_setup']),
    namespace_packages=['gs', 'gs.group'],
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'setuptools',
        'zope.browserpage',
        'zope.cachedescriptors',
        'zope.component',
        'zope.contentprovider',
        'zope.formlib',
        'zope.interface',
        'zope.pagetemplate',
        'zope.publisher',
        'zope.tal',
        'zope.tales',
        'zope.schema',
        'zope.viewlet',
        'AccessControl',
        'Zope2',
        'gs.content.form.base',
        'gs.content.layout',
        'gs.group.base',
        'gs.group.member.viewlet',  # For the link viewlet
        'gs.group.properties',  # For the link to the page
        'Products.GSGroup',
        'Products.XWFCore',
    ],
    extras_require={'docs': ['Sphinx']},
    test_suite="gs.group.privacy.tests.test_all",
    tests_require=['mock', ],
    entry_points="""
    # -*- Entry points: -*-
    """,)
