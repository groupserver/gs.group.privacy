:mod:`gs.group.privacy` API Reference
=====================================

.. currentmodule:: gs.group.privacy

.. autoclass:: gs.group.privacy.GroupVisibility
   :members: 

Normally an *adapter* is used to create the group-visibility
class from a group-info object. In the example below the
group-info object is adapted into the group-visibility, and stuff
happens if the group is public.

.. code-block:: python

   groupVisiblity = IGSGroupVisibility(self.groupInfo)
   if groupVisibility.isPublic:
       self.doStuff()

Alternatively, because the visibility class provides more
specific interfaces it can be used as a basis for an adapter. In
this example the group-info is adapted into the group visibility,
which in turn is chained into a joiner.

.. code-block:: python

   groupVisiblity = IGSGroupVisibility(self.groupInfo)
   joiner = IJoiner(groupVisibiliy)
   joiner.join(groupMember)


Interfaces
----------

.. autoclass:: gs.group.privacy.interfaces.IGSGroupVisibility
   :members:

.. autoclass:: gs.group.privacy.interfaces.IGSChangePrivacy
   :members:

.. autoclass:: gs.group.privacy.interfaces.IPublic
   :members:

.. autoclass:: gs.group.privacy.interfaces.IPublicToSiteMember
   :members:

.. autoclass:: gs.group.privacy.interfaces.IPrivate
   :members:

.. autoclass:: gs.group.privacy.interfaces.ISecret
   :members:

.. autoclass:: gs.group.privacy.interfaces.IOdd
   :members:

Visibility function
-------------------

The :class:`GroupVisibility` class determines the visibility of a
group by inspecting the objects in the group, and the group
itself, with the :func:`utils.get_visibility`
function.

.. automodule:: gs.group.privacy.utils
   :members: get_visibility, PERM_ODD, PERM_ANN, PERM_GRP, PERM_SIT

