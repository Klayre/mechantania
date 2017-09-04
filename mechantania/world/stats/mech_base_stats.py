"""
MechBaseStats

A base stats handler.  This has common methods that
allow for merging stats, retrieving stats (based on merge),
etc.
"""

#from mobjects.mech_base_objects import MechBaseObjects

class MechStatData():
    """
    MechStatData

    A single stat data type.

    This can be used fine for simple stats with scalar name/value.
    For stats with more complex values, then those will need to subclass
    this and redefine __hash__ and __eq__.
    """

    def __init__(self, nameStr, val):
        self.name = nameStr
        self.value = val

    def __hash__(self):
        return hash((self.name))

    def __eq__(self, other):
        if (type(other) == str):
            return (self.name) == (other)
        else:
            return (self.name) == (other.name)

    def __ne__(self, other):
        return not(self == other)

    def __repr__(self):
        return "[{0} : {1}]".format(str(self.name), str(self.value))

    def __str__(self):
        return self.__repr__()

## TODO : Remove the "_other_" functionality.  have this only be a container,
## and add a stats handler class if you really want to be able to merge and
## stuff.
class MechBaseStatContainer():
    """
    MechBaseStatContainer

    The root base stats.
    """

    def __init__(self, initialStats = {}):#, objAttached):
#        obj = objAttached

        # Initialize stats data to empty dictionary.
        self.stats_data = {}

        # Other stats objects which will be merged into this one.
        # This way, if two stats objects have a stat with the same name,
        # when getting this stat the two will be added.
        self.other_stats_objects = []
        
        for k in initialStats.keys():
            self.add_stats_data_object(MechStatData(k, initialStats[k]))

    def __str__(self):
        # So that when examining attributes this will pretty-print things
        retStr = "["
        for msd_key in self.stats_data.keys():
            retStr += " {0} ".format(self.stats_data[msd_key])
        retStr += "]"

        return retStr

    def has_other_stats_handler(self, otherStatsHandler):

        if (otherStatsHandler == self):
            return True

        hasHandler = False
        for obj in self.other_stats_objects:
            if (obj.has_other_stats_handler(otherStatsHandler)):
                hasHandler = True

        return hasHandler

    def add_stats_data_object(self, mechStatData):
        """
        add

        Accepts a MechStatsData object
        """

        self.stats_data[mechStatData] = mechStatData

    def add_other_stats_container(self, otherMechStatContainer):
        if (self == otherMechStatContainer):
            return

        # If we already have this stat handler, or if any of the subclasses has
        # it,
        # dont add
        if (self.has_other_stats_handler(otherMechStatContainer)):
            return

        self.other_stats_objects.append(otherMechStatContainer)

    def get_value(self, nameStr, combined=True):
        """
        get

        Gets a MechStatsData object
        """
        stats = self.stats_data[nameStr]

        totVal = stats.value

        if combined and (len(self.other_stats_objects) != 0):
            for obj in self.other_stats_objects:
                if (obj.get_value(nameStr, combined=True)):
                    totVal += obj.get_value(nameStr)

        return totVal 
