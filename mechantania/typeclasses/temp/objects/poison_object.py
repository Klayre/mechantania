"""

A simple poison object.

This will be [drink]able by the player.  If it is [drinked], then
the player's health will diminish by -20 HP every 10 seconds.  A message
will be sent to the player that his health is being depleted, and a message
will be sent to the room that the player looks ill.

After the player's health has reached 0 HP, the Player's HP will reset
and a message will be emitted stating the player has fake died.

Create this poison with

 @create/drop temp.objects.poison_object.Poison
"""
from evennia import DefaultObject

#
#  Poison definition
#

# Inherit from DefaultObject
class Poison(DefaultObject):
    def at_object_creation(self):
        """
        Called when object is created.
        """
        desc = "A bottle of poison."
        self.db.desc = desc

        # Must define these before adding the scripts
        # incase the scripts reference these
        self.db.is_full = True 

        # self.cmdset.add_default(poisonCommands.DefaultCmdSet, permanent=True)



