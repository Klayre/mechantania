# Import a trizbort (http://www.trizbort.com/) map file to create
# a map area.  The map is represented by a single room, which is
# represented by the "isStartRoom" element tag (only one room should
# have this set.  This room is returned.

# TODO - Make this return a batch script which can be executed in-game.


import evennia

from typeclasses.rooms import Room
from typeclasses.exits import Exit
import re

import xml.etree.ElementTree as ET

# Checks for special room, and if so, returns special attribute.
def check_for_special_room(roomNode):
    roomName = roomNode.attrib.get("name")

    if not roomName:
        raise Exception("Invalid room name on special")
        return None

    m = re.search("special:(.+?)", roomName)

    if m:
        return m.group(1)

    return None

def get_special_room_attrib(roomNode, attribName):
    roomSubtitle = roomNode.attrib.get("subtitle")

    if not roomSubtitle:
        raise Exception("Invalid room name on subtitle")
        return None

    searchString = attribName + ":(.+)"
    m = re.search(searchString, roomSubtitle)

    if m:
        return m.group(1)

    return None

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
        if not check_for_special_room(roomNode):
            mechRooms[roomId] = create_mech_room_from_xml(roomNode)
            print(mechRooms[roomId])
            print(mechRooms[roomId].id)
        else:
            print("Found a special room")
            toRoomName = get_special_room_attrib(roomNode, "to")
            print("special room name: %s" % toRoomName)
            if not (toRoomName):
                raise Exception("Invalid special attribute!")
            toRoom = Room.objects.search_object(toRoomName)[0]
            print("toRoom = %s" % toRoom)
            mechRooms[roomId] = toRoom

    for exitId, exitNode in xmlExits.iteritems():
        create_room_exits_from_xml(exitNode, xmlRooms, mechRooms)

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

def get_named_exit_from_line(xml_line_node):
    lineName = xml_line_node.attrib.get("name")
    #TODO: Aliases.
    #TODO: Exit description

    return [lineName]

def create_room_exits_from_xml(xml_exit_node, xml_rooms_dict, mechRoomsDict):
    # Create the exits
    #TODO: ONE-WAY EXITS! This is useful for non-cardinal direction exits which
    # might have different discriptions on either side of the exit...

    # A list - First 2 entries are source and destination.
    roomsSrcDest = []

    # Get the ids. Each "dock" has ids in continous order for a single exit,
    # so store in a list.
    dockNodes = {}
    for child in xml_exit_node:
        if (child.tag == "dock"):
            dockIndex = child.attrib.get("index")
            dockNodes[dockIndex] = child 

            roomId = child.attrib.get("id")
            roomsSrcDest.append(mechRoomsDict[roomId])

    # Create exits on both rooms.
    for dockKey, dock in dockNodes.iteritems():
        print dock

        exitNameList = []
        if xml_exit_node.attrib.get("name"):
            if (xml_exit_node.attrib.get("name") != ""):
                # Names on exits override
                exitNameList = get_named_exit_from_line(xml_exit_node)

        if (len(exitNameList) == 0):
            exitNameList = get_cardinal_name_and_aliases_from_dock_node(dock)

        dockIndex = int(dock.attrib.get("index"))
 
        # TODO Tags?
        srcRoom = roomsSrcDest[dockIndex]
        dstRoom = roomsSrcDest[(dockIndex + 1) % 2]

        for exit in srcRoom.exits:
            if exit.name == exitNameList[0]:
                msg = "Trying to create an exit {0}:#{1} on room" \
                      "{2}:#{3} that already has that exit " \
                      "created!".format(exit.name, exit.id, \
                       srcRoom.name, srcRoom.id)
                            
                print(msg)
                raise Exception(msg)

        evennia.create_object(typeclass = "exits.Exit",
                             key=exitNameList[0],
                             location=srcRoom,
                             aliases=exitNameList[1:],
                             destination=dstRoom)

