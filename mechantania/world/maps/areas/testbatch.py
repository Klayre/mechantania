
#HEADER

import evennia
import utils.import_trizbort_map as MapImporter
#AREAS_DIR = os.path.dirname(os.path.realpath(__file__))

#CODE

roomRoot = MapImporter.construct_world("world/maps/areas/test_area.trizbort")
caller.msg("constructed world")
caller.msg("Starting room: %s #%d" %(roomRoot.key, roomRoot.id))
