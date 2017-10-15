# Commands related to stats

from evennia import default_cmds
import world.rules.rules as rules

class CmdStats(default_cmds.MuxCommand):
    locks = "cmd:all()"
    key = "stats"
    aliases = ["stat"]

    def func(self):
        caller = self.caller

        if self.args:
            string = "Usage: stats"
            self.caller.msg(string)
            return

        # Show the statistics for the player
        stat = rules.calc_effective_stat("attack", caller)

        caller.msg("attack stat: {}" .format(stat))


