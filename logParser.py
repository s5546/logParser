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


'''
checks which arguments have been used VS an argument passed into this
 function
also allows for unix switches ('-') and windows options ('/')
If the argument exists, it will return true- otherwise, it will return
 false
'''
def argFormats(arg):
	arg = arg.lower()
	if ('-' + arg) in sys.argv or ('/' + arg) in sys.argv:
		return True
	return False

import sys, os, argparse, platform, time

if not argFormats('f'):
	import psutil #you'll have to install this using pip3
	process = psutil.Process(os.getpid()) 

parser = argparse.ArgumentParser(description='Choose a keyword, '
		+ 'logfile, and/or username..', prefix_chars='-/')
parser.add_argument('-k', '--keyword', help='a keyword to search for')
parser.add_argument('-l', '--logpath', help='the path to the logfile')
parser.add_argument('-s', '--savename', help='the name for the parsed log')
args = parser.parse_args()

'''
saves to a temporary file in the same directory, and once its verified
 the tmpfile is renamed to a user defined value
 (default is "parsedLog')
'''
def saveFile(listToBeWriten, name = "parsedLog"):
	f = open('tmpFile', 'w')
	qprint("saving file...")
	for line in listToBeWriten:
		f.write(line)
		spinningLoad()
	f.flush()
	os.fsync(f.fileno())
	f.close()
	os.rename('tmpFile', name)
	qprint("file saved!")

'''
checks for the quiet flag, and if absent it prints
	maybe expand upon this? like also checking for verbosity?
'''
def qprint(arg):
	if not argFormats('q'):
		print(arg)

'''
adds a neat little spinning line, to let the user know the program
 is still running.
Program execution is *sligtly* slower with this on.
It can be turned off with the x switch, but that's no fun.
Needs a global int named "state".
'''
state = 1
def spinningLoad():
	global state
	if argFormats('x'):
		return
	spinner = {
		1: '|',
		2: '/',
		3: '-',
		4: '\\'
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
def readFile(filepath):
	file1lines = []
	if not argFormats('f') or not argFormats('q'):
		statinfo = os.stat(filepath)
		mem=psutil.virtual_memory()
		swapmem=psutil.swap_memory()
		if (statinfo.st_size > mem.total):
			print("File larger than memory space." 
					+ "\nEither upgrade your computer, or allocate more swap"
					+ " space to process this (albeit slowly).") 
			return file1lines
		elif (statinfo.st_size > mem.available):
			print("File size: {s} \t\t Free RAM + Swap: {f}".format(s=statinfo.st_size, f=(swapmem.free+mem.available)))
			choice=input('This file is larger than your RAM, but may be small'
							+ ' enough to fit in swap. This is probably '
							+ 'a bad idea. Continue? (y/n)\n> ')
			if (choice.lower() == 'n'):
				return file1lines
	qprint("Opening file: "+filepath)
	file1 = open(filepath)
	qprint("Reading lines, please wait...")
	start_time = time.time()
	word = ''
	for line in file1:
		file1lines.append(line)
		if not argFormats('x'):
			spinningLoad()
	qprint("Data gotten! Closing file")
	executionTimer(start_time, time.time())
	return file1lines
	
'''
Takes two times, and subtracts the first from the second.
 What's left over represents how long something took to execute.
'''
def executionTimer(startTime, endTime):
	exe_time = endTime - startTime
	if exe_time > 7200:	#if above 2 hrs, show by hours
		print("<< %s hours >>\n(multiply by 60 to get seconds)" % exe_time/60)
	elif exe_time > 600:	#if above 10 minutes, show by minutes
		print("<< %s minutes >>\nmultiply by 10 to get seconds" % exe_time/10)
	else:
		print("<< %s seconds >>" % exe_time)
		
'''
Looks through each line of a list, adding any line containing the
 keyword (obtained via user input) to another list.
The list is returned at the end of the function.
'''
def parseList(file1lines):
	searchTerm = input("Type a keyword to search for...\n> ")
	termsFound = []
	for line in file1lines:
		if searchTerm in line:
			termsFound.append(line)
	return termsFound
	
'''
LLooks through each line of a list, adding any line containing the
 keyword (obtained via arguments) to another list.
The list is returned at the end of the function.
'''
def parseList(file1lines, searchTerm):
	termsFound = []
	for line in file1lines:
		if searchTerm in line:
			termsFound.append(line)
	return termsFound

'''
<<Main Method>>
'''

if argFormats('k') and argFormats('l') and argFormats('s'):
	#do the program with no user input
	file1lines = readFile(args.logpath) #reading the file
	termsFound = parseList(file1lines, args.keyword) #parsing the file
	saveFile(termsFound, args.savename) #saving the file
	sys.exit()

if platform.system() == "Windows":
	dir = os.popen("dir").readLines()
	if argFormats('l'):
		qprint("Arguments forcing Linux directory printing.")
		dir = os.popen("ls").readLines()
else:
	if argFormats('w'):
		qprint("Arguments forcing Windows directory printing.")
		dir = os.popen("dir").readLines()
	dir = os.popen("ls").readlines()
for line in dir:
	qprint(line)
	 
file1_path=input("Type a file from above, or type a filepath...\n> ")
file1lines = readFile(file1_path)
termsFound = parseList(file1lines)
print(str(len(termsFound)) + " instances found")
while True: #replace this with a better loop? 
	choice = input("What do you want to do with these lines?"
				+ "\n(S)ave to file\n(V)iew Logs\n(C)hange search term"
				+ "\n(E)xit\n> ")
	if choice.lower() == 'e':
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
					print("End of lines, restart (y) or end (N)?")
					time.sleep(1)
					choice = input("\n> ")
					if choice.lower() == 'y':
						currentLine = 0
					else:
						break
			choice = input("\nMore? (Y/n)\n> ")
			if choice.lower() == 'n':
				break
	elif choice.lower() == 'c':
		termsFound = parseList(file1lines)
		print(str(len(termsFound)) + " instances found")
	else:
		print("choose something else")
