#!/usr/bin/python

"""
--- Day 21: Chronal Conversion ---

You should have been watching where you were going, because as you wander the new North Pole base, you trip and fall into a very deep hole!

Just kidding. You're falling through time again.

If you keep up your current pace, you should have resolved all of the temporal anomalies by the next time the device activates. Since you have very little interest in browsing history in 500-year increments for the rest of your life, you need to find a way to get back to your present time.

After a little research, you discover two important facts about the behavior of the device:

First, you discover that the device is hard-wired to always send you back in time in 500-year increments. Changing this is probably not feasible.

Second, you discover the activation system (your puzzle input) for the time travel module. Currently, it appears to run forever without halting.

If you can cause the activation system to halt at a specific moment, maybe you can make the device send you so far back in time that you cause an integer underflow in time itself and wrap around back to your current time!

The device executes the program as specified in manual section one and manual section two.

Your goal is to figure out how the program works and cause it to halt. You can only control register 0; every other register begins at 0 as usual.

Because time travel is a dangerous activity, the activation system begins with a few instructions which verify that bitwise AND (via bani) does a numeric operation and not an operation as if the inputs were interpreted as strings. If the test fails, it enters an infinite loop re-running the test instead of allowing the program to execute normally. If the test passes, the program continues, and assumes that all other bitwise operations (banr, bori, and borr) also interpret their inputs as numbers. (Clearly, the Elves who wrote this system were worried that someone might introduce a bug while trying to emulate this system with a scripting language.)

What is the lowest non-negative integer value for register 0 that causes the program to halt after executing the fewest instructions? (Executing the same instruction multiple times counts as multiple instructions executed.)

--- Part Two ---

In order to determine the timing window for your underflow exploit, you also need an upper bound:

What is the lowest non-negative integer value for register 0 that causes the program to halt after executing the most instructions? (The program must actually halt; running forever does not count as halting.)


"""

# 5 registers
regs = { "0" : 0,
		 "1" : 0,
		 "2" : 0,
		 "3" : 0,
		 "4" : 0,
		 "5" : 0}

def reset():
	global regs
	regs = { "0" : 0, "1" : 0, "2" : 0, "3" : 0, "4" : 0, "5" : 0}
	
def regs_dump():
	return [ regs["0"], regs["1"], regs["2"], regs["3"], regs["4"], regs["5"] ]

# addr (add register) 
# stores into register C the result of adding register A and register B.
def addr(a,b,c):
	regs[c] = int(regs[a]) + int(regs[b])

# addi (add immediate)
# stores into register C the result of adding register A and value B.	
def addi(a, b, c):
	regs[c] = int(regs[a]) + int(b)

# mulr (multiply register) stores into register C 
# the result of multiplying register A and register B.
def mulr(a, b, c):
	regs[c] = int(regs[a]) * int(regs[b])

# muli (multiply immediate) 
# stores into register C the result of multiplying register A and value B.
def muli(a, b, c):
	regs[c] = int(regs[a]) * int(b)
	
# banr (bitwise AND register) stores into register C the result of the 
# bitwise AND of register A and register B.
def banr(a, b, c):
	regs[c] = int(regs[a]) & int(regs[b])

# bani (bitwise AND immediate) stores into register C the result of the 
# bitwise AND of register A and value B.
def bani(a, b, c):
	regs[c] = int(regs[a]) & int(b)

# borr (bitwise OR register) stores into register C the result of the 
# bitwise OR of register A and register B.
def borr(a, b, c):
	regs[c] = int(regs[a]) | int(regs[b])

# bori (bitwise OR immediate) stores into register C the result of the 
# bitwise OR of register A and value B.
def bori(a, b, c):
	regs[c] = int(regs[a]) | int(b)

# setr (set register) copies the contents of register A into register C. 
# (Input B is ignored.)
def setr(a, b, c):
	regs[c] = int(regs[a])

# seti (set immediate) stores value A into register C. 
# (Input B is ignored.)
def seti(a, b, c):
	regs[c] = int(a)

# gtir (greater-than immediate/register) sets register C to 1 if value A is 
# greater than register B. Otherwise, register C is set to 0.
def gtir(a, b, c):
	if(int(a) > int(regs[b])):
		regs[c] = 1
	else:
		regs[c] = 0

# gtri (greater-than register/immediate) sets register C to 1 if register 
# A is greater than value B. Otherwise, register C is set to 0.
def gtri(a, b, c):
	if(int(regs[a]) > int(b)):
		regs[c] = 1
	else:
		regs[c] = 0
		
# gtrr (greater-than register/register) sets register C to 1 if register A 
# is greater than register B. Otherwise, register C is set to 0.
def gtrr(a, b, c):
	if(int(regs[a]) > int(regs[b])):
		regs[c] = 1
	else:
		regs[c] = 0

# eqir (equal immediate/register) sets register C to 1 if value A is equal to register B. 
# Otherwise, register C is set to 0.
def eqir(a, b, c):
	if(int(a) == int(regs[b])):
		regs[c] = 1
	else:
		regs[c] = 0

# eqri (equal register/immediate) sets register C to 1 if register A is equal to value B. 
# Otherwise, register C is set to 0.
def eqri(a, b, c):
	if(int(regs[a]) == int(b)):
		regs[c] = 1
	else:
		regs[c] = 0
		
# eqrr (equal register/register) sets register C to 1 if register A is equal to register B.
# Otherwise, register C is set to 0.
def eqrr(a, b, c):
	if(int(regs[a]) == int(regs[b])):
		regs[c] = 1
	else:
		regs[c] = 0

if __name__ == "__main__":

	# map string to function
	op = {"addr" : addr, "addi" : addi, "mulr" : mulr, "muli" : muli, "banr" : banr, "bani" : bani, "borr" : borr, "bori" :bori, "setr" : setr, "seti" : seti, "gtir" : gtir, "gtri" : gtri, "gtrr" : gtrr, "eqir" : eqir, "eqri" : eqri, "eqrr" : eqrr}

	program = []
	
	# Part 1 Solution
	
	with open("day21_input", "r") as infile:
		for line in infile.readlines():
			program.append(line.strip().split(" "))
			
	ip_line = ''.join(program.pop(0))
	ip_line = ip_line.replace("#ip", '').strip() # ip_line contains IP register number
	
	reset()
	ip = 0
	regs["0"] = 2985446
	while ip < len(program) and ip > -1:
		regs[ip_line] = ip
		op[program[ip][0]](program[ip][1],program[ip][2],program[ip][3])
		ip = regs[ip_line]
		ip += 1
		#print regs_dump()
	print regs_dump()[0]
	
	# Part 2 Solution
	
	seen = []

	reset()
	ip = 0
	looped = False
	while ip < len(program) and ip > -1 and not looped:
		regs[ip_line] = ip
		op[program[ip][0]](program[ip][1],program[ip][2],program[ip][3])
		ip = regs[ip_line]
		ip += 1
		if ip == 29:
			if regs["4"] in seen:
				print seen[-1]
				looped = True
			else:
				seen.append(regs["4"])
				#print regs["4"]

			
			
	
