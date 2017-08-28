from evennia import CmdSet
from evennia import DefaultObject 

"""

A tree object.  A tree in a room will block the player from entering the room.
A player can chop the tree down and the tree will drop logs of wood (random)

Create this tree with:
    @create/drop mobjects.environment.tree.Tree
"""
class DefaultCmdSet(CmdSet):
    key = "Tree"

    def at_cmdset_creation(self):
        # No commands
        pass

# TODO: Objects will have a host of flags on them.  BLOCKING is one of them.
# This class should be refactoring with the BLOCKING flag and inherrited from
# an mobject later.

from evennia import DefaultObject

class Tree(DefaultObject):

    def at_object_creation(self):
        desc = "A large tree."
        self.db.desc = desc

        # no commands at this time
        #self.cmdset.add_default(treeCmdSet, permanent = True)

        #
        # Member variables
        #

        # Whether this tree blocks the room for entry
        self.db.mIsBlocking = True
  

