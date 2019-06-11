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


import sys
import os
import argparse
import platform
import time
import mmap
import zipfile
import tarfile
import shutil
import tempfile

parser = argparse.ArgumentParser(
	description="Takes UTF-8 decodable logs (aka nearly all logs) and reads"
	+ " them, scanning for keywords.", 
	prefix_chars="-/"
)
parser.add_argument(
	"-l", 
	"--logpath", 
	help = "the path to the logfile. If your log is in a different directory,"
	+ " use an equals between the -s/--savename and your path"
	+ " (aka an absolute path)."
	+ " Supports files, directories, zip files, and tar files."
	+ " Recursively searches, so use with caution." ,
	type = str,
	metavar = "<log path>"
)
parser.add_argument(
	"-s", 
	"--savename", 
	help = "What to save the parsed log as. If you want it in a different"
	+ " directory, use an equals between the -s/--savename and your path"
	+ " (aka an absolute path).",
	metavar = "<save name>"
	)
parser.add_argument(
	"-r", 
	"--risky", 
	help = "does riskier operations for potentially more speed. "
	+ " This actually doesn't do much at the moment...", 
	action = "store_true"
)
parser.add_argument(
	"-f",
	"--force",
	help="removes safety checks, and (if permissions are high enough)"
	+ " always does certain tasks.",
	action="store_true"
)
parser.add_argument(
	"-x", 
	"--fun", 
	help="starts the fun by adding the spinner! "
			+ "its so fun, your cpu will forget to do work-"
			+ " execution is 2-6x slower with this on, beware",
	action="store_true"
)
osGroup = parser.add_mutually_exclusive_group()
osGroup.add_argument(
	"-u", "--unix", help="forces unix OS detection", action="store_true"
)
osGroup.add_argument(
	"-w", "--windows", help="forces windows OS detection", action="store_true"
)
verboistyGroup = parser.add_mutually_exclusive_group()
verboistyGroup.add_argument(
	"-v",
	"--verbose",
	help="intensifies console output. Use more v's for more output."
	+ " 3+ v's will print *e v e r y t h i n g* .",
	action="count"
)
verboistyGroup.add_argument(
	"-q", 
	"--quiet", 
	help="reduces console output. Use more q's for less output."
	+ " Once I actually implement it, 3+ q's will disable stdout.", 
	action="count"
)
parser.add_argument(
	"-k", 
	"--keyword", 
	help="keywords to search for. Put this at the end of your command,"
	+ " and then enter as many keywords as you want.", 
	nargs=argparse.REMAINDER
)
args = parser.parse_args()

if not args.force:
	import psutil
	process = psutil.Process(os.getpid())

"""
saves to a temporary file in the same directory, and once its verified
 the tmpfile is renamed to a user defined value
 (default is "parsedLog")
"""
def saveFile(listToBeWriten, name = "parsedLog"):
	f = open("tmpFile", "w")
	vprint("saving file...", 2)
	for line in listToBeWriten:
		f.write(line)
		spinningLoad()
	f.flush()
	os.fsync(f.fileno())
	f.close()
	shutil.copy("tmpFile", name) #os.copy doesn't work across different filesystems
	os.remove("tmpFile")
	vprint("file saved!", 2)

"""
if quiet, only print when priority is higher than quiet level
 (eg. "q" will print 2 and up, "qq" will print 3 and up...)
if verbose, print when priority level is higher than 1 - verbose level
 (eg. "v" will print 0 and up, "vv" will print -1 and up...)
if neither, print when verbosity is 1 or higher

3+	: important (exceptions, etc)									<qq>
2	: program operation info (eg. prompting user, posting status...)<q>
1	: operation info (eg. listing directories, progress bars...)	<default min>
0	: info (opened file, closed file...)							<v>
less: debug															<vv>
"""
def vprint(printString, priority = 0, sep = " ", end = "\n"):
	if priority >= 3:
		print(printString, sep, end)
	else:
		if args.verbose:
			if priority >= 1 - args.verbose:
				print(printString, sep, end)
		elif args.quiet:
			if args.quiet < priority:
				print(printString, sep, end)
		elif priority > 0:
			print(printString, sep, end)

"""
adds a neat little spinning line, to let the user know the program
 is still running.
Program execution is slower with this on. Like, 3-6x slower.
 I need to do something with multiprocessing to fix that, but I"m not
  completely sure how to use it. It will be fixed, eventually.
Needs a global int named "state".
"""
state = 1
def spinningLoad():
	global state
	if not args.fun:
		return
	spinner = {
		1: "v",
		2: "<",
		3: "^",
		4: ">"
	}
	if state == 4:
		state = 1
	else:
		state += 1
	print("\b" + spinner.get(state, ""), end="\r")
		
"""
Gets keywords from stdin until the user enters an empty string.
Returns the list of keywords entered.
"""
def getKeywords():
	vprint("Hit enter without typing anything else to finish inputting strings.", 1)
	keywordList = []
	while True:
		print("< ", end="")
		keyword = input()
		if not keyword:
			return keywordList
		keywordList.append(keyword)		

"""
Reads a file located at a given path.
Checks that the file can actually be read without running out of memory
 (unless the f or q flag has been set)
Then proceeds to read the file. Each line is checked for keywords, and 
 then placed in a list if it matches any of the keywords.
Also checks if path is a directory; if so, it reads all files in that
 directory.
Also checks if path is a compressed (tar or zip) file; if so,
 readCompressedFile() is called.
"""	
def readFile(filepath, keywords, recursions = 0):
	filelines = []
	if os.path.isdir(filepath):
		dirList = listDirectory(filepath, returnDir=True)
		for files in dirList: #fully recursive, be careful
			filelines.append("\n-----<<<" + (filepath + "/" + files) + ">>>-----\n")
			filelines.append("{{" + str(recursions) + " recursion(s) deep" + "}}\n")
			filelines.extend(readFile(filepath + "/" + files, keywords, recursions+1))
		return filelines
	elif zipfile.is_zipfile(filepath):
		with zipfile.ZipFile(filepath, "r") as zipped:
			#temp directory / this program's temp / the zip file / *files inside
			tempPath = tempfile.gettempdir() + "/logParserTemp/" + filepath.split("/")[len(filepath.split("/"))-1]
			zipped.extractall(path = tempPath)
			return readFile(tempPath, keywords, recursions+1)
	elif tarfile.is_tarfile(filepath):
		with tarfile.open(filepath, "r:*") as tarred:
			tempPath = tempfile.gettempdir() + "/logParserTemp/" + filepath.split("/")[len(filepath.split("/"))-1]
			tarred.extractall(path = tempPath)
			return readFile(tempPath, keywords, recursions+1)
	#elif 
	vprint("Opening file: "+filepath, -1)
	#actual line reading
	vprint("Reading lines, please wait...", 2)
	try:
		if not args.force and not args.quiet:
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
				choice=input("This file is larger than your RAM, but may be small"
								+ " enough to fit in swap. This is probably "
								+ "a bad idea. Continue? (y/n)\n> ")
				if (choice.lower() == "n"):
					return filelines
		start_time = executionTimer()
		with open(filepath, "r") as f:
			#read the line, and check for keywords
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
				spinningLoad()
		executionTimer(start_time)
	except UnicodeDecodeError as e:
		vprint(e, 2)
		return ["File is a bytefile- UTF-8 can't decode bytefiles, skipped"]
	except PermissionError:
		vprint("Can't open file- permission denied", 3)
		return ["Permission denied for this file"]
	except FileNotFoundError:
		vprint("File not found...", 3)
		return ["File not found"]
	return filelines
	

"""
Takes a time, and subtracts it from the current time.
"""
def executionTimer(startTime = None):
	if startTime is None:
		return time.time()
	exe_time = time.time() - startTime
	if exe_time > 7200:	#if above 2 hrs, show by hours
		vprint("<< {} hours >>".format(exe_time/3600), -1)
	elif exe_time > 600:	#if above 10 minutes, show by minutes
		vprint("<< {} minutes >>".format(exe_time/60), -1)
	else:
		vprint("<< {} seconds >>" .format(exe_time), -1)
	
"""
takes a list and prints each element on its own line
prints until the screen is 2 lines away from being filled, then prompts
 user to continue or stop
"""
def viewLines(filelines):
	currentLine = 0
	while True: #emulated do-while loop
		currentLine += os.get_terminal_size(0)[1]-2
		for i in range(currentLine): 
			try:
				print(filelines[i], end="")
			except:
				vprint("<<<<End of lines>>>>", 2, end="")
				currentLine = 0
		choice = input("\nMore? (Y/n)\n> ")
		if choice.lower() == "n":
			break

"""
prints out a command the user could use next time if they want to
 automate running this.
Something tells me there's a smarter way of doing this.
"""
def automateCommandBuilder(path, keywords):
	autoCommandString = os.path.basename(__file__)
	autoCommandString += " -l " + path
	if args.force:
		autoCommandString += " -f"
	if args.fun:
		autoCommandString += " -x"
	if args.verbose:
		autoCommandString += " -" + ("v"*args.verbose)
	if args.unix:
		autoCommandString += " -u"
	elif args.windows:
		autoCommandString += " -w"
	if args.savename:
		autoCommandString += " -s " + args.savename
	if args.risky:
		autoCommandString += " -r"
	autoCommandString += " -k"
	for line in keywords:
		autoCommandString += " " + line
	vprint("Protip: automate this command using \"" + autoCommandString + "\"", 1)

"""
Lists all files in a given directory.
"""
def listDirectory(path = os.getcwd(), returnDir = False):
	directory = os.listdir(path)
	for line in directory:
		pass
		vprint(line, 1)

	if returnDir:
		return directory

"""
<<Main Method>>
"""
vprint(args, 0)
filelines = []
if args.keyword and args.logpath and args.savename:
	filelines = readFile(args.logpath, args.keyword) #reading the file
	saveFile(filelines, args.savename) #saving the file
	sys.exit()
if args.logpath and args.keyword:
	filelines = readFile(args.logpath, args.keyword)
elif args.logpath:
	filelines = readFile(args.logpath, getKeywords())
else:
	listDirectory()
	file_path=input("Type a file from above, or type a filepath...\n> ")
	keywords = getKeywords()
	automateCommandBuilder(file_path, keywords)
	filelines = readFile(file_path, keywords)

print(len(filelines), "instances found")
while True:
	choice = input("What do you want to do with these lines?"
				+ "\n(S)ave to file\n(V)iew Logs\n(C)hange search..."
				+ "\n(E)xit\n> ")
	if choice.lower() == "e":
		vprint("exiting...", 3)
		#probably fine but should have verification? dont wanna delete user files
		shutil.rmtree(tempfile.gettempdir() + "/logParserTemp/")
		sys.exit()
	elif choice.lower() == "s":
		choice = input("Name your file...")
		saveFile(filelines, choice)
	elif choice.lower() == "v":
		viewLines(filelines)
	elif choice.lower() == "c":
		file_path=input("Type a filepath...\n> ")
		filelines = readFile(file_path, keywords)
		print(len(filelines), "instances found")
	else:
		print("choose something else")
