====================
``gs.group.privacy``
====================
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Privacy information about a group
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

:Author: `Michael JasonSmith`_
:Contact: Michael JasonSmith <mpj17@onlinegroups.net>
:Date: 2013-03-25
:Organization: `GroupServer.org`_
:Copyright: This document is licensed under a
  `Creative Commons Attribution-Share Alike 3.0 New Zealand License`_
  by `OnlineGroups.Net`_.

Introduction
============

This product provides both the mechanism to reflect on the privacy settings
for a group, and change them. These tasks are done through the visibility_
code, and the `Change Privacy`_ form. In addition a `content provider`_ is
supplied.

While the standard Zope access controls are used to control access to a
group, the GroupServer_ privacy mechanism create three *bundles:* public,
private, and secret.

Visibility
==========

The group-visibility class can be created by adapting a group info::

  from gs.group.privacy.interfaces import IGSGroupVisibility
  ...
  visibility = IGSGroupVisibility(self.groupInfo)

The class provides five properties.

:``visibility``: A plain-text description of the group visibility: 

                 * ``public``
                 * ``private``
                 * ``secret``
                 * ``odd``
:``isPublic``: ``True`` if the group is public.
:``isPrivate``: ``True`` if the group is private.
:``isSecret``: ``True`` if the group is secret.
:``isOdd``: ``True`` if the group is odd.

Change Privacy
==============

The Change Privacy page, ``admin_change_basic_privacy.html`` in the Group
context, allows a *site* administrator to change the privacy of a group. 

Content Provider
================

The content provider ``groupserver.GroupPrivacy`` creates a ``<div>``
element that displays a summary of the group privacy, and an explanation of
what it means. It takes a group identifier as an argument::

  <p tal:defile:groupId view/groupInfo/id;" 
     tal:replace="structure provider:groupserver.GroupPrivacy">Privacy</p>

Resources
=========

- Code repository: https://source.iopen.net/groupserver/gs.group.privacy
- Questions and comments to http://groupserver.org/groups/development
- Report bugs at https://redmine.iopen.net/projects/groupserver

.. _GroupServer: http://groupserver.org/
.. _GroupServer.org: http://groupserver.org/
.. _OnlineGroups.Net: https://onlinegroups.net
.. _Michael JasonSmith: http://groupserver.org/p/mpj17
.. _Creative Commons Attribution-Share Alike 3.0 New Zealand License:
   http://creativecommons.org/licenses/by-sa/3.0/nz/
