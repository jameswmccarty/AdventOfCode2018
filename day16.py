#!/usr/bin/python

"""
--- Day 16: Chronal Classification ---

As you see the Elves defend their hot chocolate successfully, you go back to falling through time. This is going to become a problem.

If you're ever going to return to your own time, you need to understand how this device on your wrist works. You have a little while before you reach your next destination, and with a bit of trial and error, you manage to pull up a programming manual on the device's tiny screen.

According to the manual, the device has four registers (numbered 0 through 3) that can be manipulated by instructions containing one of 16 opcodes. The registers start with the value 0.

Every instruction consists of four values: an opcode, two inputs (named A and B), and an output (named C), in that order. The opcode specifies the behavior of the instruction and how the inputs are interpreted. The output, C, is always treated as a register.

In the opcode descriptions below, if something says "value A", it means to take the number given as A literally. (This is also called an "immediate" value.) If something says "register A", it means to use the number given as A to read from (or write to) the register with that number. So, if the opcode addi adds register A and value B, storing the result in register C, and the instruction addi 0 7 3 is encountered, it would add 7 to the value contained by register 0 and store the sum in register 3, never modifying registers 0, 1, or 2 in the process.

Many opcodes are similar except for how they interpret their arguments. The opcodes fall into seven general categories:

Addition:

    addr (add register) stores into register C the result of adding register A and register B.
    addi (add immediate) stores into register C the result of adding register A and value B.

Multiplication:

    mulr (multiply register) stores into register C the result of multiplying register A and register B.
    muli (multiply immediate) stores into register C the result of multiplying register A and value B.

Bitwise AND:

    banr (bitwise AND register) stores into register C the result of the bitwise AND of register A and register B.
    bani (bitwise AND immediate) stores into register C the result of the bitwise AND of register A and value B.

Bitwise OR:

    borr (bitwise OR register) stores into register C the result of the bitwise OR of register A and register B.
    bori (bitwise OR immediate) stores into register C the result of the bitwise OR of register A and value B.

Assignment:

    setr (set register) copies the contents of register A into register C. (Input B is ignored.)
    seti (set immediate) stores value A into register C. (Input B is ignored.)

Greater-than testing:

    gtir (greater-than immediate/register) sets register C to 1 if value A is greater than register B. Otherwise, register C is set to 0.
    gtri (greater-than register/immediate) sets register C to 1 if register A is greater than value B. Otherwise, register C is set to 0.
    gtrr (greater-than register/register) sets register C to 1 if register A is greater than register B. Otherwise, register C is set to 0.

Equality testing:

    eqir (equal immediate/register) sets register C to 1 if value A is equal to register B. Otherwise, register C is set to 0.
    eqri (equal register/immediate) sets register C to 1 if register A is equal to value B. Otherwise, register C is set to 0.
    eqrr (equal register/register) sets register C to 1 if register A is equal to register B. Otherwise, register C is set to 0.

Unfortunately, while the manual gives the name of each opcode, it doesn't seem to indicate the number. However, you can monitor the CPU to see the contents of the registers before and after instructions are executed to try to work them out. Each opcode has a number from 0 through 15, but the manual doesn't say which is which. For example, suppose you capture the following sample:

Before: [3, 2, 1, 1]
9 2 1 2
After:  [3, 2, 2, 1]

This sample shows the effect of the instruction 9 2 1 2 on the registers. Before the instruction is executed, register 0 has value 3, register 1 has value 2, and registers 2 and 3 have value 1. After the instruction is executed, register 2's value becomes 2.

The instruction itself, 9 2 1 2, means that opcode 9 was executed with A=2, B=1, and C=2. Opcode 9 could be any of the 16 opcodes listed above, but only three of them behave in a way that would cause the result shown in the sample:

    Opcode 9 could be mulr: register 2 (which has a value of 1) times register 1 (which has a value of 2) produces 2, which matches the value stored in the output register, register 2.
    Opcode 9 could be addi: register 2 (which has a value of 1) plus value 1 produces 2, which matches the value stored in the output register, register 2.
    Opcode 9 could be seti: value 2 matches the value stored in the output register, register 2; the number given for B is irrelevant.

None of the other opcodes produce the result captured in the sample. Because of this, the sample above behaves like three opcodes.

You collect many of these samples (the first section of your puzzle input). The manual also includes a small test program (the second section of your puzzle input) - you can ignore it for now.

Ignoring the opcode numbers, how many samples in your puzzle input behave like three or more opcodes?

--- Part Two ---

Using the samples you collected, work out the number of each opcode and execute the test program (the second section of your puzzle input).

What value is contained in register 0 after executing the test program?

"""

# 4 registers
regs = { "0" : 0,
		 "1" : 0,
		 "2" : 0,
		 "3" : 0}

def regs_set(a, b, c, d):
	regs["0"] = a
	regs["1"] = b
	regs["2"] = c
	regs["3"] = d

def regs_dump():
	return [ regs["0"], regs["1"], regs["2"], regs["3"] ]

# addr (add register) 
# stores into register C the result of adding register A and register B.
def addr(a,b,c):
	regs[c] = regs[a] + regs[b]

# addi (add immediate)
# stores into register C the result of adding register A and value B.	
def addi(a, b, c):
	regs[c] = regs[a] + int(b)

# mulr (multiply register) stores into register C 
# the result of multiplying register A and register B.
def mulr(a, b, c):
	regs[c] = regs[a] * regs[b]

# muli (multiply immediate) 
# stores into register C the result of multiplying register A and value B.
def muli(a, b, c):
	regs[c] = regs[a] * int(b)
	
# banr (bitwise AND register) stores into register C the result of the 
# bitwise AND of register A and register B.
def banr(a, b, c):
	regs[c] = regs[a] & regs[b]

# bani (bitwise AND immediate) stores into register C the result of the 
# bitwise AND of register A and value B.
def bani(a, b, c):
	regs[c] = regs[a] & int(b)


# borr (bitwise OR register) stores into register C the result of the 
# bitwise OR of register A and register B.
def borr(a, b, c):
	regs[c] = regs[a] | regs[b]

# bori (bitwise OR immediate) stores into register C the result of the 
# bitwise OR of register A and value B.
def bori(a, b, c):
	regs[c] = regs[a] | int(b)


# setr (set register) copies the contents of register A into register C. 
# (Input B is ignored.)
def setr(a, b, c):
	regs[c] = regs[a]

# seti (set immediate) stores value A into register C. 
# (Input B is ignored.)
def seti(a, b, c):
	regs[c] = int(a)

# gtir (greater-than immediate/register) sets register C to 1 if value A is 
# greater than register B. Otherwise, register C is set to 0.
def gtir(a, b, c):
	if(int(a) > regs[b]):
		regs[c] = 1
	else:
		regs[c] = 0

# gtri (greater-than register/immediate) sets register C to 1 if register 
# A is greater than value B. Otherwise, register C is set to 0.
def gtri(a, b, c):
	if(regs[a] > int(b)):
		regs[c] = 1
	else:
		regs[c] = 0
		
# gtrr (greater-than register/register) sets register C to 1 if register A 
# is greater than register B. Otherwise, register C is set to 0.
def gtrr(a, b, c):
	if(regs[a] > regs[b]):
		regs[c] = 1
	else:
		regs[c] = 0

# eqir (equal immediate/register) sets register C to 1 if value A is equal to register B. 
# Otherwise, register C is set to 0.
def eqir(a, b, c):
	if(int(a) == regs[b]):
		regs[c] = 1
	else:
		regs[c] = 0

# eqri (equal register/immediate) sets register C to 1 if register A is equal to value B. 
# Otherwise, register C is set to 0.
def eqri(a, b, c):
	if(regs[a] == int(b)):
		regs[c] = 1
	else:
		regs[c] = 0
		
# eqrr (equal register/register) sets register C to 1 if register A is equal to register B.
# Otherwise, register C is set to 0.
def eqrr(a, b, c):
	if(regs[a] == regs[b]):
		regs[c] = 1
	else:
		regs[c] = 0

class Sample:

	# Before: [1, 0, 2, 1]
	# 2 3 2 0
	# After:  [1, 0, 2, 1]

	def __init__(self, before, cmd, after):
		before = before.replace("Before: [", '')
		before = before.replace("]", '')
		start = before.strip().split(",")
		self.start = [ int(x) for x in start ]
		cmds = cmd.split(" ")
		self.op = cmds[0].strip()
		self.a  = cmds[1].strip()
		self.b  = cmds[2].strip()
		self.c  = cmds[3].strip()
		after = after.replace("After:  [", '')
		after = after.replace("]", '')
		after = after.strip().split(",")
		self.end = [ int(x) for x in after ]
		
	def test(self, opcode):
		
		regs_set(self.start[0], self.start[1], self.start[2], self.start[3])
		t_f = lambda x : x(self.a, self.b, self.c)
		t_f(opcode)
		
		soln = regs_dump()

		for i, val in enumerate(soln):
			if self.end[i] != val:
				return False
		return True

if __name__ == "__main__":

	opcodes = [addr, addi, mulr, muli, banr, bani, borr, bori, setr, seti, gtir, gtri, gtrr, eqir, eqri, eqrr]
	
	samples = []
	
	with open("day16_input", "r") as infile:
		while True:
			line = infile.readline()
			if not line:
				break
			if "Before" in line:
				l2  = infile.readline()
				l3  = infile.readline()
				samples.append(Sample(line, l2, l3))
	
	valid_samples = 0
	
	for sample in samples:
		sample_count = 0
		for code in opcodes:
			if sample.test(code):
				sample_count += 1
		if sample_count >= 3:
			valid_samples += 1
	
	print valid_samples
	
		
