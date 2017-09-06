"""
MechBaseStats

A base stats handler.  This has common methods that
allow for merging stats, retrieving stats (based on merge),
etc.
"""

#from mobjects.mech_base_objects import MechBaseObjects

class MechStatData(object):
    """
    MechStatData

    A single stat data type.

    This can be used fine for simple stats with scalar name/value.
    For stats with more complex values, then those will need to subclass
    this and redefine __hash__ and __eq__.
    """

    def __init__(self, nameStr, val, metadata = None):
        self.name = nameStr
        self.value = val
        self.metadata = metadata

    def __hash__(self):
        return hash((self.name))

    def __eq__(self, other):
        if (other == None):
            # TODO : Figure out how to get around this
            return False
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

# Subclass this in order to get stat-specific functionality.
class MechBaseStatContainer(object):
    """
    MechBaseStatContainer

    The root base stats.
    """

    def __init__(self, name, initialStats = {}):

        # Initialize stats data to empty dictionary.
        self.stats_data = {}

        self.name = name

        for k in initialStats.keys():
            initStat = initialStats[k]
            # Will add the value associated with the key.
            # The value can be either a MechStatData object or
            # a scalar value, in which case a new MechStatData will
            # be created internally with None for metadata
            self.add(k, initStat)

    def __str__(self):
        # So that when examining attributes this will pretty-print things
        retStr = self.name + " -> ["
        for msd_key in self.stats_data.keys():
            retStr += " {0} ".format(self.stats_data[msd_key])
        retStr += "]"

        return retStr

    def add(self, nameStr, value, metaData = None):
        """
        add

        Accepts name, value, and meta data.  Used to create
        a new stat.
        
        Args:
            nameStr - A string representing the stat name
            value - A value associated with the stat name
            metaData - Any metadata object or value.
        """
        inMechStatData = None

        if (type(value) == MechStatData):
            inMechStatData = value
        else:
            # Create new MechStatsData class
            inMechStatData = MechStatData(nameStr, value, metaData)

        self.add_stats_data_object(inMechStatData)

    def add_stats_data_object(self, mechStatData):
        if (mechStatData in self.stats_data):
            # Skip if already exists.
            return

        self.stats_data[mechStatData] = mechStatData

    # Gets the value
    def get(self, nameStr):
        """
        get

        Gets a MechStatsData object
        """
        retVal = self.stats_data.get(nameStr)

        if (retVal != None):
            return retVal.value

        return None

    def get_stats_data_object(self, nameStr):
        return self.stats_data.get(nameStr)

    def set(self, nameStr, value):
        # Check if contains
        stats = self.stats_data.get(nameStr)

        if (stats != None):
            stats.value = value

    def set_from_stats_data_object(self, mechStatData):
        statsData = self.stats_data.get(mechStatData)

        if (statsData != None):
            self.stats_data[mechStatData] = mechStatData

    def delete(self, nameStr):
        if (self.stats_data.get(nameStr)):
            del self.stats_data[nameStr]

