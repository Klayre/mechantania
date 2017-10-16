import random

# We have 3 main combat characteristics calculated from the
# character, character's armor/weapons, class, passive
# abilities, etc.
# 1. nibleness - Speed of attacks, ability to flee, ability to dodge, etc.
# 2. defense - resistance to attacks
# 3. offense - strength of attacks.

# Armor could be:
# There a number of slots on a character that can contain armor.
# Each slot contributes to the nimbleness or defense of a character.
# 
# 0. None
#  * +++ nimbleness
#  * 0 defense
# 1. Light 
#  * ++ nimbleness 
#  * + defense
# 2. Medium
#  * + nimbleness
#  * ++ defense
# 3. Heavy
#  * 0 nimbleness
#  * +++ defense

# Weapons could be:
# 0. None
# 1. Martial (such as spiky gloves, or spiky feet, etc).
#  * ++++ nibleness
#  * + attack
# 2. Stab
#  * +++ nibleness
#  * ++ attack
# 3. Slice 
#  * ++ nimbleness
#  * +++ attack
# 4. Slash
#  * + nimbleness
#  * ++++ attack
# 5. Smash
#  * 0 nimbleness
#  * +++++ attack.

def calc_effective_stat(statName, char, obj=None):
    # Rule for calculating effective stat for the character from items/weapons.
    # If obj==None, then we take the TOTAL over all objects

    # TODO : Right now these are just getting total stat.  Later though,
    # we will have rules which affect how much of each stat actually gets
    # added to the character (i.e. object's level vs char's level, etc)
    if obj is None:
        return char.equip.get_total_stat(statName)
    else:
        return char.equip.get_stat(statName, obj).actual

# Following functions calculate the stat related to each.
def calc_nimbleness(char):
    # Could be affected by armor, weapon's size, etc.
    pass

def calc_defense(char):
    # Could be affected by armor, weapon's size, etc.
    pass

def calc_offense(char):
    # Could be affected by weapon's strength
    pass

def resolve_combat(combat_handler, actiondict):
    """
    This is called by the combat handler
    actiondict is a dictionary with a list of two actions
    for each character:
    {char.id:[(action1, char, target), (action2, char, target)], ...}
    """
    flee = {} # track number of flee commands per character
    for isub in range(2):
        # loop over sub-turns
        messages = []
        for subturn in (sub[isub] for sub in actiondict.values()):
            # for each character, resolve the sub-turn
            action, char, target = subturn
            if target:
                taction, tchar, ttarget = actiondict[target.id][isub]
            if action == "hit":
                if taction == "parry" and ttarget == char:
                    msg = "%s tries to hit %s, but %s parries the attack!"
                    messages.append(msg % (char, tchar, tchar))
                elif taction == "defend" and random < 0.5:
                    msg = "%s defends against the attack by %s."
                    messages.append(msg % (tchar, char))
                elif taction == "flee":
                    msg = "%s stops %s from disengaging, with a hit!"
                    flee[tchar] = -2
                    messages.append(msg % (char, tchar))
                else:
                    msg = "%s hits %s, bypassing their %s!"
                    messages.append(msg % (char, tchar, taction))
            elif action == "parry":
                if taction == "hit":
                    msg = "%s parries the attack by %s."
                    messages.append(msg % (char, tchar))
                elif taction == "feint":
                    msg = "%s tries to parry, but %s feints and hits!"
                    messages.append(msg % (char, tchar))
                else:
                    msg = "%s parries to no avail."
                    messages.append(msg % char)
            elif action == "feint":
                if taction == "parry":
                    msg = "%s feints past %s's parry, landing a hit!"
                    messages.append(msg % (char, tchar))
                elif taction == "hit":
                    msg = "%s feints but is defeated by %s hit!"
                    messages.append(msg % (char, tchar))
                else:
                    msg = "%s feints to no avail."
                    messages.append(msg % char)
            elif action == "defend":
                msg = "%s defends."
                messages.append(msg % char)
            elif action == "flee":
                if char in flee:
                    flee[char] += 1
                else:
                    flee[char] = 1
                    msg = "%s tries to disengage (two subsequent turns needed)"
                    messages.append(msg % char)

            # echo results of each subturn
            combat_handler.msg_all("\n".join(messages))

    # at the end of both sub-turns, test if anyone fled
    msg = "%s withdraws from combat."
    for (char, fleevalue) in flee.items():
        if fleevalue == 2:
            combat_handler.msg_all(msg % char)
            combat_handler.remove_character(char)
