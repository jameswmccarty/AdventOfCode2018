#!/usr/bin/python

"""
--- Day 18: Settlers of The North Pole ---

On the outskirts of the North Pole base construction project, many Elves are collecting lumber.

The lumber collection area is 50 acres by 50 acres; each acre can be either open ground (.), trees (|), or a lumberyard (#). You take a scan of the area (your puzzle input).

Strange magic is at work here: each minute, the landscape looks entirely different. In exactly one minute, an open acre can fill with trees, a wooded acre can be converted to a lumberyard, or a lumberyard can be cleared to open ground (the lumber having been sent to other projects).

The change to each acre is based entirely on the contents of that acre as well as the number of open, wooded, or lumberyard acres adjacent to it at the start of each minute. Here, "adjacent" means any of the eight acres surrounding that acre. (Acres on the edges of the lumber collection area might have fewer than eight adjacent acres; the missing acres aren't counted.)

In particular:

    An open acre will become filled with trees if three or more adjacent acres contained trees. Otherwise, nothing happens.
    An acre filled with trees will become a lumberyard if three or more adjacent acres were lumberyards. Otherwise, nothing happens.
    An acre containing a lumberyard will remain a lumberyard if it was adjacent to at least one other lumberyard and at least one acre containing trees. Otherwise, it becomes open.

These changes happen across all acres simultaneously, each of them using the state of all acres at the beginning of the minute and changing to their new form by the end of that same minute. Changes that happen during the minute don't affect each other.

For example, suppose the lumber collection area is instead only 10 by 10 acres with this initial configuration:

Initial state:
.#.#...|#.
.....#|##|
.|..|...#.
..|#.....#
#.#|||#|#|
...#.||...
.|....|...
||...#|.#|
|.||||..|.
...#.|..|.

After 1 minute:
.......##.
......|###
.|..|...#.
..|#||...#
..##||.|#|
...#||||..
||...|||..
|||||.||.|
||||||||||
....||..|.

After 2 minutes:
.......#..
......|#..
.|.|||....
..##|||..#
..###|||#|
...#|||||.
|||||||||.
||||||||||
||||||||||
.|||||||||

After 3 minutes:
.......#..
....|||#..
.|.||||...
..###|||.#
...##|||#|
.||##|||||
||||||||||
||||||||||
||||||||||
||||||||||

After 4 minutes:
.....|.#..
...||||#..
.|.#||||..
..###||||#
...###||#|
|||##|||||
||||||||||
||||||||||
||||||||||
||||||||||

After 5 minutes:
....|||#..
...||||#..
.|.##||||.
..####|||#
.|.###||#|
|||###||||
||||||||||
||||||||||
||||||||||
||||||||||

After 6 minutes:
...||||#..
...||||#..
.|.###|||.
..#.##|||#
|||#.##|#|
|||###||||
||||#|||||
||||||||||
||||||||||
||||||||||

After 7 minutes:
...||||#..
..||#|##..
.|.####||.
||#..##||#
||##.##|#|
|||####|||
|||###||||
||||||||||
||||||||||
||||||||||

After 8 minutes:
..||||##..
..|#####..
|||#####|.
||#...##|#
||##..###|
||##.###||
|||####|||
||||#|||||
||||||||||
||||||||||

After 9 minutes:
..||###...
.||#####..
||##...##.
||#....###
|##....##|
||##..###|
||######||
|||###||||
||||||||||
||||||||||

After 10 minutes:
.||##.....
||###.....
||##......
|##.....##
|##.....##
|##....##|
||##.####|
||#####|||
||||#|||||
||||||||||

After 10 minutes, there are 37 wooded acres and 31 lumberyards. Multiplying the number of wooded acres by the number of lumberyards gives the total resource value after ten minutes: 37 * 31 = 1147.

What will the total resource value of the lumber collection area be after 10 minutes?

--- Part Two ---

This important natural resource will need to last for at least thousands of years. Are the Elves collecting this lumber sustainably?

What will the total resource value of the lumber collection area be after 1000000000 minutes?

"""

map = []

def score():
	yards = 0
	trees = 0
	for row in map:
		for char in row:
			if char == "|":
				trees += 1
			elif char == "#":
				yards += 1
	return trees * yards

def score2():
	yards = 0
	trees = 0
	mrt = 0
	mry = 0
	for row in map:
		for char in row:
			if char == "|":
				trees += 1
			elif char == "#":
				yards += 1
		mrt = max(mrt, row.count("|"))
		mry = max(mry, row.count("#"))
	return (trees, yards, mrt, mry)	

def cellcount(loc):
	yards = 0
	trees = 0
	open  = 0
	adj_contents = []
	x, y = loc
	if x > 0:
		if y > 0:
			adj_contents.append(map[y-1][x-1])
		adj_contents.append(map[y][x-1])
		if y < len(map)-1:
			adj_contents.append(map[y+1][x-1])
	if y > 0:
		adj_contents.append(map[y-1][x])
	if y < len(map)-1:
		adj_contents.append(map[y+1][x])
	if x < len(map[0])-1:
		adj_contents.append(map[y][x+1])
		if y > 0:
			adj_contents.append(map[y-1][x+1])
		if y < len(map)-1:
			adj_contents.append(map[y+1][x+1])
	return (adj_contents.count("#"), adj_contents.count("|"), adj_contents.count("."))
		

def grow(map):
	next = []
	for i, map_row in enumerate(map):
		n_gen_row = [None] * len(map[0])
		for j, cell in enumerate(map_row):
			y,t,o = cellcount((j,i))
			if map[i][j] == '.':
				if t >= 3:
					n_gen_row[j] = "|"
				else:
					n_gen_row[j] = '.'
			elif map[i][j] == '|':
				if y >= 3:
					n_gen_row[j] = '#'
				else:
					n_gen_row[j] = '|'
			elif map[i][j] == '#':
				if t >= 1 and y >= 1:
					n_gen_row[j] = "#"
				else:
					n_gen_row[j] = '.'
		next.append(n_gen_row)
	return next

if __name__ == "__main__":

	# Part 1 Solution
	map = []	
	with open("day18_input", "r") as infile:
		for line in infile.readlines():
			map.append(list(line.strip()))	
	for i in range(10):
		map = grow(map)
	print score()
	
	# Part 2 Solution
	map = []	
	with open("day18_input", "r") as infile:
		for line in infile.readlines():
			map.append(list(line.strip()))
			
	target_gen = 1000000000
	
	# give growth a head start to reach stable state
	for i in range(600):
		map = grow(map)
	
	seen_scores = []
	delta = 0
	while delta == 0:
		map = grow(map)
		res = score2()
		if res in seen_scores: # locate  loop
			delta += 1
			map = grow(map)
			while res != score2(): # find loop size
				map = grow(map)
				delta += 1
			break
		seen_scores.append(res)
	
	target_gen = (target_gen - 600 + 1) % delta
	for i in range(target_gen+1):
		map = grow(map)
	print score()
