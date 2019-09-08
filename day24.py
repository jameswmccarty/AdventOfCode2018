#!/usr/bin/python

"""
--- Day 24: Immune System Simulator 20XX ---

After a weird buzzing noise, you appear back at the man's cottage. He seems relieved to see his friend, but quickly notices that the little reindeer caught some kind of cold while out exploring.

The portly man explains that this reindeer's immune system isn't similar to regular reindeer immune systems:

The immune system and the infection each have an army made up of several groups; each group consists of one or more identical units. The armies repeatedly fight until only one army has units remaining.

Units within a group all have the same hit points (amount of damage a unit can take before it is destroyed), attack damage (the amount of damage each unit deals), an attack type, an initiative (higher initiative units attack first and win ties), and sometimes weaknesses or immunities. Here is an example group:

18 units each with 729 hit points (weak to fire; immune to cold, slashing)
 with an attack that does 8 radiation damage at initiative 10

Each group also has an effective power: the number of units in that group multiplied by their attack damage. The above group has an effective power of 18 * 8 = 144. Groups never have zero or negative units; instead, the group is removed from combat.

Each fight consists of two phases: target selection and attacking.

During the target selection phase, each group attempts to choose one target. In decreasing order of effective power, groups choose their targets; in a tie, the group with the higher initiative chooses first. The attacking group chooses to target the group in the enemy army to which it would deal the most damage (after accounting for weaknesses and immunities, but not accounting for whether the defending group has enough units to actually receive all of that damage).

If an attacking group is considering two defending groups to which it would deal equal damage, it chooses to target the defending group with the largest effective power; if there is still a tie, it chooses the defending group with the highest initiative. If it cannot deal any defending groups damage, it does not choose a target. Defending groups can only be chosen as a target by one attacking group.

At the end of the target selection phase, each group has selected zero or one groups to attack, and each group is being attacked by zero or one groups.

During the attacking phase, each group deals damage to the target it selected, if any. Groups attack in decreasing order of initiative, regardless of whether they are part of the infection or the immune system. (If a group contains no units, it cannot attack.)

The damage an attacking group deals to a defending group depends on the attacking group's attack type and the defending group's immunities and weaknesses. By default, an attacking group would deal damage equal to its effective power to the defending group. However, if the defending group is immune to the attacking group's attack type, the defending group instead takes no damage; if the defending group is weak to the attacking group's attack type, the defending group instead takes double damage.

The defending group only loses whole units from damage; damage is always dealt in such a way that it kills the most units possible, and any remaining damage to a unit that does not immediately kill it is ignored. For example, if a defending group contains 10 units with 10 hit points each and receives 75 damage, it loses exactly 7 units and is left with 3 units at full health.

After the fight is over, if both armies still contain units, a new fight begins; combat only ends once one army has lost all of its units.

For example, consider the following armies:

Immune System:
17 units each with 5390 hit points (weak to radiation, bludgeoning) with
 an attack that does 4507 fire damage at initiative 2
989 units each with 1274 hit points (immune to fire; weak to bludgeoning,
 slashing) with an attack that does 25 slashing damage at initiative 3

Infection:
801 units each with 4706 hit points (weak to radiation) with an attack
 that does 116 bludgeoning damage at initiative 1
4485 units each with 2961 hit points (immune to radiation; weak to fire,
 cold) with an attack that does 12 slashing damage at initiative 4

If these armies were to enter combat, the following fights, including details during the target selection and attacking phases, would take place:

Immune System:
Group 1 contains 17 units
Group 2 contains 989 units
Infection:
Group 1 contains 801 units
Group 2 contains 4485 units

Infection group 1 would deal defending group 1 185832 damage
Infection group 1 would deal defending group 2 185832 damage
Infection group 2 would deal defending group 2 107640 damage
Immune System group 1 would deal defending group 1 76619 damage
Immune System group 1 would deal defending group 2 153238 damage
Immune System group 2 would deal defending group 1 24725 damage

Infection group 2 attacks defending group 2, killing 84 units
Immune System group 2 attacks defending group 1, killing 4 units
Immune System group 1 attacks defending group 2, killing 51 units
Infection group 1 attacks defending group 1, killing 17 units

Immune System:
Group 2 contains 905 units
Infection:
Group 1 contains 797 units
Group 2 contains 4434 units

Infection group 1 would deal defending group 2 184904 damage
Immune System group 2 would deal defending group 1 22625 damage
Immune System group 2 would deal defending group 2 22625 damage

Immune System group 2 attacks defending group 1, killing 4 units
Infection group 1 attacks defending group 2, killing 144 units

Immune System:
Group 2 contains 761 units
Infection:
Group 1 contains 793 units
Group 2 contains 4434 units

Infection group 1 would deal defending group 2 183976 damage
Immune System group 2 would deal defending group 1 19025 damage
Immune System group 2 would deal defending group 2 19025 damage

Immune System group 2 attacks defending group 1, killing 4 units
Infection group 1 attacks defending group 2, killing 143 units

Immune System:
Group 2 contains 618 units
Infection:
Group 1 contains 789 units
Group 2 contains 4434 units

Infection group 1 would deal defending group 2 183048 damage
Immune System group 2 would deal defending group 1 15450 damage
Immune System group 2 would deal defending group 2 15450 damage

Immune System group 2 attacks defending group 1, killing 3 units
Infection group 1 attacks defending group 2, killing 143 units

Immune System:
Group 2 contains 475 units
Infection:
Group 1 contains 786 units
Group 2 contains 4434 units

Infection group 1 would deal defending group 2 182352 damage
Immune System group 2 would deal defending group 1 11875 damage
Immune System group 2 would deal defending group 2 11875 damage

Immune System group 2 attacks defending group 1, killing 2 units
Infection group 1 attacks defending group 2, killing 142 units

Immune System:
Group 2 contains 333 units
Infection:
Group 1 contains 784 units
Group 2 contains 4434 units

Infection group 1 would deal defending group 2 181888 damage
Immune System group 2 would deal defending group 1 8325 damage
Immune System group 2 would deal defending group 2 8325 damage

Immune System group 2 attacks defending group 1, killing 1 unit
Infection group 1 attacks defending group 2, killing 142 units

Immune System:
Group 2 contains 191 units
Infection:
Group 1 contains 783 units
Group 2 contains 4434 units

Infection group 1 would deal defending group 2 181656 damage
Immune System group 2 would deal defending group 1 4775 damage
Immune System group 2 would deal defending group 2 4775 damage

Immune System group 2 attacks defending group 1, killing 1 unit
Infection group 1 attacks defending group 2, killing 142 units

Immune System:
Group 2 contains 49 units
Infection:
Group 1 contains 782 units
Group 2 contains 4434 units

Infection group 1 would deal defending group 2 181424 damage
Immune System group 2 would deal defending group 1 1225 damage
Immune System group 2 would deal defending group 2 1225 damage

Immune System group 2 attacks defending group 1, killing 0 units
Infection group 1 attacks defending group 2, killing 49 units

Immune System:
No groups remain.
Infection:
Group 1 contains 782 units
Group 2 contains 4434 units

In the example above, the winning army ends up with 782 + 4434 = 5216 units.

You scan the reindeer's condition (your puzzle input); the white-bearded man looks nervous. As it stands now, how many units would the winning army have?

--- Part Two ---

Things aren't looking good for the reindeer. The man asks whether more milk and cookies would help you think.

If only you could give the reindeer's immune system a boost, you might be able to change the outcome of the combat.

A boost is an integer increase in immune system units' attack damage. For example, if you were to boost the above example's immune system's units by 1570, the armies would instead look like this:

Immune System:
17 units each with 5390 hit points (weak to radiation, bludgeoning) with
 an attack that does 6077 fire damage at initiative 2
989 units each with 1274 hit points (immune to fire; weak to bludgeoning,
 slashing) with an attack that does 1595 slashing damage at initiative 3

Infection:
801 units each with 4706 hit points (weak to radiation) with an attack
 that does 116 bludgeoning damage at initiative 1
4485 units each with 2961 hit points (immune to radiation; weak to fire,
 cold) with an attack that does 12 slashing damage at initiative 4

With this boost, the combat proceeds differently:

Immune System:
Group 2 contains 989 units
Group 1 contains 17 units
Infection:
Group 1 contains 801 units
Group 2 contains 4485 units

Infection group 1 would deal defending group 2 185832 damage
Infection group 1 would deal defending group 1 185832 damage
Infection group 2 would deal defending group 1 53820 damage
Immune System group 2 would deal defending group 1 1577455 damage
Immune System group 2 would deal defending group 2 1577455 damage
Immune System group 1 would deal defending group 2 206618 damage

Infection group 2 attacks defending group 1, killing 9 units
Immune System group 2 attacks defending group 1, killing 335 units
Immune System group 1 attacks defending group 2, killing 32 units
Infection group 1 attacks defending group 2, killing 84 units

Immune System:
Group 2 contains 905 units
Group 1 contains 8 units
Infection:
Group 1 contains 466 units
Group 2 contains 4453 units

Infection group 1 would deal defending group 2 108112 damage
Infection group 1 would deal defending group 1 108112 damage
Infection group 2 would deal defending group 1 53436 damage
Immune System group 2 would deal defending group 1 1443475 damage
Immune System group 2 would deal defending group 2 1443475 damage
Immune System group 1 would deal defending group 2 97232 damage

Infection group 2 attacks defending group 1, killing 8 units
Immune System group 2 attacks defending group 1, killing 306 units
Infection group 1 attacks defending group 2, killing 29 units

Immune System:
Group 2 contains 876 units
Infection:
Group 2 contains 4453 units
Group 1 contains 160 units

Infection group 2 would deal defending group 2 106872 damage
Immune System group 2 would deal defending group 2 1397220 damage
Immune System group 2 would deal defending group 1 1397220 damage

Infection group 2 attacks defending group 2, killing 83 units
Immune System group 2 attacks defending group 2, killing 427 units

After a few fights...

Immune System:
Group 2 contains 64 units
Infection:
Group 2 contains 214 units
Group 1 contains 19 units

Infection group 2 would deal defending group 2 5136 damage
Immune System group 2 would deal defending group 2 102080 damage
Immune System group 2 would deal defending group 1 102080 damage

Infection group 2 attacks defending group 2, killing 4 units
Immune System group 2 attacks defending group 2, killing 32 units

Immune System:
Group 2 contains 60 units
Infection:
Group 1 contains 19 units
Group 2 contains 182 units

Infection group 1 would deal defending group 2 4408 damage
Immune System group 2 would deal defending group 1 95700 damage
Immune System group 2 would deal defending group 2 95700 damage

Immune System group 2 attacks defending group 1, killing 19 units

Immune System:
Group 2 contains 60 units
Infection:
Group 2 contains 182 units

Infection group 2 would deal defending group 2 4368 damage
Immune System group 2 would deal defending group 2 95700 damage

Infection group 2 attacks defending group 2, killing 3 units
Immune System group 2 attacks defending group 2, killing 30 units

After a few more fights...

Immune System:
Group 2 contains 51 units
Infection:
Group 2 contains 40 units

Infection group 2 would deal defending group 2 960 damage
Immune System group 2 would deal defending group 2 81345 damage

Infection group 2 attacks defending group 2, killing 0 units
Immune System group 2 attacks defending group 2, killing 27 units

Immune System:
Group 2 contains 51 units
Infection:
Group 2 contains 13 units

Infection group 2 would deal defending group 2 312 damage
Immune System group 2 would deal defending group 2 81345 damage

Infection group 2 attacks defending group 2, killing 0 units
Immune System group 2 attacks defending group 2, killing 13 units

Immune System:
Group 2 contains 51 units
Infection:
No groups remain.

This boost would allow the immune system's armies to win! It would be left with 51 units.

You don't even know how you could boost the reindeer's immune system or what effect it might have, so you need to be cautious and find the smallest boost that would allow the immune system to win.

How many units does the immune system have left after getting the smallest boost it needs to win?

"""

damages = {	'radiation'	: 1,
			'bludgeoning' : 2,
			'slashing' : 3,
			'fire' : 4,
			'cold' : 5}

max_initiative = None

class Group:

	def __init__(self, N, hp, damage, attack_type, initiative, immune, weak):
		global max_initiative
		self.num_units = N
		self.hp = hp
		self.damage_dealt = damage
		self.damage = damages[attack_type]
		self.weak = [ damages[i] for i in weak ]
		self.initiative = initiative
		self.immune = [ damages[i] for i in immune ]
		self.target = None
		self.active = True
		max_initiative = max(max_initiative, self.initiative)

	def takeDamage(self, points):
		self.num_units -= (points / self.hp)
		if self.num_units <= 0:
			self.num_units = 0 
			self.active = False

	def getEffectivePower(self):
		return self.num_units * self.damage_dealt

	def getInitiative(self):
		return self.initiative

	def damageEstimate(self, opponent):
		if not opponent.active:
			return 0
		base = self.getEffectivePower()
		if self.damage in opponent.immune:
			return 0
		if self.damage in opponent.weak:
			return 2 * base
		return base

	def attack(self, opponent):
		if self.active:
			#print self.damageEstimate(opponent), min(self.damageEstimate(opponent) / opponent.hp, opponent.num_units)
			opponent.takeDamage(self.damageEstimate(opponent))		

class Army:

	def __init__(self):
		self.groups = []

	def unitCount(self):
		return sum( x.num_units for x in self.groups )

	def battleOrder(self):
		# sort by Effective Power, ties broken by Initiative
		self.groups = sorted(self.groups, key = lambda x : (x.getEffectivePower(), max_initiative - x.getInitiative()), reverse=True)

	def targetSelect(self, opponentArmy):
		availTargets = []
		for i, group in enumerate(opponentArmy.groups):
			if group.active:
				availTargets.append(i)
		for group in self.groups:
			group.target = None
			high = (0, 0, -1)
			highidx = None
			for idx in availTargets:
				damage = group.damageEstimate(opponentArmy.groups[idx])
				if damage > high[0]:
					high = (damage, opponentArmy.groups[idx].getEffectivePower(), opponentArmy.groups[idx].getInitiative())
					highidx = idx
				elif damage == high[0] and high[0] > 0:
					if opponentArmy.groups[idx].getEffectivePower() > high[1]:
						high = (damage, opponentArmy.groups[idx].getEffectivePower(), opponentArmy.groups[idx].getInitiative())
						highidx = idx
					elif opponentArmy.groups[idx].getEffectivePower() == high[1]:
						if opponentArmy.groups[idx].getInitiative() < high[2]:
							high = (damage, opponentArmy.groups[idx].getEffectivePower(), opponentArmy.groups[idx].getInitiative())
							highidx = idx
			if highidx != None:
				group.target = highidx
				availTargets.remove(highidx)		

	def spawnGroup(self, N, hp, damage, attack_type, initiative, immune, weak):
		self.groups.append(Group(N, hp, damage, attack_type, initiative, immune, weak))

	def printGroups(self):
		for i, group in enumerate(self.groups):
			print "Group", i+1, "contains", group.num_units, "units with", group.hp, "hit points."
			print "  Effective power is: ", group.getEffectivePower(), "Attack type: ", group.damage
			print "  Weak: ", group.weak, "Immune: ", group.immune, "Initiative: ", group.initiative

def parse(line, target_army, boost=0):
	weak_immune = ''
	weak = ''
	immune = ''
	attack = ''
	if "(" in line:
		outer = line[0:line.index("(")-1] + line[line.index(")")+1:]
		inner = line[line.index("(")+1:line.index(")")]
	else:
		inner = ''
		outer = line
	if len(inner) > 0:
		parts = inner.split("; ")
		for part in parts:
			if "weak to " in part:
				part = part.replace("weak to ", '')
				weak = part.split(", ")
			elif "immune to ":
				part = part.replace("immune to ", '')
				immune = part.split(", ")
	outer = outer.split(" ")
	num = int(outer[0])
	hp  = int(outer[4])
	damage  = int(outer[12])+boost
	attack = outer[13]
	initiative = int(outer[-1])

	#print num, hp, damage, attack, initiative, weak, immune
	target_army.spawnGroup(num, hp, damage, attack, initiative, immune, weak)	
	

if __name__ == "__main__":

	# Part 1 Solution

	armies = []

	with open('day24_input', 'r') as infile:
		for line in infile.readlines():
			if ':' in line:
				current_army = Army()
			elif len(line.strip()) == 0:
				armies.append(current_army)
			else:
				parse(line.strip(), current_army)
		armies.append(current_army)

	endgame = False

	while not endgame:

		#for army in armies:
		#	army.printGroups()

		endgame = False
		for army in armies:
			if army.unitCount() == 0:
				endgame = True
				break
		if endgame:
			break

		# Target Selection

		armies[0].battleOrder()
		armies[1].battleOrder()
		armies[0].targetSelect(armies[1])
		armies[1].targetSelect(armies[0])

		# Attack Stage

		attack_order = []
		for i, group in enumerate(armies[0].groups):
			if group.active:
				attack_order.append( (group.getInitiative(), 1, i+1, group.target) )
		for i, group in enumerate(armies[1].groups):
			if group.active:
				attack_order.append( (group.getInitiative(), 2, i+1, group.target) )
		
		attack_order.sort(reverse=True)
		#print attack_order
		for entry in attack_order:
			initiative, army_idx, group_idx, targetID = entry
			if targetID != None:
				armies[army_idx-1].groups[group_idx-1].attack(armies[(army_idx%2)].groups[targetID])

	print armies[0].unitCount() + armies[1].unitCount()

	# Part 2 Solution
	# 3959 too high

	global_boost = -1
	enemywon  = True
	
	while enemywon:

		round_boost = global_boost + 1
		global_boost += 1

		armies = []

		#print "Round Boost: ", round_boost

		with open('day24_input', 'r') as infile:
			for line in infile.readlines():
				if ':' in line:
					current_army = Army()
				elif len(line.strip()) == 0:
					armies.append(current_army)
					round_boost = 0
				else:
					parse(line.strip(), current_army, round_boost)
			armies.append(current_army)

		endgame = False

		while not endgame:

			#for army in armies:
			#	army.printGroups()

			endgame = False
			for army in armies:
				if army.unitCount() == 0:
					endgame = True
					break
			if endgame:
				break

			# Stalemate detection
			start_units = (armies[0].unitCount() + armies[1].unitCount())

			# Target Selection

			armies[0].battleOrder()
			armies[1].battleOrder()
			armies[0].targetSelect(armies[1])
			armies[1].targetSelect(armies[0])

			# Attack Stage

			attack_order = []
			for i, group in enumerate(armies[0].groups):
				if group.active:
					attack_order.append( (group.getInitiative(), 1, i+1, group.target) )
			for i, group in enumerate(armies[1].groups):
				if group.active:
					attack_order.append( (group.getInitiative(), 2, i+1, group.target) )
			
			attack_order.sort(reverse=True)
			#print attack_order
			for entry in attack_order:
				initiative, army_idx, group_idx, targetID = entry
				if targetID != None:
					armies[army_idx-1].groups[group_idx-1].attack(armies[(army_idx%2)].groups[targetID])

			if start_units == (armies[0].unitCount() + armies[1].unitCount()):
				endgame = True

		if (armies[1].unitCount() > 0):
			enemywon = True
		else:
			enemywon = False

	print armies[0].unitCount()

	
	

	
				
				

	
	
