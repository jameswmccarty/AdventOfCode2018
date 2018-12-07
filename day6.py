#/usr/bin/python

"""
--- Day 6: Chronal Coordinates ---

The device on your wrist beeps several times, and once again you feel like you're falling.

"Situation critical," the device announces. "Destination indeterminate. Chronal interference detected. Please specify new target coordinates."

The device then produces a list of coordinates (your puzzle input). Are they places it thinks are safe or dangerous? It recommends you check manual page 729. The Elves did not give you a manual.

If they're dangerous, maybe you can minimize the danger by finding the coordinate that gives the largest distance from the other points.

Using only the Manhattan distance, determine the area around each coordinate by counting the number of integer X,Y locations that are closest to that coordinate (and aren't tied in distance to any other coordinate).

Your goal is to find the size of the largest area that isn't infinite. For example, consider the following list of coordinates:

1, 1
1, 6
8, 3
3, 4
5, 5
8, 9

If we name these coordinates A through F, we can draw them on a grid, putting 0,0 at the top left:

..........
.A........
..........
........C.
...D......
.....E....
.B........
..........
..........
........F.

This view is partial - the actual grid extends infinitely in all directions. Using the Manhattan distance, each location's closest coordinate can be determined, shown here in lowercase:

aaaaa.cccc
aAaaa.cccc
aaaddecccc
aadddeccCc
..dDdeeccc
bb.deEeecc
bBb.eeee..
bbb.eeefff
bbb.eeffff
bbb.ffffFf

Locations shown as . are equally far from two or more coordinates, and so they don't count as being closest to any.

In this example, the areas of coordinates A, B, C, and F are infinite - while not shown here, their areas extend forever outside the visible grid. However, the areas of coordinates D and E are finite: D is closest to 9 locations, and E is closest to 17 (both including the coordinate's location itself). Therefore, in this example, the size of the largest area is 17.

What is the size of the largest area that isn't infinite?

--- Part Two ---

On the other hand, if the coordinates are safe, maybe the best you can do is try to find a region near as many coordinates as possible.

For example, suppose you want the sum of the Manhattan distance to all of the coordinates to be less than 32. For each location, add up the distances to all of the given coordinates; if the total of those distances is less than 32, that location is within the desired region. Using the same coordinates as above, the resulting region looks like this:

..........
.A........
..........
...###..C.
..#D###...
..###E#...
.B.###....
..........
..........
........F.

In particular, consider the highlighted location 4,3 located at the top middle of the region. Its calculation is as follows, where abs() is the absolute value function:

    Distance to coordinate A: abs(4-1) + abs(3-1) =  5
    Distance to coordinate B: abs(4-1) + abs(3-6) =  6
    Distance to coordinate C: abs(4-8) + abs(3-3) =  4
    Distance to coordinate D: abs(4-3) + abs(3-4) =  2
    Distance to coordinate E: abs(4-5) + abs(3-5) =  3
    Distance to coordinate F: abs(4-8) + abs(3-9) = 10
    Total distance: 5 + 6 + 4 + 2 + 3 + 10 = 30

Because the total distance to all coordinates (30) is less than 32, the location is within the region.

This region, which also includes coordinates D and E, has a total size of 16.

Your actual region will need to be much larger than this example, though, instead including all locations with a total distance of less than 10000.

What is the size of the region containing all locations which have a total distance to all given coordinates of less than 10000?

"""

class Point:
	
	def __init__(self, x, y):
		self.x = int(x)
		self.y = int(y)
		self.is_inf = False # is an outer boundry, and won't count
		self.score = 0 # for counting area
		
	def mh_dist(self, pt):
		return abs(self.x - pt.x) + abs(self.y - pt.y)


if __name__ == "__main__":

	#Part 1 Solution
	
	points = []
	with open("day6_input", "r") as infile:
		for line in infile.readlines():
			x, y = line.strip().split(", ")
			points.append(Point(x, y))
			
	# locate boundary points
	xcords = []
	ycords = []
	for point in points:
		xcords.append(point.x) # all x coordinates
		ycords.append(point.y) # all y coordinates
	minx = min(xcords)
	maxx = max(xcords)
	miny = min(ycords)
	maxy = max(ycords)
	for point in points:
		# exclude all that lie on boundary
		if point.x == minx or point.x == maxx or point.y == miny or point.y == maxy:
			point.is_inf = True

	# build a 2D grid to contain all available points
	grid = [[None] * maxx for i in range(maxy)]
		
	for i in range(minx, maxx):
		for j in range(miny, maxy):
			ranges = []
			for point in points:
				# find each grid point's distance from set of all points
				ranges.append((point.mh_dist(Point(i, j)), point))
			ranges.sort(key = lambda x : x[0]) # locate closest point
			if ranges[0][0] == ranges[1][0]: # equal distant to two points
				grid[j][i] = None
			else:
				grid[j][i] = ranges[0][1] # assign closest point
				

	# find point that owns the most grid area
	max_score = 0
	best_point = None
	for i in range(minx, maxx):
		for j in range(miny, maxy):
			if grid[j][i] is not None:
				if grid[j][i].is_inf == False:
					grid[j][i].score += 1
					if grid[j][i].score > max_score:
						max_score = grid[j][i].score
						best_point = grid[j][i]
	
	print best_point.score
	
	# Part 2 Solution
	
	# build a 2D grid to contain all available points
	grid = [[None] * maxx for i in range(maxy)]
		
	for i in range(minx, maxx):
		for j in range(miny, maxy):
			total_dist = 0
			for point in points:
				# sum each grid point's distance from set of all points
				total_dist += point.mh_dist(Point(i, j))
			if total_dist < 10000: # count as in range
				grid[j][i] = 1
			else:
				grid[j][i] = 0
	
	safe_area = 0
	for i in range(minx, maxx):
		for j in range(miny, maxy):
			safe_area += grid[j][i]
			
	print safe_area
	



		
