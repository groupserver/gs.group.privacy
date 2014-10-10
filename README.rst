====================
``gs.group.privacy``
====================
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Privacy information about a group
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

:Author: `Michael JasonSmith`_
:Contact: Michael JasonSmith <mpj17@onlinegroups.net>
:Date: 2014-10-10
:Organization: `GroupServer.org`_
:Copyright: This document is licensed under a
  `Creative Commons Attribution-Share Alike 4.0 International License`_
  by `OnlineGroups.net`_.


Introduction
============

This product provides both the mechanism to reflect on the
privacy settings for a group, and change them. These tasks are
done the `Change Privacy`_ form, and a `content provider`_.

See the documentation in the `docs` folder for information on the
privacy-introspection API.

Change Privacy
==============

The Change Privacy page, ``admin_change_basic_privacy.html`` in the Group
context, allows a *site* administrator to change the privacy of a group. 

Content Provider
================

The content provider ``groupserver.GroupPrivacy`` creates a ``<div>``
element that displays a summary of the group privacy, and an explanation of
what it means. It takes a group identifier as an argument:

.. code-block:: xml

  <p tal:defile:groupId view/groupInfo/id;" 
     tal:replace="structure provider:groupserver.GroupPrivacy">Privacy</p>

Resources
=========

- Code repository: https://github.com/groupserver/gs.group.privacy
- Questions and comments to http://groupserver.org/groups/development
- Report bugs at https://redmine.iopen.net/projects/groupserver

.. _GroupServer: http://groupserver.org/
.. _GroupServer.org: http://groupserver.org/
.. _OnlineGroups.Net: https://onlinegroups.net
.. _Michael JasonSmith: http://groupserver.org/p/mpj17
..  _Creative Commons Attribution-Share Alike 4.0 International License:
    http://creativecommons.org/licenses/by-sa/4.0/
