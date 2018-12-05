#!/usr/bin/python

import time
import re

"""
--- Day 4: Repose Record ---

You've sneaked into another supply closet - this time, it's across from the prototype suit manufacturing lab. You need to sneak inside and fix the issues with the suit, but there's a guard stationed outside the lab, so this is as close as you can safely get.

As you search the closet for anything that might help, you discover that you're not the first person to want to sneak in. Covering the walls, someone has spent an hour starting every midnight for the past few months secretly observing this guard post! They've been writing down the ID of the one guard on duty that night - the Elves seem to have decided that one guard was enough for the overnight shift - as well as when they fall asleep or wake up while at their post (your puzzle input).

For example, consider the following records, which have already been organized into chronological order:

[1518-11-01 00:00] Guard #10 begins shift
[1518-11-01 00:05] falls asleep
[1518-11-01 00:25] wakes up
[1518-11-01 00:30] falls asleep
[1518-11-01 00:55] wakes up
[1518-11-01 23:58] Guard #99 begins shift
[1518-11-02 00:40] falls asleep
[1518-11-02 00:50] wakes up
[1518-11-03 00:05] Guard #10 begins shift
[1518-11-03 00:24] falls asleep
[1518-11-03 00:29] wakes up
[1518-11-04 00:02] Guard #99 begins shift
[1518-11-04 00:36] falls asleep
[1518-11-04 00:46] wakes up
[1518-11-05 00:03] Guard #99 begins shift
[1518-11-05 00:45] falls asleep
[1518-11-05 00:55] wakes up

Timestamps are written using year-month-day hour:minute format. The guard falling asleep or waking up is always the one whose shift most recently started. Because all asleep/awake times are during the midnight hour (00:00 - 00:59), only the minute portion (00 - 59) is relevant for those events.

Visually, these records show that the guards are asleep at these times:

Date   ID   Minute
            000000000011111111112222222222333333333344444444445555555555
            012345678901234567890123456789012345678901234567890123456789
11-01  #10  .....####################.....#########################.....
11-02  #99  ........................................##########..........
11-03  #10  ........................#####...............................
11-04  #99  ....................................##########..............
11-05  #99  .............................................##########.....

The columns are Date, which shows the month-day portion of the relevant day; ID, which shows the guard on duty that day; and Minute, which shows the minutes during which the guard was asleep within the midnight hour. (The Minute column's header shows the minute's ten's digit in the first row and the one's digit in the second row.) Awake is shown as ., and asleep is shown as #.

Note that guards count as asleep on the minute they fall asleep, and they count as awake on the minute they wake up. For example, because Guard #10 wakes up at 00:25 on 1518-11-01, minute 25 is marked as awake.

If you can figure out the guard most likely to be asleep at a specific time, you might be able to trick that guard into working tonight so you can have the best chance of sneaking in. You have two strategies for choosing the best guard/minute combination.

Strategy 1: Find the guard that has the most minutes asleep. What minute does that guard spend asleep the most?

In the example above, Guard #10 spent the most minutes asleep, a total of 50 minutes (20+25+5), while Guard #99 only slept for a total of 30 minutes (10+10+10). Guard #10 was asleep most during minute 24 (on two days, whereas any other minute the guard was asleep was only seen on one day).

While this example listed the entries in chronological order, your entries are in the order you found them. You'll need to organize them before they can be analyzed.

What is the ID of the guard you chose multiplied by the minute you chose? (In the above example, the answer would be 10 * 24 = 240.)

--- Part Two ---

Strategy 2: Of all guards, which guard is most frequently asleep on the same minute?

In the example above, Guard #99 spent minute 45 asleep more than any other guard or minute - three times in total. (In all other cases, any guard spent any minute asleep at most twice.)

What is the ID of the guard you chose multiplied by the minute you chose? (In the above example, the answer would be 99 * 45 = 4455.)

"""

if __name__ == "__main__":
	#Part 1 Solution
	
	log = [] # problem input
	with open("day4_input", "r") as infile:
		for line in infile.readlines():
			log.append(line.strip())
	# Order events by timestamp
	log.sort(key = lambda x : time.mktime(time.strptime("2001-" + x[6:17], "%Y-%m-%d %H:%M")))
	
	slept = None # time guard went to sleep
	guards = {}
	for event in log:
		e_time = time.mktime(time.strptime("2001-" + event[6:17], "%Y-%m-%d %H:%M"))
		if "Guard" in event: # Shift change
			g_id = re.search("\d+", event[18:]).group(0) # Pull numerical ID
		elif "asleep" in event: # Got sleepy
			slept = e_time
		elif "wakes" in event: # Woke up
			if g_id in guards.keys():
				guards[g_id].append((slept, e_time)) # tuple of time went to sleep, and time woke up
			else:
				guards[g_id] = [(slept, e_time)]
				
	totals = []
	for guard in guards.keys():
		slept = 0 #total time slept by each guard
		for event in guards[guard]:
			slept += (event[1] - event[0])/60 # convert to mins
		print "Guard " + str(guard) + " slept for " + str(slept) + " mins."
		totals.append((guard, slept))
	
	totals.sort(key = lambda x : x[1], reverse = True) # sort by sleep time
	sleepy_id = totals[0][0] # find most sleepy guard
	print "Most sleepy guard " + str(sleepy_id)
	
	mins = [0] * 60
	for event in guards[sleepy_id]: # review log for sleepy guard
		for i in range(time.gmtime(int(event[0]))[4], time.gmtime(int(event[1]))[4]): #minute to minute
			mins[i] += 1	
	print mins.index(max(mins)) * int(sleepy_id) #minute most spent asleep multiplied by guard id
	
	#Part 2 Solution
	mins_slept = [] #(Guard ID, Max Mins, Minute Most Slept)
	for guard in guards.keys():
		mins = [0] * 60
		for event in guards[guard]:
			for i in range(time.gmtime(int(event[0]))[4], time.gmtime(int(event[1]))[4]): #minute to minute
				mins[i] += 1
		mins_slept.append((guard, max(mins), mins.index(max(mins))))
	
	mins_slept.sort(key = lambda x : x[1], reverse = True)
	print int(mins_slept[0][0]) * mins_slept[0][2]	

	
	"""
	Unused code from playing with sets below.
	"""
	
	#days = {}
	#for event in guards[sleepy_id]: # review log for sleepy guard
	#	day = str(time.gmtime(int(event[0]))[1]) + " " + str(time.gmtime(int(event[0]))[2]) #mon and day
	#	for i in range(time.gmtime(int(event[0]))[4], time.gmtime(int(event[1]))[4]):
	#		if day in days.keys():
	#			days[day].add(i)
	#		else:
	#			days[day] = set()
	#			days[day].add(i)
			
	#firstset = days.values()[0]
	#print days
	#for day in days.values():
	#	print day
	#	firstset = firstset.intersection(day)
	#print firstset.pop() * int(sleepy_id)
	#print firstset
