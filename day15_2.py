#!/usr/bin/python

from collections import deque

"""
--- Day 15: Beverage Bandits ---

Having perfected their hot chocolate, the Elves have a new problem: the Goblins that live in these caves will do anything to steal it. Looks like they're here for a fight.

You scan the area, generating a map of the walls (#), open cavern (.), and starting position of every Goblin (G) and Elf (E) (your puzzle input).

Combat proceeds in rounds; in each round, each unit that is still alive takes a turn, resolving all of its actions before the next unit's turn begins. On each unit's turn, it tries to move into range of an enemy (if it isn't already) and then attack (if it is in range).

All units are very disciplined and always follow very strict combat rules. Units never move or attack diagonally, as doing so would be dishonorable. When multiple choices are equally valid, ties are broken in reading order: top-to-bottom, then left-to-right. For instance, the order in which units take their turns within a round is the reading order of their starting positions in that round, regardless of the type of unit or whether other units have moved after the round started. For example:

                 would take their
These units:   turns in this order:
  #######           #######
  #.G.E.#           #.1.2.#
  #E.G.E#           #3.4.5#
  #.G.E.#           #.6.7.#
  #######           #######

Each unit begins its turn by identifying all possible targets (enemy units). If no targets remain, combat ends.

Then, the unit identifies all of the open squares (.) that are in range of each target; these are the squares which are adjacent (immediately up, down, left, or right) to any target and which aren't already occupied by a wall or another unit. Alternatively, the unit might already be in range of a target. If the unit is not already in range of a target, and there are no open squares which are in range of a target, the unit ends its turn.

If the unit is already in range of a target, it does not move, but continues its turn with an attack. Otherwise, since it is not in range of a target, it moves.

To move, the unit first considers the squares that are in range and determines which of those squares it could reach in the fewest steps. A step is a single movement to any adjacent (immediately up, down, left, or right) open (.) square. Units cannot move into walls or other units. The unit does this while considering the current positions of units and does not do any prediction about where units will be later. If the unit cannot reach (find an open path to) any of the squares that are in range, it ends its turn. If multiple squares are in range and tied for being reachable in the fewest steps, the step which is first in reading order is chosen. For example:

Targets:      In range:     Reachable:    Nearest:      Chosen:
#######       #######       #######       #######       #######
#E..G.#       #E.?G?#       #E.@G.#       #E.!G.#       #E.+G.#
#...#.#  -->  #.?.#?#  -->  #.@.#.#  -->  #.!.#.#  -->  #...#.#
#.G.#G#       #?G?#G#       #@G@#G#       #!G.#G#       #.G.#G#
#######       #######       #######       #######       #######

In the above scenario, the Elf has three targets (the three Goblins):

    Each of the Goblins has open, adjacent squares which are in range (marked with a ? on the map).
    Of those squares, four are reachable (marked @); the other two (on the right) would require moving through a wall or unit to reach.
    Three of these reachable squares are nearest, requiring the fewest steps (only 2) to reach (marked !).
    Of those, the square which is first in reading order is chosen (+).

The unit then takes a single step toward the chosen square along the shortest path to that square. If multiple steps would put the unit equally closer to its destination, the unit chooses the step which is first in reading order. (This requires knowing when there is more than one shortest path so that you can consider the first step of each such path.) For example:

In range:     Nearest:      Chosen:       Distance:     Step:
#######       #######       #######       #######       #######
#.E...#       #.E...#       #.E...#       #4E212#       #..E..#
#...?.#  -->  #...!.#  -->  #...+.#  -->  #32101#  -->  #.....#
#..?G?#       #..!G.#       #...G.#       #432G2#       #...G.#
#######       #######       #######       #######       #######

The Elf sees three squares in range of a target (?), two of which are nearest (!), and so the first in reading order is chosen (+). Under "Distance", each open square is marked with its distance from the destination square; the two squares to which the Elf could move on this turn (down and to the right) are both equally good moves and would leave the Elf 2 steps from being in range of the Goblin. Because the step which is first in reading order is chosen, the Elf moves right one square.

Here's a larger example of movement:

Initially:
#########
#G..G..G#
#.......#
#.......#
#G..E..G#
#.......#
#.......#
#G..G..G#
#########

After 1 round:
#########
#.G...G.#
#...G...#
#...E..G#
#.G.....#
#.......#
#G..G..G#
#.......#
#########

After 2 rounds:
#########
#..G.G..#
#...G...#
#.G.E.G.#
#.......#
#G..G..G#
#.......#
#.......#
#########

After 3 rounds:
#########
#.......#
#..GGG..#
#..GEG..#
#G..G...#
#......G#
#.......#
#.......#
#########

Once the Goblins and Elf reach the positions above, they all are either in range of a target or cannot find any square in range of a target, and so none of the units can move until a unit dies.

After moving (or if the unit began its turn in range of a target), the unit attacks.

To attack, the unit first determines all of the targets that are in range of it by being immediately adjacent to it. If there are no such targets, the unit ends its turn. Otherwise, the adjacent target with the fewest hit points is selected; in a tie, the adjacent target with the fewest hit points which is first in reading order is selected.

The unit deals damage equal to its attack power to the selected target, reducing its hit points by that amount. If this reduces its hit points to 0 or fewer, the selected target dies: its square becomes . and it takes no further turns.

Each unit, either Goblin or Elf, has 3 attack power and starts with 200 hit points.

For example, suppose the only Elf is about to attack:

       HP:            HP:
G....  9       G....  9  
..G..  4       ..G..  4  
..EG.  2  -->  ..E..     
..G..  2       ..G..  2  
...G.  1       ...G.  1  

The "HP" column shows the hit points of the Goblin to the left in the corresponding row. The Elf is in range of three targets: the Goblin above it (with 4 hit points), the Goblin to its right (with 2 hit points), and the Goblin below it (also with 2 hit points). Because three targets are in range, the ones with the lowest hit points are selected: the two Goblins with 2 hit points each (one to the right of the Elf and one below the Elf). Of those, the Goblin first in reading order (the one to the right of the Elf) is selected. The selected Goblin's hit points (2) are reduced by the Elf's attack power (3), reducing its hit points to -1, killing it.

After attacking, the unit's turn ends. Regardless of how the unit's turn ends, the next unit in the round takes its turn. If all units have taken turns in this round, the round ends, and a new round begins.

The Elves look quite outnumbered. You need to determine the outcome of the battle: the number of full rounds that were completed (not counting the round in which combat ends) multiplied by the sum of the hit points of all remaining units at the moment combat ends. (Combat only ends when a unit finds no targets during its turn.)

Below is an entire sample combat. Next to each map, each row's units' hit points are listed from left to right.

Initially:
#######   
#.G...#   G(200)
#...EG#   E(200), G(200)
#.#.#G#   G(200)
#..G#E#   G(200), E(200)
#.....#   
#######   

After 1 round:
#######   
#..G..#   G(200)
#...EG#   E(197), G(197)
#.#G#G#   G(200), G(197)
#...#E#   E(197)
#.....#   
#######   

After 2 rounds:
#######   
#...G.#   G(200)
#..GEG#   G(200), E(188), G(194)
#.#.#G#   G(194)
#...#E#   E(194)
#.....#   
#######   

Combat ensues; eventually, the top Elf dies:

After 23 rounds:
#######   
#...G.#   G(200)
#..G.G#   G(200), G(131)
#.#.#G#   G(131)
#...#E#   E(131)
#.....#   
#######   

After 24 rounds:
#######   
#..G..#   G(200)
#...G.#   G(131)
#.#G#G#   G(200), G(128)
#...#E#   E(128)
#.....#   
#######   

After 25 rounds:
#######   
#.G...#   G(200)
#..G..#   G(131)
#.#.#G#   G(125)
#..G#E#   G(200), E(125)
#.....#   
#######   

After 26 rounds:
#######   
#G....#   G(200)
#.G...#   G(131)
#.#.#G#   G(122)
#...#E#   E(122)
#..G..#   G(200)
#######   

After 27 rounds:
#######   
#G....#   G(200)
#.G...#   G(131)
#.#.#G#   G(119)
#...#E#   E(119)
#...G.#   G(200)
#######   

After 28 rounds:
#######   
#G....#   G(200)
#.G...#   G(131)
#.#.#G#   G(116)
#...#E#   E(113)
#....G#   G(200)
#######   

More combat ensues; eventually, the bottom Elf dies:

After 47 rounds:
#######   
#G....#   G(200)
#.G...#   G(131)
#.#.#G#   G(59)
#...#.#   
#....G#   G(200)
#######   

Before the 48th round can finish, the top-left Goblin finds that there are no targets remaining, and so combat ends. So, the number of full rounds that were completed is 47, and the sum of the hit points of all remaining units is 200+131+59+200 = 590. From these, the outcome of the battle is 47 * 590 = 27730.

Here are a few example summarized combats:

#######       #######
#G..#E#       #...#E#   E(200)
#E#E.E#       #E#...#   E(197)
#G.##.#  -->  #.E##.#   E(185)
#...#E#       #E..#E#   E(200), E(200)
#...E.#       #.....#
#######       #######

Combat ends after 37 full rounds
Elves win with 982 total hit points left
Outcome: 37 * 982 = 36334

#######       #######   
#E..EG#       #.E.E.#   E(164), E(197)
#.#G.E#       #.#E..#   E(200)
#E.##E#  -->  #E.##.#   E(98)
#G..#.#       #.E.#.#   E(200)
#..E#.#       #...#.#   
#######       #######   

Combat ends after 46 full rounds
Elves win with 859 total hit points left
Outcome: 46 * 859 = 39514

#######       #######   
#E.G#.#       #G.G#.#   G(200), G(98)
#.#G..#       #.#G..#   G(200)
#G.#.G#  -->  #..#..#   
#G..#.#       #...#G#   G(95)
#...E.#       #...G.#   G(200)
#######       #######   

Combat ends after 35 full rounds
Goblins win with 793 total hit points left
Outcome: 35 * 793 = 27755

#######       #######   
#.E...#       #.....#   
#.#..G#       #.#G..#   G(200)
#.###.#  -->  #.###.#   
#E#G#G#       #.#.#.#   
#...#G#       #G.G#G#   G(98), G(38), G(200)
#######       #######   

Combat ends after 54 full rounds
Goblins win with 536 total hit points left
Outcome: 54 * 536 = 28944

#########       #########   
#G......#       #.G.....#   G(137)
#.E.#...#       #G.G#...#   G(200), G(200)
#..##..G#       #.G##...#   G(200)
#...##..#  -->  #...##..#   
#...#...#       #.G.#...#   G(200)
#.G...G.#       #.......#   
#.....G.#       #.......#   
#########       #########   

Combat ends after 20 full rounds
Goblins win with 937 total hit points left
Outcome: 20 * 937 = 18740

What is the outcome of the combat described in your puzzle input?

____
Too high:
Rounds:  76
HP Left:  2872
Score 218272
______

--- Part Two ---

According to your calculations, the Elves are going to lose badly. Surely, you won't mess up the timeline too much if you give them just a little advanced technology, right?

You need to make sure the Elves not only win, but also suffer no losses: even the death of a single Elf is unacceptable.

However, you can't go too far: larger changes will be more likely to permanently alter spacetime.

So, you need to find the outcome of the battle in which the Elves have the lowest integer attack power (at least 4) that allows them to win without a single death. The Goblins always have an attack power of 3.

In the first summarized example above, the lowest attack power the Elves need to win without losses is 15:

#######       #######
#.G...#       #..E..#   E(158)
#...EG#       #...E.#   E(14)
#.#.#G#  -->  #.#.#.#
#..G#E#       #...#.#
#.....#       #.....#
#######       #######

Combat ends after 29 full rounds
Elves win with 172 total hit points left
Outcome: 29 * 172 = 4988

In the second example above, the Elves need only 4 attack power:

#######       #######
#E..EG#       #.E.E.#   E(200), E(23)
#.#G.E#       #.#E..#   E(200)
#E.##E#  -->  #E.##E#   E(125), E(200)
#G..#.#       #.E.#.#   E(200)
#..E#.#       #...#.#
#######       #######

Combat ends after 33 full rounds
Elves win with 948 total hit points left
Outcome: 33 * 948 = 31284

In the third example above, the Elves need 15 attack power:

#######       #######
#E.G#.#       #.E.#.#   E(8)
#.#G..#       #.#E..#   E(86)
#G.#.G#  -->  #..#..#
#G..#.#       #...#.#
#...E.#       #.....#
#######       #######

Combat ends after 37 full rounds
Elves win with 94 total hit points left
Outcome: 37 * 94 = 3478

In the fourth example above, the Elves need 12 attack power:

#######       #######
#.E...#       #...E.#   E(14)
#.#..G#       #.#..E#   E(152)
#.###.#  -->  #.###.#
#E#G#G#       #.#.#.#
#...#G#       #...#.#
#######       #######

Combat ends after 39 full rounds
Elves win with 166 total hit points left
Outcome: 39 * 166 = 6474

In the last example above, the lone Elf needs 34 attack power:

#########       #########   
#G......#       #.......#   
#.E.#...#       #.E.#...#   E(38)
#..##..G#       #..##...#   
#...##..#  -->  #...##..#   
#...#...#       #...#...#   
#.G...G.#       #.......#   
#.....G.#       #.......#   
#########       #########   

Combat ends after 30 full rounds
Elves win with 38 total hit points left
Outcome: 30 * 38 = 1140

After increasing the Elves' attack power until it is just barely enough for them to win without any Elves dying, what is the outcome of the combat described in your puzzle input?

"""

map = []
elfs = []
goblins = []

class Pathway:

	def __init__(self, steps):
		self.steps = steps

# print the map, including all Elf and Goblin positions
def print_map():
	row_idx = 0
	for row in map:
		out = row[:]
		for unit in elfs:
			if unit.y == row_idx and unit.alive():
				out[unit.x] = unit.char
		for unit in goblins:
			if unit.y == row_idx and unit.alive():
				out[unit.x] = unit.char
		print ''.join(out)
		row_idx += 1

# list of all Elf and Goblin occupied spaces
#def occupied():
#	return [ e.loc() for e in elfs if e.alive() ] + [ g.loc() for g in goblins if g.alive() ]

def occ_set():
	o = { e.loc() for e in elfs if e.alive() }
	return o.union( { g.loc() for g in goblins if g.alive() } )
	
# return enemy unit to attack
def get_adjacent_target(loc, char):
	targets = []
	x = loc[0]
	y = loc[1]
	dirs = { (x+1, y) , (x-1 , y), (x, y+1), (x, y-1) }
	if char == "E":
		targets = [ g for g in goblins if g.alive() and g.loc() in dirs ]
	else:
		targets = [ e for e in elfs if e.alive() and e.loc() in dirs ]
	if len(targets) == 0:
		return None
	if len(targets) == 1:
		return targets[0]
	targets.sort(key = lambda x : x.hp)
	min_hp = targets[0].hp
	targets = filter(lambda x : x.hp == min_hp, targets)
	targets = sorted(targets, key = lambda a : a.sort_loc())
	return targets[0]
	
def bfs_paths(start, dest):
	if start == dest:
		return None
		
	valid_paths = []
	min_path_len = 1000000000
	
	paths_to_eval = deque()
	paths_to_eval.append( Pathway([start]) )
		
	blocked = occ_set()
	
	while len(paths_to_eval) != 0:
		current_path = paths_to_eval.popleft() # Remove a path from the queue
		current_path = current_path.steps
		pathset = set(current_path)
		#print pathset
		#print current_path
		current_node = current_path[-1] # Look at the last location visited
		if current_node == dest: # Found a valid pathway to the destination
			if len(current_path) <= min_path_len:
				min_path_len = len(current_path)
				valid_paths.append(current_path)
		else:
			blocked.add(current_node)
		if len(current_path) < min_path_len - 1: # continue exploring from this node (if on shorter path)
			x,y = current_node			
			if y > 0: # search up
				n = (x,y-1)
				if n not in blocked and n not in pathset and map[y-1][x] == '.':
					current_path.append(n)
					paths_to_eval.append( Pathway(list(current_path)) )
					current_path.pop()
					blocked.add(n)
			if x > 0: # search left
				n = (x-1,y)
				if n not in blocked and n not in pathset and map[y][x-1] == '.':
					current_path.append(n)
					paths_to_eval.append( Pathway(list(current_path))  )
					current_path.pop()
					blocked.add(n)
			if x < len(map[y])-1: # search right
				n = (x+1,y)
				if n not in blocked and n not in pathset and map[y][x+1] == '.':
					current_path.append(n)
					paths_to_eval.append( Pathway(list(current_path)) )
					current_path.pop()
					blocked.add(n)
			if y < len(map)-1: # search down
				n = (x,y+1)
				if n not in blocked and n not in pathset and map[y+1][x] == '.':
					current_path.append(n)
					paths_to_eval.append( Pathway(list(current_path)) )
					current_path.pop()
					blocked.add(n)
	if len(valid_paths) == 0:
		return None
	
	return filter( lambda x : len(x) == min_path_len, valid_paths )
	
def bfs_steps(start, dest):
	if start == dest:
		return 0
	to_visit = []		
	to_visit.append((start, 0))
		
	blocked = occ_set()
		
	while len(to_visit) != 0:
		current, depth = to_visit[0]
		x,y = current
		blocked.add(current)
		if current == dest:
			return depth
		if y > 0: # search up
			n = (x,y-1)
			if map[y-1][x] == '.' and n not in blocked:
				to_visit.append( (n, depth + 1))
				blocked.add(n)
		if x < len(map[y])-1: # search right
			n = (x+1,y)
			if map[y][x+1] == '.' and n not in blocked:
				to_visit.append( (n, depth + 1) )
				blocked.add(n)
		if y < len(map)-1: # search down
			n = (x,y+1)
			if map[y+1][x] == '.' and n not in blocked:
				to_visit.append( (n, depth + 1) )
				blocked.add(n)
		if x > 0: # search left
			n = (x-1,y)
			if map[y][x-1] == '.' and n not in blocked:
				to_visit.append( (n, depth + 1) )
				blocked.add(n)
		to_visit = to_visit[1:]
	
	# No path
	return None
		
	
def choose_target(loc, targets):
	accessible = []
	evaluated = []
	if len(targets) == 0:
		return None
	accessible = [ (bfs_steps(loc, target), target) for target in targets ]
	if len(accessible) == 0:
		return None
	evaluated = [ t for t in accessible if t[0] != None ]
	if len(evaluated) == 0:
		return None
	evaluated.sort(key = lambda x : x[0])
	min_dist = evaluated[0][0]
	accessible = [ t[1] for t in evaluated if t[0] == min_dist ]
	accessible = sorted(accessible, key = lambda a : (a[1],a[0]))
	return accessible[0]	

class Unit:

	def __init__(self, x, y, char, pow):
		self.hp = 200
		self.x = x
		self.y = y
		self.char = char
		self.pow = pow
		
	def loc(self):
		return (self.x,self.y)
		
	# for reading order
	def sort_loc(self):
		return (self.y,self.x)
		
	def alive(self):
		if self.hp > 0:
			return True
		return False
	
	def in_range(self):
		spots = set()
		if self.x > 0 and map[self.y][self.x-1] == '.':
			spots.add((self.x-1,self.y))
		if self.x < len(map[self.y])-1 and map[self.y][self.x+1] == '.':
			spots.add((self.x+1,self.y))
		if self.y > 0 and map[self.y-1][self.x] == '.':
			spots.add((self.x,self.y-1))
		if self.y < len(map)-1 and map[self.y+1][self.x] == '.':
			spots.add((self.x,self.y+1))
		return spots		

if __name__ == "__main__":

	# Part 2 Solution
	
	low = 1
	high = 40
	pow_up = (high + low) / 2
	while low <= high:
		
		# game reset
		print "Reset with power up set to: ", pow_up
		fail = False		
		map = []
		elfs = []
		goblins = []
		
		with open("day15_input", "r") as infile:
			row_idx = 0
			for line in infile.readlines():
				line = list(line.strip())
				for x in range(len(line)):
					if line[x] == "E":
						elfs.append(Unit(x,row_idx,line[x],3+pow_up))
						line[x] = '.'
					elif line[x] == "G":
						goblins.append(Unit(x,row_idx,line[x],3))
						line[x] = '.'
				map.append(line)
				row_idx += 1

		round = 0
		endgame = False
		while True:
			# Find living units
			units = [ e for e in elfs if e.alive() ] + [ g for g in goblins if g.alive() ]
			# Sorted by reading order for turn order

			for elf in elfs:
				if not elf.alive():		
					endgame = True
			
			units = sorted(units, key = lambda a : a.sort_loc())
			if endgame == True:
				break
			
			# take each turn
			for unit in units:
				#print "Unit ", unit.char, " at ", unit.loc(), " begins turn."
				range_locs = set()
				if unit.char == "E":
					alive = [ g for g in goblins if g.alive() ]
					for g in alive:
						range_locs = range_locs.union( g.in_range() )
				else: # is a Goblin
					alive = [ e for e in elfs if e.alive() ]
					for e in alive:
						range_locs = range_locs.union( e.in_range() )
				if len(range_locs) == 0:
					endgame = True
					break
				# Don't move if in range, or if there is nowhere to move to
				if unit.alive() and unit.loc() not in range_locs and len(range_locs.difference(occ_set())) != 0:				
					opponent = choose_target(unit.loc(), range_locs.difference(occ_set()))
					next_step = None
					moves = bfs_paths(unit.loc(), opponent)
					if moves != None:
						if len(moves) > 1:
							first_steps = []
							for move in moves:
								first_steps.append(move[1])
							first_steps = sorted(first_steps, key = lambda a : (a[1],a[0]))
							next_step = first_steps[0]
						else:
							next_step = moves[0][1]
						unit.x = next_step[0]
						unit.y = next_step[1]
				# Begin attack if in range
				if unit.alive() and unit.loc() in range_locs:
					target = get_adjacent_target(unit.loc(), unit.char)
					if target != None:
						target.hp -= unit.pow
			
			# Check for End Game
			if endgame == True:
				break
			round += 1
			
		### END GAME SCORE ###
		
		for elf in elfs:
			if not elf.alive():
				fail = True
		if not fail:
			hp_total = 0
			hp_total += sum( [ e.hp for e in elfs if e.alive() ] )
			hp_total += sum( [ g.hp for g in goblins if g.alive() ] )
			print "Power Up", pow_up
			print "Rounds: ", round
			print "HP Left: ", hp_total	
			print "Score", round * hp_total
			high = pow_up
		else:
			low = pow_up
		pow_up = (high + low) / 2
