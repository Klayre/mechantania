"""
Room

Rooms are simple containers that has no location of their own.

"""

from evennia import DefaultRoom
from evennia import DefaultCharacter 

DEFAULT_ROOM_CHAR = '`'

class MechBaseRoom(DefaultRoom):
    """
    Rooms are like any Object, except their location is None
    (which is default). They also use basetype_setup() to
    add locks so they cannot be puppeted or picked up.
    (to change that, use at_object_creation instead)

    See examples/object.py for a list of
    properties and methods available on all Objects.
    """

    def at_object_creation(self):
        self.db.map_symbol = "#"

    # Returns if the room is blocked by an object or not.
    def get_blocking_objects(self):

        # Search the room's objects for any blocking object.
        return [obj for obj in self.contents_get() if
                        hasattr(obj.db, 'mIsBlocking') and obj.db.mIsBlocking]

    def return_appearance(self, looker):
        desc = super(MechBaseRoom, self).return_appearance(looker)
        return desc

    def get_map_symbol(self, looker=None):
        map_symbol = DEFAULT_ROOM_CHAR
        #
        # Perform these operations in this order (where successive checks
        # override last)
        #   1) Room map symbol (should exist always).
        #   2) Object map symbol (if multiple objects, then what?)
        #   3) Non-player charater map symbol
        #   4) player character map symbol

        if (type(self.attributes.get('map_symbol') == str)):
            map_symbol = self.attributes.get('map_symbol')

        # Search for objects in the room with map symbols.
        for obj in self.contents_get():
            if not isinstance(obj, DefaultCharacter):
                if obj.attributes.has('map_symbol'):
                    map_symbol = obj.attributes.get('map_symbol')

        # Search for characters
        # TODO: Color these red or green depending on aggr, non-aggr, or npc
        for obj in self.contents_get():
            if isinstance(obj, DefaultCharacter):
                if obj.attributes.has('map_symbol'):
                    map_symbol = obj.attributes.get('map_symbol')


        return map_symbol

