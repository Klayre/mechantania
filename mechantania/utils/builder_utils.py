import evennia.utils.search
from typeclasses.rooms import Room
from typeclasses.characters import Character
from typeclasses.accounts import Account
from typeclasses.exits import Exit
import evennia


def remove_all_rooms(tag=None, category=None):

    if tag:
        rooms = evennia.utils.search.search_object_by_tag(key=tag, category=category)

    else:
        # Removes all rooms from the world, except for limbo
        rooms = Room.objects.all()

    numRooms = len(rooms) - 2 # Don't count Limbo
    cntr = 0

    for room in rooms:
        # Clear exits
        room.clear_exits()


        if room.name == "Limbo" or room.id == 2:
            # Don't delete limbo
            continue
        
        print "Deleting room %d / %d" % (cntr, numRooms)
        # First delete on non-account, non-character objects in the room if
        # their home is set to this zone.

        roomObjects = room.contents
        for roomObject in roomObjects:
            if (not isinstance(roomObject, Character)
                and not isinstance(roomObject, Account)):
#                roomObject.scripts.clear()
                print ("  Deleting object '%s'" %roomObject.name)
                roomObject.delete()

        # Clear scripts
#        roomScripts = room.scripts.all()
#        for script in roomScripts:
#            script.stop()

        # Delete the room
        room.delete()
        cntr += 1

def connect_all_areas():
    CARDINAL_DIRS = { "north" : "south",
                      "south" : "north",
                      "east"  : "west",
                      "west"  : "east",
                      "northeast" : "southwest",
                      "southwest" : "northeast",
                      "southeast" : "northwest",
                      "northwest" : "southeast"}

    EXIT_OPPOSITE = { "north" : "south",
                      "south" : "north",
                      "east"  : "west",
                      "west"  : "east",
                      "northeast" : "southwest",
                      "southwest" : "northeast",
                      "southeast" : "northwest",
                      "northwest" : "southeast"}

    def is_cardinal_direction(mech_exit):
        return mech_exit.name in CARDINAL_DIRS

    # Gets the exit of of the opposite direction from destRoom (i.e.
    # if mech_exit is North, it will return the Exit object of South
    # from destRoom.
    # If opposite exit is not found, it will return None.
    def get_opposite_exit(mech_exit, destRoom):
        for exit in destRoom.exits:
            if EXIT_OPPOSITE[exit.name] == mech_exit.name:
                return exit

        return None

    # Get all the rooms that match the <area> tag
    connector_from_rooms = evennia.utils.search.search_object_by_tag(key="connector_from",
                                                                     category="map_builder")
    connector_to_rooms = evennia.utils.search.search_object_by_tag(key="connector_to",
                                                      category="map_builder")

    for from_room in connector_from_rooms:
        # get the connector dict
        connectorDict = from_room.db.map_builder_connector_dict

        if not connectorDict:
            raise Exception("No connector dictionary assigned to connector from_room "
                            "%s/#%d in zone %s" %(from_room.name,
                                                  int(from_room.id),
                                                  from_room.tags.get(category="zone")))
        
        zoneDest = connectorDict["zoneDestination"]
        connectorName = connectorDict["connectorName"]
        
        for rooms in connector_to_rooms:
            print "TEST"
            print "zoneDest: " + zoneDest
            print "connectorname: " + connectorName
            print rooms.tags.all(return_key_and_category=True)
            print rooms.ndb.connector_name
            print "connectorname == rooms.ndb.connector_name" + \
            str(str(connectorName) == str(rooms.ndb.connector_name))

        # Search the to rooms for the one with a tag with zoneDest as zone
        # TROUBLE HERE.  connector_name == connectorName doesn't seem to work.
        to_room = [to_room for to_room in connector_to_rooms if \
                   to_room.tags.get(zoneDest, category="zone") and \
                   (str(to_room.ndb.connector_name) == str(connectorName))]

        # Do we have multiple to rooms?
        if len(to_room) > 1:
            exMsg = "Multiple to_room for connector to zone %s:%s" %(zoneDest, connectorName)
            raise Exception(exMsg)

        if len(to_room) == 0:
            exMsg = "No to_room matching %s:%s" %(zoneDest, connectorName)
            raise Exception(exMsg)

        if to_room == None:
            exMsg = "No to_room for connector to zone %s:%s" %(zoneDest, connectorName)
            raise Exception(exMsg)

        to_room = to_room[0]

        # Gather exits leading into this room.
        # Check to make sure to_room doesn't already have these exits.
        # Follow the exit to exit's distination, and then set the cardinal
        # direction exit to the to_room instead
        # Then delete the from_room connector.


        #Gather exits
        from_room_exits = from_room.exits
        to_room_exits = to_room.exits

        # Gather exits in "from_room", and move them to "to_room"
        for from_exit in from_room_exits:
            exit_in_to_room = False
            create_exit_name = from_exit.name

            if (is_cardinal_direction(from_exit)):
                for to_exit in to_room_exits:
                    if to_exit.name == create_exit_name:
                        exit_in_to_room = True
                if exit_in_to_room:
                    raise Exception("Can't connect connector room exit.  There"
                                    "is already an exit named %s in room #%s"
                                    % (create_exit_name, to_room.id))

            # Create the exit in the to_room, same as exit in from_room
            evennia.create_object(typeclass = "exits.Exit",
                                  key=create_exit_name,
                                  location=to_room,
                                  destination=from_exit.destination,
                                  aliases=from_exit.aliases.all())

            # Now iterate over all the rooms with exits to the "from_room", and
            # set their destination to the to room.
            for currExit in Exit.objects.all_family():
                if currExit.destination == from_room:
                    currExit.destination = to_room


# TODO: Clean up, remove connector tags, etc
# TODO: ADd locks?
