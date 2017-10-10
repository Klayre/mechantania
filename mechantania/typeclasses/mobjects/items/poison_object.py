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
from typeclasses.objects import Object 

from commands.items.poison_commands import DefaultCmdSet as poisonCmdSet
from mscripts.poison_script import PoisonScript

#
#  Poison definition
#

class Poison(Object):

    def at_object_creation(self):
        """
        Called when object is created.
        """
        desc = "A bottle of poison."
        self.db.desc = desc

        # Must define these before adding the scripts
        # incase the scripts reference these
        self.db.is_full = True 

        self.cmdset.add_default(poisonCmdSet, permanent=True)

    def return_appearance(self, looker):
        # Get the description of parent
        string = super(Poison, self).return_appearance(looker)

        if self.db.is_full:
            return string + "\n\nA tiny bottle of |g green |n liquid."
        else:
            return string + "\n\nThe bottle appears empty"
    
    def do_drink(self, pobject):
        if (not self.db.is_full):
            pobject.msg("You can't drink from an empty bottle...")
            return

        if (pobject.db.mech_character_stats_container == None):
            pobject.msg("You can't drink this poison, apparently you have no "
                        "stats... are you even alive?")
            return

        currHp = pobject.db.mech_character_stats_container.get_value("hp_curr")
        if (currHp == None):

            pobject.msg("You can't drink this poison, apparently you have no"
                        "HP... are you even alive?")
            # Why is this called on a non-player?
            return


        # Attach the poison script to the player
        pobject.scripts.add(PoisonScript)

        pobject.msg("You chug the bottle of poison.")
        self.db.is_full = False
