# Creates a map that can be printed.
from typeclasses.mobjects.mech_base_rooms import MechBaseRoom

# Map size in W/H
MAP_SIZE_W = 9

# Center of the map from character's POV
MAP_CENTER = (MAP_SIZE_W/2, MAP_SIZE_W/2)

# Default if no symbol can be obtained from room.

NO_ROOM_CHAR = '.'

class Mapper():

    """
    A basic dynamic mapper class which will display the map with MAP_SIZE_W in
    WxH
    """

    def __init__(self):
        """
        Initializes the map
        """

        self.reset_map()

    def reset_map(self):
        """
        Clears the map and fills in with default NO_ROOM_CHAR
        """
        self.map = [['.' for x in range(MAP_SIZE_W)] for y in \
                    range(MAP_SIZE_W)]

    def print_map(self):
        """
        Prints the map to text.  Only used for debugging.
        """
        print(self.map)

    def has_room(self, local_coords):
        """
        Checks if the room at local_coords (local) is already in the map
        """
        return self.map[local_coords[0]][local_coords[1]] != NO_ROOM_CHAR

    def is_valid_coords(self, coords):
        if ((coords[0] < 0) or (coords[0] >= MAP_SIZE_W) or
            (coords[1] < 0) or (coords[1] >= MAP_SIZE_W)):
            return False

        return True

    def do_cell_recursive(self, room, prevRoom, local_coords, do_recurse=True):

        # TODO: If db.map_symbol does not exist, this leads to strange things.
        # I think there is a bug in how i'm checking below...
        if room.attributes.has('map_symbol'):
            if isinstance(room, MechBaseRoom):
                self.map[local_coords[0]][local_coords[1]] = \
                        room.get_map_symbol()
#                if (type(room.attributes.get('map_symbol') == str)):
#                    self.map[local_coords[0]][local_coords[1]] = room.attributes.get('map_symbol')
#            else:
#                ## Not needed since map is initialized to empty NO_ROOM_CHAR

        if (do_recurse):
            for ex in room.exits:
                if (ex.key == "north" and ex.destination != prevRoom):
                    newCoords = (local_coords[0], local_coords[1]+1)

                    # Make sure have not already visited this room
                    # on another path...
                    if (self.is_valid_coords(newCoords) and not self.has_room(newCoords)):
                        self.do_cell_recursive(ex.destination, room, newCoords)
                if (ex.key == "east" and ex.destination != prevRoom):
                    newCoords = (local_coords[0]+1, local_coords[1])

                    # Make sure have not already visited this room
                    # on another path...
                    if (self.is_valid_coords(newCoords) and not self.has_room(newCoords)):
                        self.do_cell_recursive(ex.destination, room, newCoords)
                if (ex.key == "south" and ex.destination != prevRoom):
                    newCoords = (local_coords[0], local_coords[1]-1)

                    # Make sure have not already visited this room
                    # on another path...
                    if (self.is_valid_coords(newCoords) and not self.has_room(newCoords)):
                        self.do_cell_recursive(ex.destination, room, newCoords)
                if (ex.key == "west" and ex.destination != prevRoom):
                    newCoords = (local_coords[0]-1, local_coords[1])

                    # Make sure have not already visited this room
                    # on another path...
                    if (self.is_valid_coords(newCoords) and not self.has_room(newCoords)):
                        self.do_cell_recursive(ex.destination, room, newCoords)
        
        pass

    def generate_map(self, roomCenter):
        """
        Main call to generate the map.
        
        This should be called anytime the room that is the center
        of the map needs to change.  I.e. when a player changes rooms.
        """
        self.do_cell_recursive(roomCenter, roomCenter, MAP_CENTER)

        # Convert map to unicode
        for x in range(MAP_SIZE_W):
            for y in range(MAP_SIZE_W):
                if isinstance(self.map[x][y], basestring):
                    self.map[x][y] = self.map[x][y].decode('UTF-8')
        pass

    def __str__(self):
        retStr = ""

        # Flips so that the display starts with (0, 0) at the bottom
        for y in range(MAP_SIZE_W):
            retStr += "\n"
            for x in range(MAP_SIZE_W):
                # format to 2 char
                retStr += '{: <2}'.format(self.map[x][(MAP_SIZE_W - 1) - y])

        return retStr
