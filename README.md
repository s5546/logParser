# logParser
im not very good at python pls no bully

Developed on python 3.6.7, using Geany

Uses psutil, you'll have to install it using pip3 (or just use the -f flag, it gets rid of some safety measures but you wont need psutil then)

Attempts to follow PEP8

switches:

-f removes some safety precautions and "forces" it to read the file

	Also removes the need for psutil

-w forces windows style commands even if your OS isnt windows

-u forces unix style commands even if your OS isnt unix

-x starts the fun by enabling the spinning loader

	it's also 2-6x slower with the spinner on

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

revolutionary new idea: no individual file searching

	just use grep if you want that (or find-str if you're on windows)

innovate

	What I have is essentially a very slow version of grep that's a little more user-friendly. I need to add something more...
	
	ideas (not necessarily practical ones):
		
		Sorter (a-z, z-a, more?)
		
		Really drive home that userfriendliness
		
			Multithreading? Grep is not multithreaded, and while there are ways to use it with multiple threads- they're complicated, and an average end-user won't know how to use them (if they even realize multithreading is a thing)
			
				Maybe not TOO hard? If I can get the line count (of the file) and core count (of the cpu), maybe I could (somewhat) evenly distribute work like that? 
			
		Some sort of compression support?
		
			Native reading from tar.gz files (would be very useful on windows)
			
		GUI?
		
			Probably hell in python
		
options menu

	(make these settings persistent somehow)

	Where to save to?
	
	How to sort the lines?
	
	How many lines to read at one time?
	
clean up

	why my formatting succ so much pls fix, future me
	
	figure out how to format python code
	
	why all these random variables happening everywhere
	
	more comments pls
	
	
QoL

	line count suffixes
	
	better explanations on the -h screen
	
	there's probably optimizations everywhere to be made

	improve the spin loader
		
		threading, basically
