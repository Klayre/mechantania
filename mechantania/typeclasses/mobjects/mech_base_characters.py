from evennia import DefaultCharacter
from world.stats.mech_base_stats import MechBaseStatContainer
import re

## Subclass of MechBaseStatsContainer that contains stats common
## to all characters.
#class MechCharacterStatContainer(MechBaseStatContainer):
#
#    def __init__(self, initCharacterStats):
#        # Required stats for a character
#        # Make sure to define a property for it at end of this
#        # class to make it easily accessible.
#        required_stats = ["hp"]
#        name = "Base character stats"
#
#        for st in required_stats:
#            if (initCharacterStats.get(st) == None):
#                print("HP is required!")
#                # TODO log error about not having required stats.
#
#        super(MechCharacterStatContainer, self).__init__(name, initCharacterStats)
#
#    ### Properties for common stats.
#    ###
#    @property
#    def hp(self):
#        return self.get("hp")
#
#    @hp.setter
#    def hp(self, val):
#        return self.set("hp", val)
from evennia.utils import lazy_property
from world.stats.traits import TraitHandler

#class MechCharacterStats:
#
#    def __init__(self, ownerCharacter):
#        self.char = ownerCharacter
#
#    # Base stats of the character

class MechBaseCharacter(DefaultCharacter):
    """
    The Character defaults to reimplementing some of base Object's hook methods with the
    following functionality:

    at_basetype_setup - always assigns the DefaultCmdSet to this object type
                    (important!)sets locks so character cannot be picked up
                    and its commands only be called by itself, not anyone else.
                    (to change things, use at_object_creation() instead).
    at_after_move(source_location) - Launches the "look" command after every move.
    at_post_unpuppet(player) -  when Player disconnects from the Character, we
                    store the current location in the pre_logout_location Attribute and
                    move it to a None-location so the "unpuppeted" character
                    object does not need to stay on grid. Echoes "Player has disconnected" 
                    to the room.
    at_pre_puppet - Just before Player re-connects, retrieves the character's
                    pre_logout_location Attribute and move it back on the grid.
    at_post_puppet - Echoes "PlayerName has entered the game" to the room.

    """

    def at_object_creation(self):
        "This is called when object is first created, only."
        pass

    def at_before_move(self, dest):

        """
        Checks the room doesn't have any objects with mIsBlocking property
        """
        isBlocked = False

        # Search all objects in room
        allObjects = (con for con in dest.contents)

        # Filter out just things
        allBlockingObjects = []

        for con in allObjects:
            if (hasattr(con.db, 'mIsBlocking') and con.db.mIsBlocking):
                isImmortal = False
                
                if self.locks.check_lockstring(self, "dummy:perm(Immortals)"):
                    isImmortal = True

                if (not isImmortal):
                    # Only block non-immortals
                    allBlockingObjects.append(con)
                    self.msg("A %s blocks your path." % con.name)
                else:
                    self.msg("You would have been blocked by a %s, but you are an "
                             "IMMORTAL!" % con.name)

        if (len(allBlockingObjects) != 0):
            return False

        # Otherwise just do normal movement.
        return super(MechBaseCharacter, self).at_before_move(dest)

     # Overload "search" to also allow the syntax <exit>.<object>

    def search(self, searchdata,
               global_search=False,
               use_nicks=True,  # should this default to off?
               typeclass=None,
               location=None,
               attribute_name=None,
               quiet=False,
               exact=False,
               candidates=None,
               nofound_string=None,
               multimatch_string=None,
               use_dbref=True):

        # Check if we have an exit pre-pended to the start of the command
        p = re.compile("(.+)\.(.+)")
        searchmatch = p.search(searchdata)
        
        if searchmatch:
            # We do have an exit pre-pended, let's extract it and then search
            # that location for the object we want.
            # We do this by
            # 1) stripping off the prepended location + "." from the object
            # 2) using the prepended location to search the "exits", and if
            # found, set the target of the search command there

            searchLocationString = None
            searchTarg = None

            searchLocationString = searchmatch.group(1)
            searchTarg = searchmatch.group(2)

            for ex in self.location.exits:
                if (ex.key == searchLocationString) or (searchLocationString in ex.aliases.all()):
                    location = ex.destination
                    searchdata = searchTarg
                    break

    
        return super(MechBaseCharacter, self).search(searchdata, global_search,
                                             use_nicks, typeclass,
                                             location,
                                             attribute_name,
                                             quiet,
                                             exact,
                                             candidates,
                                             nofound_string,
                                             multimatch_string,
                                             use_dbref)

    @lazy_property
    def stats_base(self):
        return TraitHandler(self, db_attribute='stats_base')
