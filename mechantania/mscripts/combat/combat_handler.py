import random
from typeclasses.scripts import Script

# Todo: automatically target when only two characters 
class CombatHandler(Script):
    """
    This implements the combat handler.
    """

    # standard Script hooks 

    def at_script_creation(self):
        "Called when script is first created"

        self.key = "combat_handler_%i" % random.randint(1, 1000)
        self.desc = "handles combat"
        self.interval = 60 * 2  # two minute timeout
        self.start_delay = True
        self.persistent = True   

        # store all combatants
        # A dict of dbref : character object
        self.db.characters = {}

        # A dict of dbref : [ targets ]
        self.ndb.targets = {}

        # Character battle queue.  First one in queue gets to go next.
        self.db.characterQueue = []

#        # store all actions for each turn
#        self.db.turn_actions = {}
#        # number of actions entered per combatant
#        self.db.action_count = {}

    def _init_character(self, character):
        """
        This initializes handler back-reference 
        and combat cmdset on a character
        """
        character.ndb.combat_handler = self
        character.cmdset.add("commands.combat.combat.CombatCmdSet")

    def _cleanup_character(self, character):
        """
        Remove character from handler and clean 
        it of the back-reference and cmdset
        """
        dbref = character.id 
        del self.db.characters[dbref]
        del self.ndb.targets[dbref]

        # Remove character from queue
        if dbref in self.db.characterQueue:
            self.db.characterQueue.remove(dbref)

#        del self.db.turn_actions[dbref]
#        del self.db.action_count[dbref]        
        del character.ndb.combat_handler
        character.cmdset.delete("commands.combat.combat.CombatCmdSet")
        character.msg("|yYour battle is over.|n")

    # Gets the next dbref after this one in the characters list.
    def _get_next_dbref_in_queue(self):
        # Pop off the top, then push onto back
        charTurn = self.db.characterQueue.pop(0)

        self.db.characterQueue.append(charTurn)

        print(self.db.characterQueue)
        return charTurn

    def at_start(self):
        """
        This is called on first start but also when the script is restarted
        after a server reboot. We need to re-assign this combat handler to 
        all characters as well as re-assign the cmdset.
        """
        for character in self.db.characters.values():
            self._init_character(character)

        # Select a random character for turn

    def at_stop(self):
        "Called just before the script is stopped/destroyed."
        for character in list(self.db.characters.values()):
            # note: the list() call above disconnects list from database
            self._cleanup_character(character)

    def at_repeat(self):
        """
        This is called every self.interval seconds (turn timeout) or 
        when force_repeat is called (because everyone has entered their 
        commands). We know this by checking the existence of the
        `normal_turn_end` NAttribute, set just before calling 
        force_repeat.
        
        """
        if self.ndb.normal_turn_end:
            # we get here because the turn ended normally
            # (force_repeat was called) - no msg output
            del self.ndb.normal_turn_end
        else:        
            # turn timeout
            self.msg_all("Turn timer timed out. Continuing.")
        self.end_turn()

    # Combat-handler methods

    def add_character(self, character):
        "Add combatant to handler"
        dbref = character.id
        self.db.characters[dbref] = character        
        self.ndb.targets[dbref] = []
        self.db.characterQueue.append(character.id)

        self._init_character(character)
       
    def remove_character(self, character):
        "Remove combatant from handler"
        if character.id in self.db.characters:
            # Cleanup the character, deleting entries.
            self._cleanup_character(character)
        if not self.db.characters or len(self.db.characters) < 2:
            # if no more characters in battle, kill this handler
            self.stop()

    def msg_all(self, message):
        "Send message to all combatants"
        for character in self.db.characters.values():
            character.msg(message)

    def add_action(self, action, character):
        """
        Called by combat commands to perform an action.

        If it is not character's turn, this command will do nothing.
        If it is character's turn, this function will attempt to
        perform the action on the character's selected targets.

         action - string identifying the action, like "hit" or "parry"
         character - the character performing the action
         target - the target character or None

        actions are stored in a dictionary keyed to each character, each
        of which holds a list of max 2 actions. An action is stored as
        a tuple (character, action, target). 
        """
        dbref = character.id

        retMsg = ""

        targetId = None

        # Check if this character's turn.
        if (self.db.characterQueue[0] != character.id):
            character.msg( "It's not your turn...")
            return False

        if len(self.ndb.targets) == 0 or len(self.ndb.targets[character.id]) == 0:
            # TODO: Maybe have a function for each action type to pick the
            # targets.  AOE spells might not require a single target.
            # No targets, so pick one at random (excluding the character
            # obviously)
            potentialTargets = \
                    [char for char in self.db.characters.values() if char != character]
            randTarget = random.choice(potentialTargets)
            targetId = randTarget.id

            retMsg += "You are not targetting anyone, so targetting {target} " \
            "at random.\n".format(target=randTarget)
        else:
            if character.id in self.ndb.targets:
                targetId = self.ndb.targets[character.id][0]

        if targetId == None:
            character.msg( "|rERROR: |n problems finding a suitable target.")
            return False
        if targetId not in self.db.characters:
            character.msg( "|rERROR: |n Target is not in list of combatants!")
            return False

        targetChar = self.db.characters[targetId]
        retMsg += "You {action} {target}".format(action=action,
                                                 target=targetChar)
        character.msg(retMsg) 
        self.end_turn()

        return True

    def end_turn(self):
        """
        This resolves all actions by calling the rules module. 
        It then resets everything and starts the next turn. It
        is called by at_repeat().
        """        
#        resolve_combat(self, self.db.turn_actions)

        if len(self.db.characters) < 2:
            # less than 2 characters in battle, kill this handler
            self.msg_all("Combat has ended")
            self.stop()
        else:
            # reset counters before next turn
            for character in self.db.characters.values():
                self.db.characters[character.id] = character

                # cycle to next turn.
                self._get_next_dbref_in_queue()
#                self.db.action_count[character.id] = 0
#                self.db.turn_actions[character.id] = [("defend", character, None),
#                                                  ("defend", character, None)]
        self.msg_all("It is now {char}'s turn \
                     ...".format(char = \
                                 self.db.characters[self.db.characterQueue[0]]))


