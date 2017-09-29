
#HEADER

import evennia
import evennia.utils.search
import utils.import_trizbort_map as MapImporter
from utils.builder_utils import remove_all_rooms

# A list of area files you should use when constructing.  These will
# be accumulated into the callers "ndb.build_area_list" dictionary.
# The dictionary will contain key="area name",value="start room #dbref"
# There will be a failure if either the area name or start room #dbref
# can't be found.
AREA_FILES = ["world/maps/areas/tutorial/tutorial.trizbort",
              "world/maps/areas/tutorial/tutorial2.trizbort"]

#CODE

# Delete the caller.ndb.builder_area_list
caller.ndb.builder_area_list = {}

# Construct each area in the game.
cntr = 0
for mapFile in AREA_FILES:
    caller.msg("Building area %d / %d : '%s'" %(cntr, len(AREA_FILES), mapFile))

    # Delete any areas with same name.
    xml_tree = MapImporter.parse_file(mapFile)
    if (not xml_tree):
        caller.msg("ERROR: Can not load map %s." % mapFile)

    area_name = MapImporter.get_map_name(xml_tree)
    if (not area_name):
        caller.msg("ERROR: Can not get map name from %s." % mapFile)

    # Remove all rooms
    objects_with_zone = evennia.utils.search.search_object_by_tag(area_name,
                                                                  category="zone")

    if len(objects_with_zone) != 0:
        caller.msg("  Warning: Zone with name %s already exists.  All rooms in this"
                   "zone will be deleted." % area_name)

    remove_all_rooms(tag=area_name, category="zone")

    roomRoot = MapImporter.construct_world(xml_tree)

    caller.msg("constructed area %s" % area_name)
    caller.msg("Starting room: %s |y#%d|n" %(roomRoot.key, roomRoot.id))

    caller.ndb.builder_area_list[area_name] = roomRoot.id

    cntr += 1
