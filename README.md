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

-x disables the spinny load thing, but why would you want to do that?

	i put literally minutes into coding that and you're just gonna break my heart like that? </3

-k keywords to search through the file for

-l path to log you want to parse

-s saves the logs to whatever file you specify

-q reduces verbosity, varying depending on how many q's you use

	3 q's or more will disable console output, once I get that implemented

-v intensifies verbosity, varying depending on how many v's you use.
	
	2 v's or more shows debug info



----

todo:

make it cli friendly- pass some parameters in yaknow
	
	-c continous scanning
	
	
clean up

	why my formatting succ so much pls fix, future me
	
	figure out how to format python code
	
	why all these random variables happening everywhere
	
	more comments pls
	
	
QoL

	dont have so many exceptions
	
	there's probably optimizations everywhere to be made

	improve the spin loader
		
		threading, basically
