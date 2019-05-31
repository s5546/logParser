# logParser
im not very good at python pls no bully

Developed on python 3.6.7, using Geany

Uses psutil, you'll have to install it using pip3 (or just use the -f flag, it gets rid of some safety measures but you wont need psutil then)

switches:

-f removes some safety precautions and "forces" it to read the file

-w forces windows style commands even if your OS isnt windows

-l forces linux style commands even if your OS isnt linux

-x disables the spinny load thing, but why would you want to do that?

	i put literally minutes into coding that and you're just gonna break my heart like that? </3




todo:

make it cli friendly- pass some parameters in yaknow

	-q quiet
	
	-k keyword file OR string
	
	-p log path
	
	-s save file to xxxx.txt
	
	-d debug strings (show variables, execution times, etc)

	
options for searched data

	save to file

	automatically show lines- as many as the current terminal size can handle
	
	
clean up

	why my formatting succ so much pls fix, future me
	
	figure out how to format python code
	
	why so many unneeded debug statements
	
	
where the comments at

	get me those comments
	
	
QoL

	dont have so many exceptions
	
	there's probably optimizations everywhere to be made
	
		eg. lots of lists used towards the end when we could probably just reuse 1/2 of em
