from evennia import Command
from evennia import create_script
from evennia import default_cmds
from evennia.commands.cmdset import CmdSet
from evennia.commands.default import help

# Commands
# Attack commands
# Hit (weapon type slice, slash, etc)
## Physical attack
#
# Misc commands
## Target <enemy 1> <enemy 2>, etc
### Doesn't take a turn
#
## Flee
### Take a chance to flee from combat.  Opponents won't be able
### to attack you for 10 seconds.
## Backout
### Debug command to end the fight.


class CmdHit(Command):
    """
    hit an enemy
    
    usage:
        hit <target>

    Strikes the given enemy with your current weapon.
    """
    key = "hit"
    aliases = ["strike", "slash"]
    help_category = "combat"

    def func(self):
        "Implements the command"
#        if not self.args:
#            self.caller.msg("Usage: hit <target>")
#            return
#        target = self.caller.search(self.args)
#        if not target:
#            return
        ok = self.caller.ndb.combat_handler.add_action("hit",
                                                        self.caller)
        if not ok:
            self.caller.msg("You cannot {0}".format(self.key))

#        # tell the handler to check if turn is over
#        self.caller.ndb.combat_handler.check_end_turn()


#class CmdParry(Command):
#    """
#    parry an enemy
#    
#    usage:
#        parry <target>
#
#    Strikes the given enemy with your current weapon.
#    """
#    key = "parry"
#    help_category = "combat"
#
#    def func(self):
#        "Implements the command"
#        if not self.args:
#            self.caller.msg("Usage: parry <target>")
#            return
#        target = self.caller.search(self.args)
#        if not target:
#            return
#        ok = self.caller.ndb.combat_handler.add_action("parry",
#                                                       self.caller,
#                                                       target)
#
#        if ok:
#            self.caller.msg("You add 'parry' to the combat queue")
#        else:
#            self.caller.msg("You can only queue two actions per turn!")
#
#        # tell the handler to check if turn is over
#        self.caller.ndb.combat_handler.check_end_turn()
#
#class CmdFeint(Command):
#    """
#    feint an enemy
#    
#    usage:
#        feint <target>
#
#    Strikes the given enemy with your current weapon.
#    """
#    key = "feint"
#    help_category = "combat"
#
#    def func(self):
#        "Implements the command"
#        if not self.args:
#            self.caller.msg("Usage: feint <target>")
#            return
#        target = self.caller.search(self.args)
#        if not target:
#            return
#        ok = self.caller.ndb.combat_handler.add_action("feint",
#                                                       self.caller,
#                                                       target)
#
#        if ok:
#            self.caller.msg("You add 'feint' to the combat queue")
#        else:
#            self.caller.msg("You can only queue two actions per turn!")
#
#        # tell the handler to check if turn is over
#        self.caller.ndb.combat_handler.check_end_turn()
#
#
#class CmdDefend(Command):
#    """
#    defend an enemy
#    
#    usage:
#        defend <target>
#
#    Strikes the given enemy with your current weapon.
#    """
#    key = "defend"
#    help_category = "combat"
#
#    def func(self):
#        "Implements the command"
#        if not self.args:
#            self.caller.msg("Usage: defend <target>")
#            return
#        target = self.caller.search(self.args)
#        if not target:
#            return
#        ok = self.caller.ndb.combat_handler.add_action("defend",
#                                                       self.caller,
#                                                       target)
#
#        if ok:
#            self.caller.msg("You add 'defend' to the combat queue")
#        else:
#            self.caller.msg("You can only queue two actions per turn!")
#
#        # tell the handler to check if turn is over
#        self.caller.ndb.combat_handler.check_end_turn()
#
#class CmdDefend(Command):
#    """
#    defend an enemy
#    
#    usage:
#        defend <target>
#
#    Strikes the given enemy with your current weapon.
#    """
#    key = "defend"
#    help_category = "combat"
#
#    def func(self):
#        "Implements the command"
#        if not self.args:
#            self.caller.msg("Usage: defend <target>")
#            return
#        target = self.caller.search(self.args)
#        if not target:
#            return
#        ok = self.caller.ndb.combat_handler.add_action("defend",
#                                                       self.caller,
#                                                       target)
#
#        if ok:
#            self.caller.msg("You add 'defend' to the combat queue")
#        else:
#            self.caller.msg("You can only queue two actions per turn!")
#
#        # tell the handler to check if turn is over
#        self.caller.ndb.combat_handler.check_end_turn()
#
#class CmdDisengage(Command):
#    """
#    disengage an enemy
#    
#    usage:
#        disengage <target>
#
#    Strikes the given enemy with your current weapon.
#    """
#    key = "disengage"
#    help_category = "combat"
#
#    def func(self):
#        "Implements the command"
#
#        if not self.args:
#            self.caller.msg("Usage: disengage <target>")
#            return
#        target = self.caller.search(self.args)
#        if not target:
#            return
#        ok = self.caller.ndb.combat_handler.add_action("disengage",
#                                                       self.caller,
#                                                       target)
#
#        if ok:
#            self.caller.msg("You add 'disengage' to the combat queue")
#        else:
#            self.caller.msg("You can only queue two actions per turn!")
#
#        # tell the handler to check if turn is over
#        self.caller.ndb.combat_handler.check_end_turn()

class CmdBackout(Command):
    """
    Backs out of combat.

    usage:
        backout

    USED ONLY FOR TESTING.
    Will remove the character from the combat handler.
    """
    key = "backout"
    help_category = "combat"

    def func(self):
        self.caller.msg("You backout from combat...")
        self.caller.ndb.combat_handler.remove_character(self.caller)

class CombatCmdSet(CmdSet):
    key = "combat_cmdset"
    mergetype = "Replace"
    priority = 10
    no_exits = True

    def at_cmdset_creation(self):
        self.add(CmdHit())
#        self.add(CmdParry())
#        self.add(CmdFeint())
#        self.add(CmdDefend())
#        self.add(CmdDisengage())
        self.add(CmdBackout())
        self.add(default_cmds.CmdPose())
        self.add(default_cmds.CmdSay())
        self.add(default_cmds.CmdHelp())

        # The help system
        self.add(help.CmdHelp())
        self.add(help.CmdSetHelp())

class CmdAttack(Command):
    """
    initiates combat

    Usage:
      attack <target>

    This will initiate combat with <target>. If <target is
    already in combat, you will join the combat. 
    """
    key = "attack"
    help_category = "General"

    def func(self):
        "Handle command"
        if not self.args:
            self.caller.msg("Usage: attack <target>")            
            return
        target = self.caller.search(self.args)
        if not target:
            return
        # set up combat
        if target.ndb.combat_handler:
            # target is already in combat - join it            
            target.ndb.combat_handler.add_character(self.caller)
            target.ndb.combat_handler.msg_all("%s joins combat!" % self.caller)
        else:
            # create a new combat handler
            # TODO Change path of this..
            chandler = create_script("mscripts.combat.combat_handler.CombatHandler")
            chandler.add_character(self.caller)
            chandler.add_character(target)
            self.caller.msg("You attack %s! You are in combat." % target)
            target.msg("%s attacks you! You are in combat." % self.caller)  
