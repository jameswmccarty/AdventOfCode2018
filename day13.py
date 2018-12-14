#!/usr/bin/python

"""
--- Day 13: Mine Cart Madness ---

A crop of this size requires significant logistics to transport produce, soil, fertilizer, and so on. The Elves are very busy pushing things around in carts on some kind of rudimentary system of tracks they've come up with.

Seeing as how cart-and-track systems don't appear in recorded history for another 1000 years, the Elves seem to be making this up as they go along. They haven't even figured out how to avoid collisions yet.

You map out the tracks (your puzzle input) and see where you can help.

Tracks consist of straight paths (| and -), curves (/ and \), and intersections (+). Curves connect exactly two perpendicular pieces of track; for example, this is a closed loop:

/----\
|    |
|    |
\----/

Intersections occur when two perpendicular paths cross. At an intersection, a cart is capable of turning left, turning right, or continuing straight. Here are two loops connected by two intersections:

/-----\
|     |
|  /--+--\
|  |  |  |
\--+--/  |
   |     |
   \-----/

Several carts are also on the tracks. Carts always face either up (^), down (v), left (<), or right (>). (On your initial map, the track under each cart is a straight path matching the direction the cart is facing.)

Each time a cart has the option to turn (by arriving at any intersection), it turns left the first time, goes straight the second time, turns right the third time, and then repeats those directions starting again with left the fourth time, straight the fifth time, and so on. This process is independent of the particular intersection at which the cart has arrived - that is, the cart has no per-intersection memory.

Carts all move at the same speed; they take turns moving a single step at a time. They do this based on their current location: carts on the top row move first (acting from left to right), then carts on the second row move (again from left to right), then carts on the third row, and so on. Once each cart has moved one step, the process repeats; each of these loops is called a tick.

For example, suppose there are two carts on a straight track:

|  |  |  |  |
v  |  |  |  |
|  v  v  |  |
|  |  |  v  X
|  |  ^  ^  |
^  ^  |  |  |
|  |  |  |  |

First, the top cart moves. It is facing down (v), so it moves down one square. Second, the bottom cart moves. It is facing up (^), so it moves up one square. Because all carts have moved, the first tick ends. Then, the process repeats, starting with the first cart. The first cart moves down, then the second cart moves up - right into the first cart, colliding with it! (The location of the crash is marked with an X.) This ends the second and last tick.

Here is a longer example:

/->-\        
|   |  /----\
| /-+--+-\  |
| | |  | v  |
\-+-/  \-+--/
  \------/   

/-->\        
|   |  /----\
| /-+--+-\  |
| | |  | |  |
\-+-/  \->--/
  \------/   

/---v        
|   |  /----\
| /-+--+-\  |
| | |  | |  |
\-+-/  \-+>-/
  \------/   

/---\        
|   v  /----\
| /-+--+-\  |
| | |  | |  |
\-+-/  \-+->/
  \------/   

/---\        
|   |  /----\
| /->--+-\  |
| | |  | |  |
\-+-/  \-+--^
  \------/   

/---\        
|   |  /----\
| /-+>-+-\  |
| | |  | |  ^
\-+-/  \-+--/
  \------/   

/---\        
|   |  /----\
| /-+->+-\  ^
| | |  | |  |
\-+-/  \-+--/
  \------/   

/---\        
|   |  /----<
| /-+-->-\  |
| | |  | |  |
\-+-/  \-+--/
  \------/   

/---\        
|   |  /---<\
| /-+--+>\  |
| | |  | |  |
\-+-/  \-+--/
  \------/   

/---\        
|   |  /--<-\
| /-+--+-v  |
| | |  | |  |
\-+-/  \-+--/
  \------/   

/---\        
|   |  /-<--\
| /-+--+-\  |
| | |  | v  |
\-+-/  \-+--/
  \------/   

/---\        
|   |  /<---\
| /-+--+-\  |
| | |  | |  |
\-+-/  \-<--/
  \------/   

/---\        
|   |  v----\
| /-+--+-\  |
| | |  | |  |
\-+-/  \<+--/
  \------/   

/---\        
|   |  /----\
| /-+--v-\  |
| | |  | |  |
\-+-/  ^-+--/
  \------/   

/---\        
|   |  /----\
| /-+--+-\  |
| | |  X |  |
\-+-/  \-+--/
  \------/   

After following their respective paths for a while, the carts eventually crash. To help prevent crashes, you'd like to know the location of the first crash. Locations are given in X,Y coordinates, where the furthest left column is X=0 and the furthest top row is Y=0:

           111
 0123456789012
0/---\        
1|   |  /----\
2| /-+--+-\  |
3| | |  X |  |
4\-+-/  \-+--/
5  \------/   

In this example, the location of the first crash is 7,3.

*82, 104)

--- Part Two ---

There isn't much you can do to prevent crashes in this ridiculous system. However, by predicting the crashes, the Elves know where to be in advance and instantly remove the two crashing carts the moment any crash occurs.

They can proceed like this for a while, but eventually, they're going to run out of carts. It could be useful to figure out where the last cart that hasn't crashed will end up.

For example:

/>-<\  
|   |  
| /<+-\
| | | v
\>+</ |
  |   ^
  \<->/

/---\  
|   |  
| v-+-\
| | | |
\-+-/ |
  |   |
  ^---^

/---\  
|   |  
| /-+-\
| v | |
\-+-/ |
  ^   ^
  \---/

/---\  
|   |  
| /-+-\
| | | |
\-+-/ ^
  |   |
  \---/

After four very expensive crashes, a tick ends with only one cart remaining; its final location is 6,4.

What is the location of the last cart at the end of the first tick where it is the only cart left?

(121,22)

"""

carts = []
map = []

def display_map():
	row_idx = 0
	for row in map:
		line = ''.join(row)
		for cart in carts:
			if cart.y == row_idx:
				line = list(line)
				line[cart.x] = cart.as_char()
				line = ''.join(line)
		row_idx += 1
		print line,
	print

class Cart:

	def __init__(self, x, y, pic):
		
		# 0 - left
		# 1 - straight
		# 2 - right
		self.turn = 0
		
		# 0 - ^ - up
		# 1 - > - right
		# 2 - v - down
		# 3 - < - left
		if pic == "^":
			self.dir  = 0
		elif pic == ">":
			self.dir  = 1
		elif pic == "v":
			self.dir  = 2
		elif pic == "<":
			self.dir  = 3
		
		self.x = x
		self.y = y
		self.rmv = False

	def as_char(self):
		if self.dir == 0:
			return "^"
		elif self.dir == 1:
			return ">"
		elif self.dir == 2:
			return "v"
		elif self.dir == 3:
			return "<"
	
	def move(self):
		if self.dir == 0:
			self.y -= 1
		elif self.dir == 1:
			self.x += 1
		elif self.dir == 2:
			self.y += 1
		elif self.dir == 3:
			self.x -= 1
		
		for cart in carts:
			if cart != self:
				if cart.x == self.x and cart.y == self.y:
					return False
			
		track = map[self.y][self.x]
		
		if track == '/':
			if self.dir == 3:
				self.dir = 2
			elif self.dir == 0:
				self.dir = 1
			elif self.dir == 2:
				self.dir = 3
			elif self.dir == 1:
				self.dir = 0
		elif track == '\\':
			if self.dir == 3:
				self.dir = 0
			elif self.dir == 0:
				self.dir = 3
			elif self.dir == 2:
				self.dir = 1
			elif self.dir == 1:
				self.dir = 2
		elif track == '+':
			if self.turn == 0: # left
				self.dir -= 1
				if self.dir < 0:
					self.dir = 3
			elif self.turn == 2: # right
				self.dir += 1
				self.dir %= 4
			self.turn += 1
			self.turn %= 3
		return True

	def rm_move(self):
		if self.dir == 0:
			self.y -= 1
		elif self.dir == 1:
			self.x += 1
		elif self.dir == 2:
			self.y += 1
		elif self.dir == 3:
			self.x -= 1
		
		for cart in carts:
			if cart != self:
				if cart.x == self.x and cart.y == self.y:
					self.rmv = True	
					cart.rmv = True
			
		track = map[self.y][self.x]
		
		if track == '/':
			if self.dir == 3:
				self.dir = 2
			elif self.dir == 0:
				self.dir = 1
			elif self.dir == 2:
				self.dir = 3
			elif self.dir == 1:
				self.dir = 0
		elif track == '\\':
			if self.dir == 3:
				self.dir = 0
			elif self.dir == 0:
				self.dir = 3
			elif self.dir == 2:
				self.dir = 1
			elif self.dir == 1:
				self.dir = 2
		elif track == '+':
			if self.turn == 0: # left
				self.dir -= 1
				if self.dir < 0:
					self.dir = 3
			elif self.turn == 2: # right
				self.dir += 1
				self.dir %= 4
			self.turn += 1
			self.turn %= 3
		
if __name__ == "__main__":

	# Part 1 Solution
	with open("day13_input", "r") as infile:
		row_idx = 0
		for line in infile.readlines():
			map.append(list(line))
			for i in range(len(map[row_idx])):
				if map[row_idx][i] == "^" or map[row_idx][i] == "v":
					carts.append(Cart(i,row_idx,map[row_idx][i]))
					map[row_idx][i] = "|"
				if map[row_idx][i] == "<" or map[row_idx][i] == ">":
					carts.append(Cart(i,row_idx,map[row_idx][i]))
					map[row_idx][i] = "-"
			row_idx += 1
	
	crashed = False
	while not crashed:
		#display_map()
		carts = sorted(carts, key=lambda a: (a.y,a.x))
		for cart in carts:
			if not cart.move():
				print str(cart.x) + ", " + str(cart.y)
				crashed = True
				break
		if not crashed:
			for i in range(len(carts)):
				for j in range(i+1, len(carts)):
					if carts[i].x == carts[j].x and carts[i].y == carts[j].y:
						print str(carts[i].x) + ", " + str(carts[i].y)
						crashed = True
						break


	# Part 2 Solution
	map = []
	carts = []
	with open("day13_input", "r") as infile:
		row_idx = 0
		for line in infile.readlines():
			map.append(list(line))
			for i in range(len(map[row_idx])):
				if map[row_idx][i] == "^" or map[row_idx][i] == "v":
					carts.append(Cart(i,row_idx,map[row_idx][i]))
					map[row_idx][i] = "|"
				if map[row_idx][i] == "<" or map[row_idx][i] == ">":
					carts.append(Cart(i,row_idx,map[row_idx][i]))
					map[row_idx][i] = "-"
			row_idx += 1
	
	
	while True:
		#display_map()
		if len(carts) == 1:
			print str(carts[0].x) + "," + str(carts[0].y)
			break
		carts = sorted(carts, key=lambda a: (a.y,a.x))
		for cart in carts:
			if not cart.rmv:
				cart.rm_move()
		for cart in carts:
			if cart.rmv:
				carts.remove(cart)
		if len(carts) == 1:
			print str(carts[0].x) + "," + str(carts[0].y)
			break
		for i in range(len(carts)):
			for j in range(i+1,len(carts)):
					if carts[i].x == carts[j].x and carts[i].y == carts[j].y:
						carts[i].rmv = True
						carts[j].rmv = True
		for cart in carts:
			if cart.rmv:
				carts.remove(cart)			
			
			
		
