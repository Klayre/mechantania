"""
Room

Rooms are simple containers that has no location of their own.

"""

from mobjects.mech_base_rooms import MechBaseRoom
from evennia import utils
from typeclasses.characters import Character
from typeclasses.characters import Npc


class Room(MechBaseRoom):
    """
    Rooms are like any Object, except their location is None
    (which is default). They also use basetype_setup() to
    add locks so they cannot be puppeted or picked up.
    (to change that, use at_object_creation instead)

    See examples/object.py for a list of
    properties and methods available on all Objects.
    """
    def at_object_receive(self, obj, source_location):
        if utils.inherits_from(obj, Npc): # An NPC has entered
            pass
        else:
            if utils.inherits_from(obj, Character):
                # A player character has entered.
                # Cause the character to look around

                # Note this used to be in "at_after_move"
                obj.execute_cmd('look')

                for item in self.contents:
                    if utils.inherits_from(item, Npc):
                        # An NPC is in the room
                        item.at_char_entered(obj)


