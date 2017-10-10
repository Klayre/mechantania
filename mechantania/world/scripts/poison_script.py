from typeclasses.scripts import Script

class PoisonScript(Script):

    def at_script_creation(self):

        """
        Called when script object is first created. Sets things up.
        We want to have a lid on the button that the user can pull
        aside in order to make the button 'pressable'. But after a set
        time that lid should auto-close again, making the button safe
        from pressing (and deleting this command).
        """

        self.key = "poison_script"
        self.desc = "Script to control the poison effect on the player"
        self.interval = 5
        self.persistent = False 
        self.start_delay = True
        #self.repeats = 1

#    def is_valid(self):
#        pass
#
#    def at_start(self):
#        pass

    def at_stop(self):
        self.obj.msg("The poison wears off!")
        pass

    def at_repeat(self):
        # This is meant to be attached to the player with hp
        hp = self.obj.db.mech_character_stats_container.get_value("hp_curr")

        if (hp != None):
            hp -= 20
            self.obj.msg("%s Your body trembles as the poison courses through "
                         "your veins (HP: %s)." % (self.obj.name, hp))
            self.obj.location.msg_contents("%s shivers and doesn't look so"
                                           "good." % self.obj.name,
                                           exclude=self.obj)
            if (hp <= 0):
                hp = 100
                self.obj.msg("You DIE.  Not.")
                self.stop()

        self.obj.db.mech_character_stats_container.set_value("hp_curr", hp)



