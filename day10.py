#!/usr/bin/python

from PIL import Image

"""
--- Day 10: The Stars Align ---

It's no use; your navigation system simply isn't capable of providing walking directions in the arctic circle, and certainly not in 1018.

The Elves suggest an alternative. In times like these, North Pole rescue operations will arrange points of light in the sky to guide missing Elves back to base. Unfortunately, the message is easy to miss: the points move slowly enough that it takes hours to align them, but have so much momentum that they only stay aligned for a second. If you blink at the wrong time, it might be hours before another message appears.

You can see these points of light floating in the distance, and record their position in the sky and their velocity, the relative change in position per second (your puzzle input). The coordinates are all given from your perspective; given enough time, those positions and velocities will move the points into a cohesive message!

Rather than wait, you decide to fast-forward the process and calculate what the points will eventually spell.

For example, suppose you note the following points:

position=< 9,  1> velocity=< 0,  2>
position=< 7,  0> velocity=<-1,  0>
position=< 3, -2> velocity=<-1,  1>
position=< 6, 10> velocity=<-2, -1>
position=< 2, -4> velocity=< 2,  2>
position=<-6, 10> velocity=< 2, -2>
position=< 1,  8> velocity=< 1, -1>
position=< 1,  7> velocity=< 1,  0>
position=<-3, 11> velocity=< 1, -2>
position=< 7,  6> velocity=<-1, -1>
position=<-2,  3> velocity=< 1,  0>
position=<-4,  3> velocity=< 2,  0>
position=<10, -3> velocity=<-1,  1>
position=< 5, 11> velocity=< 1, -2>
position=< 4,  7> velocity=< 0, -1>
position=< 8, -2> velocity=< 0,  1>
position=<15,  0> velocity=<-2,  0>
position=< 1,  6> velocity=< 1,  0>
position=< 8,  9> velocity=< 0, -1>
position=< 3,  3> velocity=<-1,  1>
position=< 0,  5> velocity=< 0, -1>
position=<-2,  2> velocity=< 2,  0>
position=< 5, -2> velocity=< 1,  2>
position=< 1,  4> velocity=< 2,  1>
position=<-2,  7> velocity=< 2, -2>
position=< 3,  6> velocity=<-1, -1>
position=< 5,  0> velocity=< 1,  0>
position=<-6,  0> velocity=< 2,  0>
position=< 5,  9> velocity=< 1, -2>
position=<14,  7> velocity=<-2,  0>
position=<-3,  6> velocity=< 2, -1>

Each line represents one point. Positions are given as <X, Y> pairs: X represents how far left (negative) or right (positive) the point appears, while Y represents how far up (negative) or down (positive) the point appears.

At 0 seconds, each point has the position given. Each second, each point's velocity is added to its position. So, a point with velocity <1, -2> is moving to the right, but is moving upward twice as quickly. If this point's initial position were <3, 9>, after 3 seconds, its position would become <6, 3>.

Over time, the points listed above would move like this:

Initially:
........#.............
................#.....
.........#.#..#.......
......................
#..........#.#.......#
...............#......
....#.................
..#.#....#............
.......#..............
......#...............
...#...#.#...#........
....#..#..#.........#.
.......#..............
...........#..#.......
#...........#.........
...#.......#..........

After 1 second:
......................
......................
..........#....#......
........#.....#.......
..#.........#......#..
......................
......#...............
....##.........#......
......#.#.............
.....##.##..#.........
........#.#...........
........#...#.....#...
..#...........#.......
....#.....#.#.........
......................
......................

After 2 seconds:
......................
......................
......................
..............#.......
....#..#...####..#....
......................
........#....#........
......#.#.............
.......#...#..........
.......#..#..#.#......
....#....#.#..........
.....#...#...##.#.....
........#.............
......................
......................
......................

After 3 seconds:
......................
......................
......................
......................
......#...#..###......
......#...#...#.......
......#...#...#.......
......#####...#.......
......#...#...#.......
......#...#...#.......
......#...#...#.......
......#...#..###......
......................
......................
......................
......................

After 4 seconds:
......................
......................
......................
............#.........
........##...#.#......
......#.....#..#......
.....#..##.##.#.......
.......##.#....#......
...........#....#.....
..............#.......
....#......#...#......
.....#.....##.........
...............#......
...............#......
......................
......................

After 3 seconds, the message appeared briefly: HI. Of course, your message will be much longer and will take many more seconds to appear.

What message will eventually appear in the sky?

--- Part Two ---

Good thing you didn't have to wait, because that would have taken a long time - much longer than the 3 seconds in the example above.

Impressed by your sub-hour communication capabilities, the Elves are curious: exactly how many seconds would they have needed to wait for that message to appear?

"""

class Point:
	
	def __init__(self, x, y, dx, dy):
		self.x = x
		self.y = y
		self.dx = dx
		self.dy = dy
		self.ox = x
		self.oy = y
	
	def move(self):
		self.x += self.dx
		self.y += self.dy
		
	def set_time(self, t):
		self.x = self.ox + self.dx*t
		self.y = self.oy + self.dy*t
	

def parse_pt(line):
	# Example: position=< 9,  1> velocity=< 0,  2>
	pos, vol = line.split("> velocity=<")
	pos = pos.replace("position=<", '').strip()
	x, y = pos.split(",")
	vol = vol.replace(">", '').strip()
	dx, dy = vol.split(",")
	return Point(int(x),int(y),int(dx),int(dy))
	
def draw_sky(w, h, points):
	#line = '-' * w
	#print line
	sky = [[" "] * w for i in range(h)]
	for p in points:
		if p.y >=0 and p.y < h and p.x >=0 and p.x < w:
			sky[p.y][p.x] = "X"
	for row in sky:
		line = ''.join(val for val in row)
		print line.rstrip()

def img_sky(w,h,points):
	img = Image.new( 'RGB', (w,h), "black") # Create a new black image
	pixels = img.load() # Create the pixel map
	for p in points:
		if p.x >=0 and p.x < w and p.y >=0 and p.y < h:
			pixels[p.x,p.y] = (255, 255, 255) # Set the colour accordingly
	return img
	
# translate points to origin and return
# overall width and height
def clean_dim(points):
	mx = 10000
	my = 10000
	ax = 0
	ay = 0
	for p in points:
		mx = min(p.x,mx)
		my = min(p.y,my)
	for p in points:
		p.x -= mx
		p.y -= my
		ay = max(p.y,ay)
		ax = max(p.x,ax)
	return ax, ay

# alignment occurs when all characters are less than 10 pixels tall
def guess_jump(t, points):
	mn = 1000
	mx = 0
	for p in points:
		p.set_time(t)
		mn = min(mn,p.y)
		mx = max(mx,p.y)
	if mx-mn < 10:
		return True
	return False
	

if __name__ == "__main__":

	# Part 1 and 2 Solution
	
	points = []
	
	with open("day10_input", "r") as infile:
		for line in infile.readlines():
			points.append(parse_pt(line))
			
	jump_t = 0
	for i in range(25000):
		if guess_jump(i,points):
			jump_t = i
			break
	
	w,h = clean_dim(points)
	
	draw_sky(w+2,h+2,points)
	print jump_t
	img_sky(w+2,h+2,points).show()