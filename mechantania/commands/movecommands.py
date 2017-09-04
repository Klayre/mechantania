from evennia import default_cmds

class CmdExitError(default_cmds.MuxCommand):
    " Parent class for all exit errors "
    locks = "cmd:all()"
    arg_regex = r"\s|$"
    auto_help = False
    def func(self):
        "returns the error"
        self.caller.msg("You cannot move %s." % self.key)

class CmdExitErrorNorth(CmdExitError):
    key = "north"
    aliases = ["n"]

class CmdExitErrorWest(CmdExitError):
    key = "west"
    aliases = ["w"]

class CmdExitErrorEast(CmdExitError):
    key = "east"
    aliases = ["e"]

class CmdExitErrorSouth(CmdExitError):
    key = "south"
    aliases = ["s"]


class CmdExitErrorSouthEast(CmdExitError):
    key = "southeast"
    aliases = ["se"]
class CmdExitErrorNorthEast(CmdExitError):
    key = "ne"
    aliases = ["ne"]
class CmdExitErrorNorthWest(CmdExitError):
    key = "nw"
    aliases = ["nw"]
class CmdExitErrorSouthWest(CmdExitError):
    key = "southwest"
    aliases = ["sw"]
