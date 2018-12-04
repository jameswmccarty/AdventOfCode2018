#!/usr/bin/python

"""
--- Day 3: No Matter How You Slice It ---

The Elves managed to locate the chimney-squeeze prototype fabric for Santa's suit (thanks to someone who helpfully wrote its box IDs on the wall of the warehouse in the middle of the night). Unfortunately, anomalies are still affecting them - nobody can even agree on how to cut the fabric.

The whole piece of fabric they're working on is a very large square - at least 1000 inches on each side.

Each Elf has made a claim about which area of fabric would be ideal for Santa's suit. All claims have an ID and consist of a single rectangle with edges parallel to the edges of the fabric. Each claim's rectangle is defined as follows:

    The number of inches between the left edge of the fabric and the left edge of the rectangle.
    The number of inches between the top edge of the fabric and the top edge of the rectangle.
    The width of the rectangle in inches.
    The height of the rectangle in inches.

A claim like #123 @ 3,2: 5x4 means that claim ID 123 specifies a rectangle 3 inches from the left edge, 2 inches from the top edge, 5 inches wide, and 4 inches tall. Visually, it claims the square inches of fabric represented by # (and ignores the square inches of fabric represented by .) in the diagram below:

...........
...........
...#####...
...#####...
...#####...
...#####...
...........
...........
...........

The problem is that many of the claims overlap, causing two or more claims to cover part of the same areas. For example, consider the following claims:

#1 @ 1,3: 4x4
#2 @ 3,1: 4x4
#3 @ 5,5: 2x2

Visually, these claim the following areas:

........
...2222.
...2222.
.11XX22.
.11XX22.
.111133.
.111133.
........

The four square inches marked with X are claimed by both 1 and 2. (Claim 3, while adjacent to the others, does not overlap either of them.)

If the Elves all proceed with their own plans, none of them will have enough fabric. How many square inches of fabric are within two or more claims?

--- Part Two ---

Amidst the chaos, you notice that exactly one claim doesn't overlap by even a single square inch of fabric with any other claim. If you can somehow draw attention to it, maybe the Elves will be able to make Santa's suit after all!

For example, in the claims above, only claim 3 is intact after all claims are made.

What is the ID of the only claim that doesn't overlap?

"""

def claim_parse(claim):
	id, info = claim.split(" @ ")
	coords, dims = info.split(": ")
	x, y = coords.split(",")
	w, h = dims.split("x")
	return (str(id),int(x),int(y),int(w),int(h))


if __name__ == "__main__":
	#Part 1 Solution
	#fabric is 1000x1000 inches.  Each sq inch holds a set of claims.
	fab_size = 1000
	fabric = []
	for i in xrange(fab_size):
		fabric.append([ set() for __ in xrange(fab_size)])
	#fabric = [ [ '' ] * fab_size for i in range(fab_size) ]
	claims = []
	overlaps = 0
	with open("day3_input", "r") as infile:
		for line in infile.readlines():
			claims.append(line.strip())
	for claim in claims:
		id_num,x,y,w,h = claim_parse(claim)
		for i in range(x,x+w):
			for j in range(y,y+h):
				#fabric[j][i] = fabric[j][i] + id_num + " "
				fabric[j][i].add(id_num)
	for i in range(fab_size):
		for j in range(fab_size):
			#if len(fabric[j][i].strip().split(" ")) > 1:
			if len(fabric[j][i]) > 1:
				overlaps += 1
	print "Part 1 solution " + str(overlaps)

	#Part 2 Solution
	for claim in claims:
		valid = True
		id_num,x,y,w,h = claim_parse(claim)
		for i in range(x,x+w):
			for j in range(y,y+h):
				if len(fabric[j][i]) != 1:
					valid = False
		if valid == True:
			print "Part 2 solution " + id_num

