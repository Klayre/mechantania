# Creates a map that can be printed.
from typeclasses.mobjects.mech_base_rooms import MechBaseRoom

MAP_SIZE_W = 9
MAP_CENTER = (MAP_SIZE_W/2, MAP_SIZE_W/2)
NO_ROOM_CHAR = '.'

class Mapper():

    def __init__(self):
        self.reset_map()

    def reset_map(self):
        self.map = [['.' for x in range(MAP_SIZE_W)] for y in \
                    range(MAP_SIZE_W)]

    def print_map(self):
        print(self.map)

    def has_room(self, coords):
        return self.map[coords[0]][coords[1]] != NO_ROOM_CHAR

    def do_cell_recursive(self, room, prevRoom, map_coords, do_recurse=True):

        if hasattr(room, 'map_symbol'):
            self.map[map_coords[0]][map_coords[1]] = room.map_symbol

        if (do_recurse):
            for ex in room.exits:
                if (ex.key == "north" and ex.destination != prevRoom):
                    newCoords = (map_coords[0], map_coords[1]+1)

                    # Make sure have not already visited this room
                    # on another path...
                    if (not self.has_room(newCoords)):
                        self.do_cell_recursive(ex.destination, room, newCoords)
                if (ex.key == "east" and ex.destination != prevRoom):
                    newCoords = (map_coords[0]+1, map_coords[1])

                    # Make sure have not already visited this room
                    # on another path...
                    if (not self.has_room(newCoords)):
                        self.do_cell_recursive(ex.destination, room, newCoords)
                if (ex.key == "south" and ex.destination != prevRoom):
                    newCoords = (map_coords[0], map_coords[1]-1)

                    # Make sure have not already visited this room
                    # on another path...
                    if (not self.has_room(newCoords)):
                        self.do_cell_recursive(ex.destination, room, newCoords)
                if (ex.key == "west" and ex.destination != prevRoom):
                    newCoords = (map_coords[0]-1, map_coords[1])

                    # Make sure have not already visited this room
                    # on another path...
                    if (not self.has_room(newCoords)):
                        self.do_cell_recursive(ex.destination, room, newCoords)
        
        pass

    def generate_map(self, roomCenter):
        self.do_cell_recursive(roomCenter, roomCenter, MAP_CENTER)

        print(self)
        pass

    def __str__(self):
        retStr = ""

        # TODO Flip
        for y in range(MAP_SIZE_W):
            retStr += "\n"
            for x in range(MAP_SIZE_W):
                retStr += self.map[x][y]

        return retStr
