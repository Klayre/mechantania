
#HEADER
import utils.builder_utils

#CODE

#
# Glues together the areas in order to form the whole world.
#

# For each area, gather all the rooms with tags for "special".

#for area, startRoom in caller.ndb.builder_area_list.iteritems():
#
#    # First destroy any rooms from this area previously created.
#    remove_all_rooms(tag=area, category="zone")

# Look for connectors
utils.builder_utils.connect_all_areas()
