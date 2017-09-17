from evennia import CmdSet
from evennia import DefaultObject 

"""

A tree object.  A tree in a room will block the player from entering the room.
A player can chop the tree down and the tree will drop logs of wood (random)

Create this tree with:
    @create/drop mobjects.environment.tree.Tree
"""
class DefaultWallCmdSet(CmdSet):
    key = "Wall"

    def at_cmdset_creation(self):
        # No commands on this object.
        pass

# TODO: Objects will have a host of flags on them.  BLOCKING is one of them.
# This class should be refactoring with the BLOCKING flag and inherrited from
# an mobject later.

from evennia import DefaultObject

class Wall(DefaultObject):

    def at_object_creation(self):
        desc = "A large wall."
        self.db.desc = desc
        self.db.map_symbol = "#"

        #
        # Member variables
        #
        self.db.mIsBlocking = True

        # no commands at this time.  Also don't want the player to be able
        # to "get" the tree.
        self.cmdset.add_default(DefaultWallCmdSet, permanent=True)

