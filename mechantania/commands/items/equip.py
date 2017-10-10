from evennia import default_cmds
import world.rules.rules as rules

class CmdWear(default_cmds.MuxCommand):
    """ Wear an object """
    locks = "cmd:all()"
    key = "wear"
    aliases = ["equip"]


    def func(self):
        # Wears an item.
        caller = self.caller

        args = self.args.strip()
        if args:
            # Check if caller has this thing.
            obj = caller.search(
                                args,
                                candidates=caller.contents,
                                nofound_string="%s not found in inventory!" % args,
                                multimatch_string="You are carrying more than one %s: " % args)

            if not obj:
                return

            if not obj:
                caller.msg("You do not have {}".format(str(obj)))
                return
            else:
                if (not caller.equip.add(obj)) :
                    caller.msg("You can't equip that.")
                    return
                if hasattr(obj, "at_equip"):
                    obj.at_equip(caller)

                caller.msg("You equip the {}".format(str(obj)))

               
        else:
            # Display current equip

            if hasattr(caller, "equip"):
                output = caller.equip.pretty_print(caller)
                if not output:
                    caller.msg("You have nothing equipped")
                else:
                    caller.msg("|YYour equipment:|n\n{}".format(output))
                    totalStat = 0;
                    totalStat = rules.calc_effective_stat("attack", caller)
                    caller.msg("Total |rattack|n: %s" % str(totalStat))
            else:
                caller.msg("Can't display equipment.")

#            # Get the currently equipped armor/weapons.
#            if hasattr(caller.equip):
#                data = []
#                s_width = 0;
#                for slot, obj in caller.equip:
#                    wearName = slot
#
#                    if not obj or not obj.access(caller, "view"):
#                        continue
#
#                    if (caller.equip.limbs):
#                        # For limbs, use the named limb instead.
#                        for l in caller.equip.limbs:
#                            if slot in l[1]: # Check if limb attached to slot
#                                wearName = l[0] # Set wearname to limb name.
#                            
#                    s_width = max(len(wearName), s_width)
#
#                    data.append(
#                        "  |b{slot:>{swidth}.{swidth}}|n: {item:<20.20}".format(
#                            slot=wearName.capitalize(),
#                            swidth=s_width,
#                            item=obj.name,
#                        )
#                    )
#                    
#                if len(data) <= 0:
#                    output = "You have nothing equipped."
#                else:
#                    table = EvTable(header=False, border=None, table=[data])
#                    output = "|YYour equipment:|n\n{}".format(table)
#
#                caller.msg(output)
#            else:
#                caller.msg("You have no wearable slots.")

