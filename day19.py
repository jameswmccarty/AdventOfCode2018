#!/usr/bin/python

import math

"""
--- Day 19: Go With The Flow ---

With the Elves well on their way constructing the North Pole base, you turn your attention back to understanding the inner workings of programming the device.

You can't help but notice that the device's opcodes don't contain any flow control like jump instructions. The device's manual goes on to explain:

"In programs where flow control is required, the instruction pointer can be bound to a register so that it can be manipulated directly. This way, setr/seti can function as absolute jumps, addr/addi can function as relative jumps, and other opcodes can cause truly fascinating effects."

This mechanism is achieved through a declaration like #ip 1, which would modify register 1 so that accesses to it let the program indirectly access the instruction pointer itself. To compensate for this kind of binding, there are now six registers (numbered 0 through 5); the five not bound to the instruction pointer behave as normal. Otherwise, the same rules apply as the last time you worked with this device.

When the instruction pointer is bound to a register, its value is written to that register just before each instruction is executed, and the value of that register is written back to the instruction pointer immediately after each instruction finishes execution. Afterward, move to the next instruction by adding one to the instruction pointer, even if the value in the instruction pointer was just updated by an instruction. (Because of this, instructions must effectively set the instruction pointer to the instruction before the one they want executed next.)

The instruction pointer is 0 during the first instruction, 1 during the second, and so on. If the instruction pointer ever causes the device to attempt to load an instruction outside the instructions defined in the program, the program instead immediately halts. The instruction pointer starts at 0.

It turns out that this new information is already proving useful: the CPU in the device is not very powerful, and a background process is occupying most of its time. You dump the background process' declarations and instructions to a file (your puzzle input), making sure to use the names of the opcodes rather than the numbers.

For example, suppose you have the following program:

#ip 0
seti 5 0 1
seti 6 0 2
addi 0 1 0
addr 1 2 3
setr 1 0 0
seti 8 0 4
seti 9 0 5

When executed, the following instructions are executed. Each line contains the value of the instruction pointer at the time the instruction started, the values of the six registers before executing the instructions (in square brackets), the instruction itself, and the values of the six registers after executing the instruction (also in square brackets).

ip=0 [0, 0, 0, 0, 0, 0] seti 5 0 1 [0, 5, 0, 0, 0, 0]
ip=1 [1, 5, 0, 0, 0, 0] seti 6 0 2 [1, 5, 6, 0, 0, 0]
ip=2 [2, 5, 6, 0, 0, 0] addi 0 1 0 [3, 5, 6, 0, 0, 0]
ip=4 [4, 5, 6, 0, 0, 0] setr 1 0 0 [5, 5, 6, 0, 0, 0]
ip=6 [6, 5, 6, 0, 0, 0] seti 9 0 5 [6, 5, 6, 0, 0, 9]

In detail, when running this program, the following events occur:

    The first line (#ip 0) indicates that the instruction pointer should be bound to register 0 in this program. This is not an instruction, and so the value of the instruction pointer does not change during the processing of this line.
    The instruction pointer contains 0, and so the first instruction is executed (seti 5 0 1). It updates register 0 to the current instruction pointer value (0), sets register 1 to 5, sets the instruction pointer to the value of register 0 (which has no effect, as the instruction did not modify register 0), and then adds one to the instruction pointer.
    The instruction pointer contains 1, and so the second instruction, seti 6 0 2, is executed. This is very similar to the instruction before it: 6 is stored in register 2, and the instruction pointer is left with the value 2.
    The instruction pointer is 2, which points at the instruction addi 0 1 0. This is like a relative jump: the value of the instruction pointer, 2, is loaded into register 0. Then, addi finds the result of adding the value in register 0 and the value 1, storing the result, 3, back in register 0. Register 0 is then copied back to the instruction pointer, which will cause it to end up 1 larger than it would have otherwise and skip the next instruction (addr 1 2 3) entirely. Finally, 1 is added to the instruction pointer.
    The instruction pointer is 4, so the instruction setr 1 0 0 is run. This is like an absolute jump: it copies the value contained in register 1, 5, into register 0, which causes it to end up in the instruction pointer. The instruction pointer is then incremented, leaving it at 6.
    The instruction pointer is 6, so the instruction seti 9 0 5 stores 9 into register 5. The instruction pointer is incremented, causing it to point outside the program, and so the program ends.

What value is left in register 0 when the background process halts?

--- Part Two ---

A new background process immediately spins up in its place. It appears identical, but on closer inspection, you notice that this time, register 0 started with the value 1.

What value is left in register 0 when this new background process halts?

--- PROGRAM ---

#ip 4 ; Register #4 is IP
00 addi 4 16 4 ; jump to line 17
01 seti 1 4 3  ; R3 = 1
02 seti 1 3 5  ; R5 = 1
03 mulr 3 5 1  ; R1 = R3 * R5
04 eqrr 1 2 1  ; If R2 = R1, then R1=1, else R1=0
05 addr 1 4 4  ; R4 = R4 + R1 
06 addi 4 1 4  ; R4 = R1 + R4 ' Skipped if R2=R1
07 addr 3 0 0  ; R0 = R3 + R0 
08 addi 5 1 5  ; R5 = R5 + 1
09 gtrr 5 2 1  ; If R5 > R2, R1=1, else R1 = 0
10 addr 4 1 4  ; R4 = R1 + R4 
11 seti 2 9 4  ; R4 = 2 ' Skipped if R5 > R2
12 addi 3 1 3  ; R3 = R3 + 1
13 gtrr 3 2 1  ; If R3 > R2, R1 = 1, else R1 = 0
14 addr 1 4 4  ; R4 = R4 + R1
15 seti 1 6 4  ; R4 = 1 ' Skipped if R3 > R2
16 mulr 4 4 4  ; R4 = R4 * R4
17 addi 2 2 2  ; R2 = R2 + 2
18 mulr 2 2 2  ; R2 = R2 * R2
19 mulr 4 2 2  ; R2 = R4 * R2
20 muli 2 11 2 ; R2 = R2 * 11
21 addi 1 2 1  ; R1 = R1 + 2
22 mulr 1 4 1  ; R1 = R4 * R1
23 addi 1 7 1  ; R1 = R1 + 7
24 addr 2 1 2  ; R2 = R1 + R2
25 addr 4 0 4  ; R4 = R0 + R4 '1 is stored in R0 --> Skips to line 27
26 seti 0 8 4  ; R4 = 0 ' returns to program start if R0 = 0
27 setr 4 3 1  ; R1 = R4
28 mulr 1 4 1  ; R1 = R4 * R1
29 addr 4 1 1  ; R1 = R4 + R1
30 mulr 4 1 1  ; R1 = R4 * R1
31 muli 1 14 1 ; R1 = R1 * 14
32 mulr 1 4 1  ; R1 = R4 * R1
33 addr 2 1 2  ; R2 = R1 + R2
34 seti 0 3 0  ; R0 = 0 ' if we get here, orig exec pathway...
35 seti 0 6 4  ; R4 = 0 -- Jump to line 0 (line 1 after IP+)

 ----- PROGRAM TRACE ----
 
Line:  0  ['addi', '4', '16', '4'] [1, 0, 0, 0, 0, 0] ; jump to line 17
Line:  17 ['addi', '2', '2', '2'] [1, 0, 0, 0, 17, 0]
Line:  18 ['mulr', '2', '2', '2'] [1, 0, 2, 0, 18, 0]
Line:  19 ['mulr', '4', '2', '2'] [1, 0, 4, 0, 19, 0]
Line:  20 ['muli', '2', '11', '2'] [1, 0, 76, 0, 20, 0]
Line:  21 ['addi', '1', '2', '1'] [1, 0, 836, 0, 21, 0]
Line:  22 ['mulr', '1', '4', '1'] [1, 2, 836, 0, 22, 0]
Line:  23 ['addi', '1', '7', '1'] [1, 44, 836, 0, 23, 0]
Line:  24 ['addr', '2', '1', '2'] [1, 51, 836, 0, 24, 0]
Line:  25 ['addr', '4', '0', '4'] [1, 51, 887, 0, 25, 0]
Line:  27 ['setr', '4', '3', '1'] [1, 51, 887, 0, 27, 0]
Line:  28 ['mulr', '1', '4', '1'] [1, 27, 887, 0, 28, 0]
Line:  29 ['addr', '4', '1', '1'] [1, 756, 887, 0, 29, 0]
Line:  30 ['mulr', '4', '1', '1'] [1, 785, 887, 0, 30, 0]
Line:  31 ['muli', '1', '14', '1'] [1, 23550, 887, 0, 31, 0]
Line:  32 ['mulr', '1', '4', '1'] [1, 329700, 887, 0, 32, 0]
Line:  33 ['addr', '2', '1', '2'] [1, 10550400, 887, 0, 33, 0]
Line:  34 ['seti', '0', '3', '0'] [1, 10550400, 10551287, 0, 34, 0]
Line:  35 ['seti', '0', '6', '4'] [0, 10550400, 10551287, 0, 35, 0]
Line:  1 ['seti', '1', '4', '3'] [0, 10550400, 10551287, 0, 1, 0]
Line:  2 ['seti', '1', '3', '5'] [0, 10550400, 10551287, 1, 2, 0]
Line:  3 ['mulr', '3', '5', '1'] [0, 10550400, 10551287, 1, 3, 1]
Line:  4 ['eqrr', '1', '2', '1'] [0, 1, 10551287, 1, 4, 1] ; reg 1 and reg 2 are equal?
Line:  5 ['addr', '1', '4', '4'] [0, 0, 10551287, 1, 5, 1] ; add regs 1 and 4, stor 4
Line:  6 ['addi', '4', '1', '4'] [0, 0, 10551287, 1, 6, 1] ; increment reg 4 (skip inst)
Line:  8 ['addi', '5', '1', '5'] [0, 0, 10551287, 1, 8, 1] ; store 1 in reg 5
Line:  9 ['gtrr', '5', '2', '1'] [0, 0, 10551287, 1, 9, 2] ; check if reg 5 > reg 2
Line:  10 ['addr', '4', '1', '4'] [0, 0, 10551287, 1, 10, 2] ; add reg 4 to reg 1 | if reg 5 is > reg 2, we'll jump to line 12 on next inst
Line:  11 ['seti', '2', '9', '4'] [0, 0, 10551287, 1, 11, 2] ; jump back to line #3 (if above not met)
Line:  3 ['mulr', '3', '5', '1'] [0, 0, 10551287, 1, 3, 2]   ; multiply reg 3 by reg 5, stor 1
Line:  4 ['eqrr', '1', '2', '1'] [0, 2, 10551287, 1, 4, 2]
Line:  5 ['addr', '1', '4', '4'] [0, 0, 10551287, 1, 5, 2]
Line:  6 ['addi', '4', '1', '4'] [0, 0, 10551287, 1, 6, 2]
Line:  8 ['addi', '5', '1', '5'] [0, 0, 10551287, 1, 8, 2]
Line:  9 ['gtrr', '5', '2', '1'] [0, 0, 10551287, 1, 9, 3]
Line:  10 ['addr', '4', '1', '4'] [0, 0, 10551287, 1, 10, 3]
Line:  11 ['seti', '2', '9', '4'] [0, 0, 10551287, 1, 11, 3]
Line:  3 ['mulr', '3', '5', '1'] [0, 0, 10551287, 1, 3, 3]
Line:  4 ['eqrr', '1', '2', '1'] [0, 3, 10551287, 1, 4, 3]
Line:  5 ['addr', '1', '4', '4'] [0, 0, 10551287, 1, 5, 3]
Line:  6 ['addi', '4', '1', '4'] [0, 0, 10551287, 1, 6, 3]
Line:  8 ['addi', '5', '1', '5'] [0, 0, 10551287, 1, 8, 3]
Line:  9 ['gtrr', '5', '2', '1'] [0, 0, 10551287, 1, 9, 4]
Line:  10 ['addr', '4', '1', '4'] [0, 0, 10551287, 1, 10, 4]
Line:  11 ['seti', '2', '9', '4'] [0, 0, 10551287, 1, 11, 4]

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

	# Part 1 Solution

	# map string to function
	op = {"addr" : addr, "addi" : addi, "mulr" : mulr, "muli" : muli, "banr" : banr, "bani" : bani, "borr" : borr, "bori" :bori, "setr" : setr, "seti" : seti, "gtir" : gtir, "gtri" : gtri, "gtrr" : gtrr, "eqir" : eqir, "eqri" : eqri, "eqrr" : eqrr}

	program = []
	
	with open("day19_input", "r") as infile:
		for line in infile.readlines():
			program.append(line.strip().split(" "))
			
	ip_line = ''.join(program.pop(0))
	ip_line = ip_line.replace("#ip", '').strip() # ip_line contains IP register number
	
	reset()
	ip = 0
	while ip < len(program) and ip > -1:
		regs[ip_line] = ip
		op[program[ip][0]](program[ip][1],program[ip][2],program[ip][3])
		ip = regs[ip_line]
		ip += 1
		#print regs_dump()
	print regs_dump()[0]
	
	# Part 2 Solution
	
	"""
	program = []
	
	with open("day19_input", "r") as infile:
		for line in infile.readlines():
			program.append(line.strip().split(" "))
			
	ip_line = ''.join(program.pop(0))
	ip_line = ip_line.replace("#ip", '').strip() # ip_line contains IP register number
	
	reset()
	
	regs["0"] = 1
	
	ip = 0
	while ip < len(program) and ip > -1:
		regs[ip_line] = ip
		print "Line: ", ip, program[ip], regs_dump()
		op[program[ip][0]](program[ip][1],program[ip][2],program[ip][3])
		ip = regs[ip_line]
		ip += 1
		#print regs_dump()
	print regs_dump()[0]
	"""
	
	"""
	R0 will contain a sum of numbers that are factors of the value in R2 (10551287)
	"""
	
	target_val = 10551287
	sum_factors = 0
	for i in range(1,target_val):
		if target_val % i == 0:
			sum_factors += i
	print sum_factors + target_val
	
	
	
	
	
