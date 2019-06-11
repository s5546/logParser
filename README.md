# logParser
im not very good at python pls no bully

Developed on python 3.6.7, using Geany

Uses psutil, you'll have to install it using pip3 (or just use the -f flag, it gets rid of some safety measures but you wont need psutil then)

Attempts to follow PEP8, except for the parts that I don't like and also the parts I forget about

switches:

-f removes some safety precautions and "forces" it to read the file

	Also removes the need for psutil

-w forces windows style commands even if your OS isnt windows

-u forces unix style commands even if your OS isnt unix

-x enables the spinning load thing, making the program at least twice as fun

	it ALSO slows down execution by 2-6x, giving you even more time for the fun

-k keywords to search through the file for

-l path to log you want to parse

-s saves the logs to whatever file you specify

-q reduces verbosity, varying depending on how many q's you use

	3 q's or more will disable console output, once I get that implemented

-v intensifies verbosity, varying depending on how many v's you use.
	
	2 v's or more shows debug info

----
Known bugs:

- "-l" switch only accepts relative paths, not absolute paths

	Accepts absolute paths when there's an equals between the -l and the path
	
- Some directories are added, regardless of if they have any matches

----

todo:

innovate

	What I have is essentially a very slow version of grep that's a little more user-friendly. I need to add something more...
	
	ideas (not necessarily practical ones):
		
		Sorter (a-z, z-a, more?)
		
		Really drive home that userfriendliness
		
			Multithreading? Grep is not multithreaded, and while there are ways to use it with multiple threads- they're complicated, and an average end-user won't know how to use them (if they even realize multithreading is a thing)
			
		GUI?
		
			Probably hell in python
		
options menu

	(make these settings persistent somehow)

	Where to save to?
	
	How to sort the lines?
	
	How many lines to read at one time?
  
  options to remove redundant lines of passwords
	
	make directory searching non-recursive
	
	make multi-file logs cohesive, instead of split
	
clean up

	why my formatting succ so much pls fix, future me
	
	figure out how to format python code
	
	why all these random variables happening everywhere
	
	
QoL

	line count suffixes
	
	better explanations on the -h screen

	faster reading
	
		mmem is how I wanna do it, but honestly mmem scares me
	
	there's probably optimizations everywhere to be made

	improve the spin loader
		
		threading, basically
		
	add file filtering to readFile()
