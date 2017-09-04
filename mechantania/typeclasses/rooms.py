"""
Room

Rooms are simple containers that has no location of their own.

"""

from evennia import DefaultRoom


class Room(DefaultRoom):
    """
    Rooms are like any Object, except their location is None
    (which is default). They also use basetype_setup() to
    add locks so they cannot be puppeted or picked up.
    (to change that, use at_object_creation instead)

    See examples/object.py for a list of
    properties and methods available on all Objects.
    """

    # Returns if the room is blocked by an object or not.
    def get_blocking_objects(self):

        # Search the room's objects for any blocking object.
        return [obj for obj in self.contents_get() if
                        hasattr(obj.db, 'mIsBlocking') and obj.db.mIsBlocking]

