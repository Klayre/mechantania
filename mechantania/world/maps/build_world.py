# Builds the entire world.

#TODO If you ever have _connector_ nodes to connect from one map file to
# another, then use this file - after importing ev erything, go through all
# the world and connect the connector nodes.

#HEADER

from typeclasses.rooms import Room

#CODE

caller.msg("Building the world...Please wait...")
# Build test world
#INSERT world.maps.build_areas

caller.msg("Areas built, gluing them together...Please wait...")
# Glue the world together
#INSERT world.maps.connect_areas

caller.msg("World building DONE.")
