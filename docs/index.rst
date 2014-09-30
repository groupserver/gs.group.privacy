:mod:`gs.group.privacy`
=======================

Contents:

.. toctree::
   :maxdepth: 2

   api
   HISTORY

While the standard Zope *access control lists* are used to set
the permissions for a group, the GroupServer_ privacy mechanism
create four *bundles* of permissions: public, public to site
members, private, and secret. This product provides both the
mechanism to reflect on the privacy settings for a group, and
change them.

Privacy definitions
-------------------

Public:

  * The group is visible to everyone
  * The files are visible to everyone
  * The messages are visible to everyone

Public to site members:

  * The group is visible to members of the site (if they are
    logged in)
  * The files are visible to members of the site (if they are
    logged in)
  * The messages are visible to members of the site (if they are
    logged in)

Private:

  * The group is visible to everyone
  * The files are visible to group-members only
  * The messages are visible to group-members only

Secret:

  * The group is visible to group-members only
  * The files are visible to group-members only
  * The messages are visible to group-members only

Odd:

  * The current permissions fail to reflect a standard
    configuration

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

Resources
=========

- Code repository: https://github.com/groupserver/gs.group.privacy
- Questions and comments to http://groupserver.org/groups/development
- Report bugs at https://redmine.iopen.net/projects/groupserver

.. _GroupServer: http://groupserver.org/
