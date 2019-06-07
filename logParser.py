#!/usr/bin/python3
#  logParser.py
#  
#  Copyright 2019 Spencer Finch <altmcman@gmail.com>
#  
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#  
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#  
#  


import sys, os, argparse, platform, time
from itertools import islice
from pathlib import Path
parser = argparse.ArgumentParser(description='Choose a keyword, '
		+ 'logfile, and/or username..', prefix_chars='-/')
parser.add_argument('-k', '--keyword', help='a keyword to search for')
parser.add_argument('-l', '--logpath', help='the path to the logfile', type=str)
parser.add_argument('-s', '--savename', help='the name for the parsed log')
parser.add_argument('-f', '--force', help="remove safety checks", action="store_true")
parser.add_argument('-x', '--nofun', help="stops the fun by removing the spinner", action="store_true")
osGroup = parser.add_mutually_exclusive_group()
osGroup.add_argument('-u', '--unix', help="forces unix OS detection", action="store_true")
osGroup.add_argument('-w', '--windows', help="forces windows OS detection", action="store_true")
verboistyGroup = parser.add_mutually_exclusive_group()
verboistyGroup.add_argument('-v', '--verbose', help="intensifies console output", action="count")
verboistyGroup.add_argument('-q', '--quiet', help="reduces console output", action="count")
args = parser.parse_args()
print(args)

if not args.force:
	import psutil #you'll have to install this using pip3
	process = psutil.Process(os.getpid())

'''
saves to a temporary file in the same directory, and once its verified
 the tmpfile is renamed to a user defined value
 (default is "parsedLog')
'''
def saveFile(listToBeWriten, name = "parsedLog"):
	f = open('tmpFile', 'w')
	vprint("saving file...", 2)
	for line in listToBeWriten:
		f.write(line)
		spinningLoad()
	f.flush()
	os.fsync(f.fileno())
	f.close()
	os.rename('tmpFile', name)
	vprint("file saved!", 2)

'''
if quiet, only print when priority is higher than quiet level
 (eg. 'q' will print 2 and up, 'qq' will print 3 and up...)
if verbose, print when priority level is higher than 1 - verbose level
 (eg. 'v' will print 0 and up, 'vv' will print -1 and up...)
if neither, print when verbosity is 1 or higher

3+	: important (exceptions, etc)									<qq>
2	: program operation info (eg. prompting user, posting status...)<q>
1	: operation info (eg. listing directories, progress bars...)	<default min>
0	: info (opened file, closed file...)							<v>
less: debug															<vv>
'''
def vprint(printString, priority = 0):
	if priority >= 3:
		print(printString)
	else:
		if args.verbose:
			if priority >= 1 - args.verbose:
				print(printString)
		elif args.quiet:
			if args.quiet < priority:
				print(printString)
		elif priority > 0:
			print(printString)

'''
adds a neat little spinning line, to let the user know the program
 is still running.
Program execution is slower with this on. Like, 3x slower.
 I need to do something with multiprocessing to fix that, but I'm not
  completely sure how to use it. It will be fixed, eventually.
It can be turned off with the x switch, but that's no fun.
Needs a global int named "state".
'''
state = 1
def spinningLoad():
	global state
	if args.nofun:
		return
	spinner = {
		1: 'v',
		2: '<',
		3: '^',
		4: '>'
	}
	if state == 4:
		state = 1
	else:
		state += 1
	print('\b' + spinner.get(state, ''), end="\r")
		
'''
Reads a file located at a given path.
Checks that the file can actually be read without running out of memory
 (unless the f or q flag has been set)
Then proceeds to read the file and place each line in a list, one by one
'''	
def readFile(filepath, keywords):
	filelines = []
	vprint("Opening file: "+filepath, -1)
	#safety checking, for if the file can actually be loaded
	if not args.force or not args.quiet:
		statinfo = os.stat(filepath)
		mem=psutil.virtual_memory()
		swapmem=psutil.swap_memory()
		if (statinfo.st_size > mem.available+swapmem.free):
			vprint("File larger than memory space." 
					+ "\nEither upgrade your computer, allocate more swap"
					+ " space to process this (albeit slowly), or"
					+ "\nclose some programs.", 3) 
			return filelines
		elif (statinfo.st_size > mem.available):
			print("File size: {s} \t\t Free RAM + Swap: {f}".format(s=statinfo.st_size, f=(swapmem.free+mem.available)))
			choice=input('This file is larger than your RAM, but may be small'
							+ ' enough to fit in swap. This is probably '
							+ 'a bad idea. Continue? (y/n)\n> ')
			if (choice.lower() == 'n'):
				return filelines
	vprint("Reading lines, please wait...", 2)
	start_time = executionTimer()
	try:
		with open(filepath, 'r') as f: 
			while True:
				lineString = f.readline()
				if not lineString:
					break
				keyFound = False
				for key in keywords:
					if key in lineString:
						keyFound = True
				if keyFound:
					filelines.append(lineString)
	except Exception as e:
		print(e)
		return readFile(input("Error reading file: Check the name/filepath, and your "
		+ "permissions. \nChoose a different file:\n> "))
	vprint("Data gotten! Closing file", 0)
	executionTimer(start_time)
	
	return filelines
	
'''
Takes a time, and subtracts it from the current time.
'''
def executionTimer(startTime = None):
	if startTime == None:
		return time.time()
	exe_time = time.time() - startTime
	if exe_time > 7200:	#if above 2 hrs, show by hours
		vprint("<< {} hours >>".format(exe_time/3600), -1)
	elif exe_time > 600:	#if above 10 minutes, show by minutes
		vprint("<< {} minutes >>".format(exe_time/60), -1)
	else:
		vprint("<< {} seconds >>" .format(exe_time), -1)
		
'''
Looks through each line of a list, adding any line containing the
 keyword (obtained via user input or argument) to another list.
The list is returned at the end of the function.
'''
def parseList(filelines, searchterm=None):
	if searchterm == None:
		searchTerm = input("Type a keyword to search for...\n> ")
	termsFound = []
	for line in filelines:
		if searchTerm in line:
			termsFound.append(line)
	return termsFound

'''
<<Main Method>>
'''

if args.keyword and args.logpath and args.savename:
	#do the program with no user input
	filelines = readFile(args.logpath, args.keyword) #reading the file
	saveFile(termsFound, args.savename) #saving the file
	sys.exit()

if platform.system() == "Windows":
	dir = os.popen("dir").readLines()
	if args.linux:
		vprint("Arguments forcing Linux directory printing.", 0)
		dir = os.popen("ls").readLines()
else:
	if args.windows:
		vprint("Arguments forcing Windows directory printing.", 0)
		dir = os.popen("dir").readLines()
	dir = os.popen("ls").readlines()
for line in dir:
	vprint(line, 1)
if args.logpath:
	filelines = readFile(args.logpath, ['password'])
else:
	file1_path=input("Type a file from above, or type a filepath...\n> ")
	filelines = readFile(file1_path, ['password'])



termsFound = parseList(filelines)
print(str(len(termsFound)) + " instances found")
while True:
	choice = input("What do you want to do with these lines?"
				+ "\n(S)ave to file\n(V)iew Logs\n(C)hange search..."
				+ "\n(E)xit\n> ")
	if choice.lower() == 'e':
		vprint("exiting...", 2)
		sys.exit()
	elif choice.lower() == 's':
		choice = input("Name your file...")
		saveFile(termsFound, choice)
	elif choice.lower() == 'v':
		currentLine = 0
		while True: #emulated do-while loop
			currentLine += os.get_terminal_size(0)[1]-2
			for i in range(currentLine): 
				try:
					print(termsFound[i], end='')
				except:
					vprint("<<<<End of lines>>>>", 2)
					currentLine = 0
			choice = input("\nMore? (Y/n)\n> ")
			if choice.lower() == 'n':
				break
	elif choice.lower() == 'c':
		file1_path=input("Type a filepath...\n> ")
		filelines = readFile(file1_path)
		termsFound = parseList(filelines)
		print(str(len(termsFound)) + " instances found")
	else:
		print("choose something else")

