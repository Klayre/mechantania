# -*- coding: UTF-8 -*-
"""
Equipment handler module.

The `EquipHandler` provides an interface to maniplate a character's
"equipped" or worn items. The handler is instantiated as a property on a
character typeclass, with the character passed as an argument. It looks
for certain properties in the character's db attributes handler to
initialize itself and provide persistence.

Config Properties:
    slots (dict): mapping of slots: equipped items
    limbs (tuple[tuple[str, tuple]]): nested tuple describing character
        limbs and which slots map to which limbs.

        This attribute should be of nested ordered types, preferably tuples.
        The format for its data is:

            limbs = (
                (limb1, (slot1,)),
                (limb2, (slot2, slot3)),
                (limb3, (slot4, ...)
            )

        Slot names will be displayed in-game in the order they appear
        in the limbs attribute. If missing or empty, slots are displayed
        in alphabetical order.

Setup:
    To use the EquipHandler, add it to a character typeclass as follows:
    ```python
    from world.equip import EquipHandler
      ...
    @property
    def equip(self):
        return EquipHandler(self)
    ```

Use:
    Equippable items are equipped and unequipped using the `add` and `remove`
    methods, respectively.

    The EquipHandler can be iterated over to access the contents of its slots
    in an ordered fashion. It also supports `obj in character.equip` syntax
    to check whether an item is equipped

Commands:
    See commands/equip.py for the commands related to this handler.

Example usage:
    # Say obj is a hat.
    > obj in character.equip
    False
    > character.equip.add(obj)
    True
    > obj in equip
    True
    > for slot, item in character.equip:
    >     print "%s: %s" % (slot, item)
    'head: a hat'
    > character.equip.get('head')
    'a hat'
    > character.equip.remove(obj)
    True
"""
from world.items import Equippable
from evennia.utils.evtable import EvTable


class EquipException(Exception):
    """Base exception class for EquipHandler."""
    def __init__(self, msg):
        self.msg = msg


class EquipHandler(object):
    """Handler for a character's "equipped" items.

    Args:
        obj (Character): parent character object. see module docstring
            for character attribute configuration info.

    Properties
        slots (tuple): returns a tuple of all slots in order
        empty_slots (list): returns a list of empty slots

    Note:
        Individual slots' items can be accessed as attributes

    Methods:
        add (Equippable): "equip" an item from the character's inventory.
        remove (Equippable): "un-equip" an item and move it to inventory.
    """
    def __init__(self, obj):
        # save the parent typeclass
        self.obj = obj

        if not self.obj.db.slots:
            raise EquipException('`EquipHandler` requires `db.slots` attribute on `{}`.'.format(obj))

        if obj.db.limbs and len(obj.db.limbs) > 0:
            self.limbs = {limb: slots for limb, slots in obj.db.limbs}
            self.slot_order = reduce(lambda x, y: x+y, (s for l, s in obj.db.limbs))
            # check that all slots are accounted for
            if set(self.slot_order) != set(self.obj.db.slots.iterkeys()):
                raise EquipException('Invalid limb configuration: slot/limb mismatch')
        else:
            self.limbs = {}
            self.slot_order = sorted(obj.db.slots.keys())

    def _set(self, slot, item):
        """Set a slot's contents."""
        # allows None values to pass all checks
        if item is not None:
            # confirm the item is equippable
            if not item.is_typeclass(Equippable, exact=False):
                raise EquipException("Item is not equippable.")
            # confirm the requested slot is valid
            if slot not in self.slots:
                raise EquipException("Slot not available: {}".format(slot))
        self.obj.db.slots[slot] = item

    def __len__(self):
        """Returns the number of equipped objects."""
        return len(self.obj.db.slots) - len(self.empty_slots)

    def __str__(self):
        """Shows the equipment."""
        return str(self.obj.db.slots)

    def __iter__(self):
        """Iterate over the equip in an ordered way."""
        if not self.obj.db.slots:
            return
        for slot in self.slot_order:
            yield slot, self.get(slot)

    def __contains__(self, item):
        """Implement the __contains__ method."""
        return item.id in (i.id for i
                           in self.obj.db.slots.itervalues()
                           if i)

    @property
    def slots(self):
        """Returns a list of all equipment slots."""
        return self.slot_order

    @property
    def empty_slots(self):
        """Returns a list of empty slots."""
        return [k for k, v in self if v is None]

    def isEquipped(self, checkObject):
        for slot, item in self.obj.db.slots.iteritems():
            if item == checkObject:
                return True

        return False

    def get(self, slot):
        """Return the item in the named slot."""
        if slot in self.obj.db.slots:
            return self.obj.db.slots[slot]
        else:
            return None

    def add(self, obj):
        """Add an object to character's equip.

        Args:
            obj (Equippable): the item to be equipped
        """
        # TODO: Add exceptions to return types of errors:
        # * no free slots
        # * object slot is invalid
        free_slots = [sl for sl in obj.db.slots if sl in self.empty_slots]
        if not free_slots:
            return False
        if obj.db.multi_slot:
            if len(free_slots) != len(obj.db.slots):
                return False
            for slot in free_slots:
                self._set(slot, obj)
        else:
            slot = free_slots[0]
            self._set(slot, obj)
        return True

    def remove(self, obj):
        """Remove an object from character's equip.

        Args:
            obj (Equippable): the item to be un-equipped
        """
        removed = False
        for slot, item in self:
            if item == obj:
                self._set(slot, None)
                removed = True
        return removed

    def get_stat(self, statName, inobj):
        stat = 0

        objFound = False

        for slot, obj in self:
            if (inobj is obj):
                objFound = True
                break

        if objFound == False:
            return 0

        return inobj.stats.get(statName)


    def get_total_stat(self, statName):
        totalStat = 0

        for slot, obj in self:
            if obj is not None:
                stat = self.get_stat(statName, obj)
                if stat:
                    totalStat += stat.actual

        return totalStat

    def pretty_print(self, looker, filter_stats=None, print_stats = True):
        # Get the currently equipped armor/weapons.
        data = []
        s_width = 0;

        table = EvTable("|wLimb|n",
                        "|wSlot|n",
                        "|wItem|n",
                        "|wLevel|n",
                        "|wRarity|n",
                        "|wDurability|n",
                        border = "cells")

# ISSUE 1480 - still under pull request
        if print_stats:
            table.add_column(header="|wStats|n")

        for slot, obj in self:
            wearName = slot

            if obj and not obj.access(looker, "view"):
                continue

            if not obj:
                objString = ""
                objLevel = ""
                objRarity = ""
                objDurability = ""
            else:
                # construct the string for the object.
                objString = "{name}".format(name=obj.name)
                objLevel = obj.get_level()
                objRarity = obj.get_rarity()
                objDurability = "{} %".format(obj.get_durability_percentage())

            if (self.limbs):
                # For limbs, use the named limb instead.
                for limbName, slots in self.limbs.iteritems():
                    if slot in slots: # Check if limb attached to slot
                        wearName = limbName # Set wearname to limb name.

            s_width = max(len(wearName), s_width)

            rowData = [wearName, slot, objString, objLevel, objRarity, objDurability]
            if print_stats and obj is not None:
                rowData.append(obj.pp_stats(looker=self.obj, excludeStats=["level", "rarity", "durability"]))

            table.add_row(*rowData)

#            data.append(
#                "  |b{slot:>{swidth}.{swidth}}|n: {item:<20.20}".format(
#                    slot=wearName.capitalize(),
#                    swidth=s_width,
#                    item=objName,
#                )
#            )

        return str(table)
#        if len(data) <= 0:
#            return None
#        else:
#            table = EvTable(header=False, border=None, table=[data])
#            return str(table)

