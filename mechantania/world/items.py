import typeclasses.objects as objects
from evennia.utils import lazy_property
from world.handlers.traits import TraitHandler

STATS_NAME = "stats_item"

# Stats common to all items.
STATS_ITEM = {
    'rarity' : { 'name':'rarity', 'type':'static', 'base':0 },
}

# Stats common to all equippables 
STATS_EQUIPPABLE = {
    'attack' : { 'name':'attack', 'type':'static', 'base':0 },
    'speed' : { 'name':'speed', 'type':'static', 'base':0 },
    'defense' : {'name':'defense', 'type':'static', 'base':0 },
    'bulkiness' : {'name':'bulkiness', 'type':'static', 'base':0 },
    'durability' : {'name':'durability', 'type':'gauge', 'base':0, 'min':0},
    'level' : { 'name':'level', 'type':'static', 'base':0 },
}

def RepresentsInt(s):
    try:
        int(s)
        return True
    except ValueError:
        return False

# Light, medium, heavy armor/weapons/clothes.
# TODO: Maybe these should be related only to weapons/armor later,
# TODO: Turn this into a wrapper function instead
# not to clothes.
EQUIP_SIZES = ["none", "light", "medium", "heavy"]

class Item(objects.Object):

        #for key, kwargs in BASE_STATS.iteritems():
        #    self.stats_base.add(key, **kwargs)

    def at_object_creation(self):
        super(Item, self).at_object_creation()

        self.locks.add(";".join(("puppet:perm(Wizards)",
                                 "equip:false()",
                                 "get:true()"
                                )))

        # Attach the item stats.
        if self.stats:
            del self.stats

        # Create the stats if they don't already exist.
        for key, kwargs in STATS_ITEM.iteritems():
            if not self.stats.get(key):
                # Only add the stat if it doesn't exist.
                self.stats.add(key, **kwargs)

            # Check the "ndb" stat names, which might have been set through
            # prototypes.
            if key in self.nattributes.all():
                stat = self.stats.get(key)

                if stat is not None:
                    stat.base = self.nattributes.get(key)


    def return_apearance(self, looker):
        pass

    @lazy_property
    def stats(self):
        return TraitHandler(self, db_attribute=STATS_NAME)


class Equippable(Item):
    def at_object_creation(self):
        super(Equippable, self).at_object_creation()

        self.locks.add("puppet:false();wear:true()")

        # Default slot is armor.
        self.db.slots = ["body"]

        # Attach the item stats.
        for key, kwargs in STATS_EQUIPPABLE.iteritems():
            if not self.stats.get(key):
                # Only add the stat if it doesn't exist.
                self.stats.add(key, **kwargs)


    def at_equip(self, equipper):
        pass

    def basetype_posthook_setup(self):
        # Check the "db" stat names, which might have been set through
        # prototypes.

        # This is called from basetype_posthook_setup because all of the attributes
        # in a prototype are added BEFORE this call in at_first_save, but after
        # at_object_creation (so at_object_creation can't be used)

        # Any DB stats with traits of the same name will instead set the state,
        # and the corresponding attribute will be removed.
        for key in self.stats.all:
            attribValue = self.attributes.get(key)
            if attribValue is not None:
                stat = self.stats.get(key)
                stat.base = attribValue
                self.attributes.remove(key)

        # Init internal attributes
        self.__init_prototype_attribs()

        print("equip size : {}".format(self.db.equip_size))


    #
    # Internal functions
    #
    def __init_prototype_attribs(self):
        # Checks that the attributes from prototypes is valid
        equip_size = self.attributes.get("equip_size")

        # Clean equip size, either by converting to int from string or by cleaning the string.
        if equip_size is not None:
            equip_size = equip_size.lower()
            if equip_size not in EQUIP_SIZES:
                raise ValueError("Invalid equip_size param {}".format(equip_size))

            self.db.equip_size = equip_size
