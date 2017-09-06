# Import a trizbort (http://www.trizbort.com/) map file to create
# a map area.  The map is represented by a single room, which is
# represented by the "isStartRoom" element tag (only one room should
# have this set.  This room is returned.

# TODO - Make this return a batch script which can be executed in-game.


import evennia

from typeclasses.rooms import Room
from typeclasses.exits import Exit

import xml.etree.ElementTree as ET

def construct_world(filename):
    tree = ET.parse(filename)
    root = tree.getroot()

    print(root)
    print(root.attrib)

    infoRoot = None
    mapRoot = None

    for child in root:
        if (child.tag == "info"):
            infoRoot = child
        if (child.tag == "map"):
            mapRoot = child

    # Iterate over all the children in mapRoot.
    # Children tags:
    #   "room" - A roomt
    #   "line" - A connect between rooms

    # Dict of rooms by their unique ID  (note ID is
    # global amongst everything.
    xmlRooms = {}

    # Starting room ID
    startRoomId = None

    # Dict of exits by their unique ID
    xmlExits = {}


    for child in mapRoot:
        childId = child.attrib["id"]

        if (child.tag == "room"):
            xmlRooms[childId] = child

            if (child.attrib.get("isStartRoom")):
                if (child.attrib.get("isStartRoom") == "yes"):
                    startRoomId = childId

        elif (child.tag == "line"):
            xmlExits[childId] = child

    print (xmlRooms)
    print (xmlExits)
    print ("Start room: " + startRoomId)                    


    # Now we have all our rooms and exits. Let's start creating.

    # Start by creating all the rooms.  Keep them in dict by their original
    # ID for easy reference.
    mechRooms = {}

    for roomId, roomNode in xmlRooms.iteritems():
        mechRooms[roomId] = create_mech_room_from_xml(roomNode)
        print(mechRooms[roomId])
        print(mechRooms[roomId].id)


    for exitId, exitNode in xmlExits.iteritems():
        create_room_exits_from_xml(exitNode, mechRooms)

    # Return the starting room.
    return mechRooms[startRoomId]

def create_mech_room_from_xml(xml_room_node):
    # Create our room.
    # TODO: Use region for zone
    name = xml_room_node.attrib.get("name")
    desc = xml_room_node.attrib.get("description")

    # TODO Allow for typeclasses to be specified
    # TODO Allow for locks/permissions to be specified
    # TODO Allow for aliases to be specified
    # TODO Allow for mapsymbol to be specified

    roomObject = evennia.create_object(typeclass = "rooms.Room", key=name)
    roomObject.db.desc = desc

    return roomObject

# Returns a list of primary name as first element, and aliases
# as other elements
def get_cardinal_name_and_aliases_from_dock_node(dock):
    portDir = dock.attrib.get("port")
    retList = []
    if portDir == "s":
        retList.append("south")
        retList.append("s")
    elif portDir == "w":
        retList.append("west")
        retList.append("w")
    elif portDir == "n":
        retList.append("north")
        retList.append("n")
    elif portDir == "e":
        retList.append("east")
        retList.append("e")
    elif portDir == "ne":
        retList.append("northeast")
        retList.append("ne")
    elif portDir == "se":
        retList.append("southeast")
        retList.append("se")
    elif portDir == "sw":
        retList.append("southwest")
        retList.append("sw")
    elif portDir == "nw":
        retList.append("northwest")
        retList.append("nw")

    # Otherwise just return whatever was stored.
    # TODO: Add aliases?
    retList.append(portDir)

    return retList

def create_room_exits_from_xml(xml_exit_node, mechRoomsDict):
    # Create the exits

    # A list - First 2 entries are source and destination.
    roomSrcDist = []

    # Get the ids. Each "dock" has ids in continous order for a single exit,
    # so store in a list.
    dockNodes = {}
    for child in xml_exit_node:
        print("dock node:\n")
        print(child)
        if (child.tag == "dock"):
            dockNodes[child.attrib.get("index")] = child 
            roomSrcDist.append(child.attrib.get("id"))
            print(dockNodes[child.attrib.get("index")])

    print(roomSrcDist)
    # Create exits on both rooms.
    for dockKey, dock in dockNodes.iteritems():
        print dock
        exitNameList = get_cardinal_name_and_aliases_from_dock_node(dock)

        dockIndex = int(dock.attrib.get("index"))
 
        # TODO Tags?
        srcRoom = mechRoomsDict[roomSrcDist[dockIndex]]
        dstRoom = mechRoomsDict[roomSrcDist[(dockIndex + 1) % 2]]

        evennia.create_object(typeclass = "exits.Exit",
                             key=exitNameList[0],
                             location=srcRoom,
                             aliases=exitNameList[1:],
                             destination=dstRoom)

