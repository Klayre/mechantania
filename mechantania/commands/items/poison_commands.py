from evennia import Command
from evennia import CmdSet

class CmdDrink(Command):
    key = "drink poison"
    aliases = ["drink"]
    locks = "cmd:all()"

    def func(self):
        # Pass the caller to the PoisonScript object
        self.obj.do_drink(self.caller)

class DefaultCmdSet(CmdSet):
    key = "PoisonCmdSet"

    def at_cmdset_creation(self):
        "Init the cmd set"
        self.add(CmdDrink)

