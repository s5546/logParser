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

import argparse
import sys
import os
import zipfile
import tarfile
import shutil
import tempfile
import time
import psutil
import afl

"""
Python's input() method doesn't check that the user inputted bytes, and instead assumes the input's a string- rasing an 
exception if it's not a string. This method catches all exceptions that user input and fuzzing have shown me.
"""


def safe_input(display_string=None):
	while True:
		try:
			return input(display_string)
		except EOFError:
			vprint("Unexpected end of your input", 2)
			sys.exit(1)
		except ValueError:
			vprint("Unexpected value in your input, please try again", 2)
			return "<Unknown Value>"
		except UnicodeDecodeError:
			vprint("Unexpected value in your input, please try again", 2)
			return "<Unknown Byte>"


"""
saves to a temporary file in the same directory, and once its verified the tmpfile is renamed to a user defined value
(default is "parsedLog")
"""


def save_file(list_to_be_written, name="parsedLog"):
	try:
		f = open("tmpFile", "w")
		vprint("saving file...", 2)
		for line in list_to_be_written:
			f.write(line)
			spinning_load()
		f.flush()
		os.fsync(f.fileno())
		f.close()
		# os.copy doesn't work across different filesystems
		if name != "tmpFile":
			shutil.copy("tmpFile", name)
			os.remove("tmpFile")
		vprint("file saved!", 2)
	except PermissionError:
		vprint("Permission denied, cannot save in directory " + os.getcwd(), 2)
	except NotADirectoryError:
		vprint("Save location invalid", 2)


"""
if quiet, only print when priority is higher than quiet level (eg. "q" will print 2 and up, "qq" will print 3 and up...)
if verbose, print when priority level is higher than 1 - verbose level (eg. "v" will print 0 and up, "vv" will print -1 
and up...)
if neither, print when verbosity is 1 or higher

3+	: important (exceptions, etc)									<qq>
2	: program operation info (eg. prompting user, posting status...)<q>
1	: operation info (eg. listing directories, progress bars...)	<default>
0	: info (opened file, closed file...)							<v>
less: debug															<vv>
"""


def vprint(print_string, priority=0, sep=" ", end="\n"):
	if priority >= 3:
		print(print_string, sep, end)
	else:
		if args.verbose:
			if priority >= 1 - args.verbose:
				print(print_string, sep, end)
		elif args.quiet:
			if args.quiet < priority:
				print(print_string, sep, end)
		elif priority > 0:
			print(print_string, sep, end)


"""
adds a neat little spinning line, to let the user know the program is still running.
Program execution is slower with this on. Like, 2-6x slower. I need to do something with multiprocessing to fix that, 
but I'm not completely sure how to use it. It will be fixed, eventually.
Needs a global int named "state", but I'm looking for a not-dumb way to use local variables instead
"""


def spinning_load(version=0):
	state = 1
	print("yep")
	if not args.fun:
		return
	spinner = {}
	if version == 0:
		spinner = {
			1: "v",
			2: "<",
			3: "^",
			4: ">"
		}
	elif version == 1:
		spinner = {
			1: "/",
			2: "-",
			3: "\\",
			4: "|"
		}
	while True:
		if state == 5:
			state = 1
		print("\b" + spinner.get(state, ""), end="\r")
		yield state
		state += 1


"""
Gets keywords from stdin until the user enters an empty string.
Returns the list of keywords entered.
"""


def get_keywords():
	vprint("Hit enter without typing anything else to finish"
								+ " inputting strings.", 1)
	keyword_list = []
	while True:
		print("< ", end="")
		keyword = safe_input("")
		if not keyword:
			return keyword_list
		keyword_list.append(keyword)


"""
Reads a file located at a given path.
Checks that the file can actually be read without running out of memory (unless the f or q flag has been set)
Then proceeds to read the file. Each line is checked for keywords, and then placed in a list if it matches any of the 
keywords.
Also checks if path is a directory; if so, it reads all files in that directory.
Also checks if path is a compressed (tar or zip) file.
"""


def read_file(file_path, keywords, recursions=0):
	temp_lines = []
	current_line = 0
	print("printing: \"", file_path, "\"")
	try:
		if args.ignore_file:
			if file_path in args.ignore_file:
				return
			if os.path.isdir(file_path):
				dir_list = list_directory(file_path, True)
				for files in dir_list:  # fully recursive, be careful
					temp_lines.append("\n-----<<<" + (file_path + "/" + files) + ">>>-----\n")
					temp_lines.append("{{" + str(recursions) + " recursion(s) deep" + "}}\n")
					temp_lines.extend(read_file(file_path + "/" + files, keywords, recursions + 1))
				return temp_lines
			elif zipfile.is_zipfile(file_path):
				with zipfile.ZipFile(file_path, "r") as zipped:
					# temp directory / this program's temp / the zip file / *files inside
					temp_path = tempfile.gettempdir() + "/logParserTemp/" + file_path.split("/tmp/logParserTemp")[
						len(file_path.split("/")) - 1]
					zipped.extractall(path=temp_path)
					vprint("extracting " + temp_path, 0)
					return read_file(temp_path, keywords, recursions + 1)
			elif tarfile.is_tarfile(file_path):
				with tarfile.open(file_path, "r:*") as tarred:
					temp_path = tempfile.gettempdir() + "/logParserTemp/" + file_path.split("/")[
						len(file_path.split("/")) - 1]
	def is_within_directory(directory, target):
		
		abs_directory = os.path.abspath(directory)
		abs_target = os.path.abspath(target)
	
		prefix = os.path.commonprefix([abs_directory, abs_target])
		
		return prefix == abs_directory
	
	def safe_extract(tar, path=".", members=None, *, numeric_owner=False):
	
		for member in tar.getmembers():
			member_path = os.path.join(path, member.name)
			if not is_within_directory(path, member_path):
				raise Exception("Attempted Path Traversal in Tar File")
	
		tar.extractall(path, members, numeric_owner=numeric_owner) 
		
	
	safe_extract(tarred, path=temp_path)
					vprint("extracting " + temp_path, 0)
					return read_file(temp_path, keywords, recursions + 1)

		# actual line reading
		vprint("Reading lines, please wait...", 2)
		if not args.force and not args.quiet:
			statinfo = os.stat(file_path)
			mem = psutil.virtual_memory()
			swapmem = psutil.swap_memory()
			if statinfo.st_size > mem.available + swapmem.free:
				vprint("File larger than memory space."
											+ "\nEither upgrade your computer, allocate more swap"
											+ " space to process this (albeit slowly), or"
											+ "\nclose some programs.", 3)
				return temp_lines
			elif statinfo.st_size > mem.available:
				print("File size: {s} \t\t Free RAM + Swap: {f}".format(s=statinfo.st_size,
																		f=(swapmem.free + mem.available)))
				choice = safe_input("This file is larger than your RAM, but may be small enough to fit in swap. This is"
										+ " probably a bad idea. Continue? (y/n)\n> ")
				if choice.lower() == "n":
					return temp_lines
		vprint("Opening file: " + file_path, -1)
		start_time = execution_timer()
		with open(file_path, "r") as f:
			# Read the line, and check for keywords
			while True:
				current_line += 1
				lineString = f.readline()
				if not lineString:
					break
				key_found = False
				for key in keywords:
					if key in lineString:
						if args.ignore_keyword:
							for ig in args.ignore_keyword:
								if ig not in lineString:
									key_found = True
						else:
							key_found = True
				if key_found:
					temp_lines.append(str(current_line) + "] " + lineString)
					spinning_load()
		execution_timer(start_time)
	except PermissionError:
		vprint("Can't open file- permission denied", 3)
		return ["Permission denied for this file"]
	except FileNotFoundError:
		vprint("File not found", 3)
		return ["File not found"]
	except ValueError as e:
		vprint(e, 2)
	except NotADirectoryError:
		pass
	except UnicodeDecodeError:
		temp_lines.append(str(current_line) + " <<UnicodeDecodeError>>")
		pass
	except IsADirectoryError:
		pass
	return temp_lines


"""
Takes a time, and subtracts it from the current time.
If not given a time, returns the current time.
"""


def execution_timer(start_time=None):
	if start_time is None:
		return time.time()
	exe_time = time.time() - start_time
	if exe_time > 7200:  # if above 2 hrs, show by hours
		vprint("<< {} hours >>".format(exe_time / 3600), -1)
	elif exe_time > 600:  # if above 10 minutes, show by minutes
		vprint("<< {} minutes >>".format(exe_time / 60), -1)
	else:
		vprint("<< {} seconds >>".format(exe_time), -1)


"""
takes a list and prints each element on its own line. Prints until the screen is 2 lines away from being filled, then 
prompts user to continue or stop
"""


def view_lines(filelines):
	currentLine = 0
	while True:  # emulated do-while loop
		try:
			currentLine += os.get_terminal_size(0)[1] - 2
			for i in range(currentLine):
				print(filelines[i], end="")
			choice = safe_input("\nMore? (Y/n)\n> ")
			if choice.lower() == "n":
				break
		except OSError:  # fuzzing purposes
			break
		except: # todo: too broad, figure out what this should actually be
			vprint("<<<<End of lines>>>>", 2, end="")
			currentLine = 0


"""
prints out a command the user could use next time if they want to
	automate running this.
Something tells me there's a smarter way of doing this.
"""


def automate_command_builder(path, keywords):
	auto_command_string = os.path.basename(__file__)
	auto_command_string += " -l " + path
	if args.force:
		auto_command_string += " -f"
	if args.fun:
		auto_command_string += " -x"
	if args.verbose:
		auto_command_string += " -" + ("v" * args.verbose)
	if args.unix:
		auto_command_string += " -u"
	elif args.windows:
		auto_command_string += " -w"
	if args.savename:
		auto_command_string += " -s " + args.savename
	if args.risky:
		auto_command_string += " -r"
	auto_command_string += " -k"
	for line in keywords:
		auto_command_string += " " + line
	if args.ignore_keyword:
		auto_command_string += " -ik"
		for line in args.ignore_keyword:
			auto_command_string += " " + line
	if args.ignore_keyword:
		auto_command_string += " -if"
		for line in args.ignore_file:
			auto_command_string += " " + line
	vprint("Protip: automate this command using \"" + auto_command_string + "\"", 1)


"""
Lists all files in a given directory.
"""


def list_directory(path=None, return_dir=False):
	if path is None:
		os.getcwd()
	directory = os.listdir(path)
	for line in directory:
		vprint(line, 1)
	if return_dir:
		return directory


def parse_arguments():
	parser = argparse.ArgumentParser(
		description="Takes UTF-8 decodable logs (aka nearly all logs) and reads them, scanning for keywords.",
		prefix_chars="-/"
	)
	parser.add_argument(
		"-l",
		"--logpath",
		help="the path to the logfile. If your log is in a different directory,"
			+ " use an equals between the -l/--logname and your path (aka an absolute path)."
			+ " Supports files, directories, zip files, and tar files."
			+ " Searches recursively, so use with caution.",
		type=str,
		metavar="<log path>"
	)
	parser.add_argument(
		"-s",
		"--savename",
		help="What to save the parsed log as. If you want it in a different"
			+ " directory, use an equals between the -s/--savename and your path"
			+ " (aka an absolute path).",
		metavar="<save name>"
	)
	parser.add_argument(
		"-r",
		"--risky",
		help="does riskier operations for potentially more speed. This actually doesn't do much at the moment...",
		action="store_true"
	)
	parser.add_argument(
		"-f",
		"--force",
		help="removes safety checks, and (if permissions are high enough) always does certain tasks.",
		action="store_true"
	)
	parser.add_argument(
		"-x",
		"--fun",
		help="starts the fun by adding the spinner! its so fun, your cpu will forget to do work- execution is 2-6x "
			+ "slower with this on, beware",
		action="store_true"
	)

	os_group = parser.add_mutually_exclusive_group()
	os_group.add_argument(
		"-u",
		"--unix",
		help="forces unix OS detection",
		action="store_true"
	)
	os_group.add_argument(
		"-w",
		"--windows",
		help="forces windows OS detection",
		action="store_true"
	)
	verboisty_group = parser.add_mutually_exclusive_group()
	verboisty_group.add_argument(
		"-v",
		"--verbose",
		help="intensifies console output. Use more v's for more output. 3+ v's will print *e v e r y t h i n g* .",
		action="count"
	)
	verboisty_group.add_argument(
		"-q",
		"--quiet",
		help="reduces console output. Use more q's for less output. Once I actually implement it, 3+ q's will disable "
			+ "stdout.",
		action="count"
	)
	parser.add_argument(
		"-k",
		"--keyword",
		help="keywords to search for. Put this at the end of your command, and then enter as many keywords as you want.",
		nargs="*"
	)
	parser.add_argument(
		"-ik",
		"--ignore_keyword",
		help="keywords to ignore. Put this at the end of your command, and then enter as many keywords as you want.",
		nargs="*"
	)
	parser.add_argument(
		"-if",
		"--ignore_file",
		help="log files to ignore. Put this at the end of your command, and then enter as many log files as you want.",
		nargs="*"
	)
	return parser.parse_args()


"""
i'm sorry for this
"""


def global_args(arg_space):
	global args
	args = arg_space


"""
<<Main Method>>
"""
afl.init()
if __name__ == "__main__":
	args = parse_arguments()

	vprint(args, 0)
	file_lines = []
	if args.keyword and args.logpath and args.savename:
		file_lines = read_file(args.logpath, args.keyword)  # reading the file
		save_file(file_lines, args.savename)  # saving the file
		sys.exit()
	if args.logpath and args.keyword:
		file_lines = read_file(args.logpath, args.keyword)
	elif args.logpath:
		file_lines = read_file(args.logpath, get_keywords())
	else:
		list_directory()
		file_path = safe_input("Type a file from above, or type a filepath...\n> ")
		keywords = get_keywords()
		automate_command_builder(file_path, keywords)
		file_lines = read_file(file_path, keywords)

	choiceList = ['s', 'v', 'c', 'e']
	choice = ""
	fail = False
	while True:
		if fail is True:
			for letter in choice:
				if letter in choiceList:
					choice = letter
					fail = False
					break
		else:
			choice = safe_input("What do you want to do with these lines?"
								+ "\n(S)ave to file\n(V)iew Logs\n(C)hange search..."
								+ "\n(E)xit\n> ")
		print("'", choice, "'")
		vprint(str(len(file_lines)) + " instances found", 2)
		if choice.lower() == choiceList[0]:
			while True:
				choice = safe_input("Name your file...")
				if choice is not "":
					save_file(file_lines, choice)
					break
				else:
					vprint("File name \"" + choice + "\" not valid.", 2)
		elif choice.lower() == choiceList[1]:
			view_lines(file_lines)
		elif choice.lower() == choiceList[2]:
			file_lines = read_file(safe_input("Type a filepath...\n> "), get_keywords())
			print(len(file_lines), "instances found")
		elif choice.lower() == choiceList[3] or "<Unknown" in choice or choice == "":
			vprint("exiting...", 3)
			# probably fine but should have verification? dont wanna delete user files-
			# but at a certian point, it's kinda their fault for storing files in /tmp...
			# but if this ever somehow gets a wildly wrong directly, that's gonna suck
			if os.path.isdir(tempfile.gettempdir() + "/logParserTemp/"):
				shutil.rmtree(tempfile.gettempdir() + "/logParserTemp/")
			os._exit(0)
		else:
			fail = True


class Parser:
	file_lines = []
	opts = {}
	args = {}

	def __init__(self, **options):
		self.opts = options
		self.update_arguments(self.opts)
		global_args(self.args)

	def easy_read_lines(self):
		self.update_arguments(self.opts)
		self.read_filelines()
		if self.opts["save_path"].get() is not "":
			save_file(self.filelines, self.opts["save_path"].get())

	def update_arguments(self, options, skip_parse_args=False):
		if not skip_parse_args:
			self.args = parse_arguments()
		verbosity = self.opts["verbosity_value"].get()
		if verbosity is not 0:
			if verbosity < 0:
				self.args.quiet = verbosity
			else:
				self.args.verbose = verbosity
		self.args.log_path = self.opts["log_path"].get()
		self.args.ignore_keyword = self.opts["ignored_keyword_list"].get()  # todo: adapt from string to list
		self.args.ignore_file = self.opts["ignored_file_list"].get()  # todo: adapt from string to list
		forced_os = self.opts["force_os_detection"].get()
		if forced_os is not "":
			if forced_os is "u":
				self.args.unix = True
			else:
				self.args.windows = True
		self.args.force = self.opts["force_box"].get()
		self.args.fun = self.opts["fun_box"].get()
		global_args(self.args)
		self.args.save_name = self.opts["save_path"].get()

	def read_filelines(self, also_get_lines=False):
		self.filelines = read_file(self.opts["log_path"].get(), self.opts[
			"keyword_list"].get())  # reading the file  # todo: adapt keywords from string to list
		if also_get_lines:
			return self.get_file_lines()

	def get_file_lines(self):
		return self.filelines
