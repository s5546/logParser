# logParser
im not very good at python pls no bully

Developed on python 3.6.7, using Geany

Uses psutil, you'll have to install it using pip3 (or just use the -f flag, it gets rid of some safety measures but you wont need psutil then)

Uses tkinter for the GUI. Check if you have it installed by running "python -m tkinter"- a window should pop up.

	If you're on Python 3.7.2 or above, it should already be installed. It wasn't for me, but it SHOULD be.

	If you're on linux, search for "python3-tk" in your distro's repos (eg. "sudo apt install python3-tk")
	
	If you're on windows, follow this guide: https://tkdocs.com/tutorial/install.html#installwin
	
	If you're on macOS, follow this guide: https://tkdocs.com/tutorial/install.html#installmac
	
		(note: i have no way to test if that works, sorry)

Attempts to follow PEP8, except for the parts that I don't like and also the parts I forget about

----

switches:

- f: removes some safety precautions and "forces" it to read the file

	Also removes the need for psutil

- w: forces windows style commands even if your OS isnt windows

- u: forces unix style commands even if your OS isnt unix

- x: enables the spinning load thing, making the program at least twice as fun

	it ALSO slows down execution by 2-6x, giving you even more time for the fun

- k: keywords to search through the file for

- l: path to log you want to parse

- s: saves the logs to whatever file you specify

- q: reduces verbosity, varying depending on how many q's you use

	3 q's or more will disable console output, once I get that implemented

- v: intensifies verbosity, varying depending on how many v's you use.
	
	2 v's or more shows debug info
	
- ik: ignores all keywords that match this list

- if: ignores all files matching this list

- d: performs dangerous operations for potentially extra speed. Needs an argument passed to it, sprinkled around the code.

- r: recursively searches when needed. Defaults to 0, for infinite recursion. Specify the recursion depth you want.

- rr: removes redundant lines- eg if "abcd" is in a file twice, only the first time will be printed.

- ll: limits output to XXXX lines before stopping. Must be an integer, and only counts up when a line matches.

----
Known bugs:

- "-l" switch only accepts relative paths, not absolute paths

	Accepts absolute paths when there's an equals between the -l and the path
	
- All files parsed are listed in output, regardless of if they match any keywords

- Depending on how they're made, Zip Bombs can occasionally put the program in an infinite loop of extracting the same few zips

	This is related to how I do the file searching- I always read the alphabetically first file (regardless of how recently it's been extracted, but if i instead appended it to the end it might be easier (or extracted all zips before file reading, idk)

- CLI: typing a null byte anywhere causes program to crash

	this is expected for python- null bytes serve as EOF for python- but should i protect against that?
	
- The read speed seems wildly inconsistent- see logParservsGrep06-05-19.png

	Shows average times over 1250 trials, LP has a std dev. of ~5 but grep is at about 1
	
	On a more recent trial, the min and median beat grep's mid median and mean- but the max almost doubles grep's max, bringing the mean to +8 seconds. Something's volatile in my program?

- verbosity is broken on the gui- both directions appear to make it more verbose

- the list box keeps adding its entries repeatedly
----
Example files included:

- tarzipdir.tar.gz.zip.xz

	has four small logs. From the top down, its a zip containing both [a gzip file, which we currently dont support] and a tar.gz containing both [a txt file] and (a directory containing a zip and a tar.gz, each of which contain a txt file).
	
	Tests recursive compressed files, the tmp directory, corrupted file filtering, and the limits of human comprehension
	
- bomb.zip

	Generated from https://github.com/damianrusinek/zip-bomb
	
	a zip bomb! Generated using "python zip-bomb.py nested 8192000 out.zip"
	
	supposedly uncompresses to 800gb

https://www.secrepo.com/ has some pretty good logs if ya need em

----

todo:

- innovate~~~~

	- Grep's a native linux command and about 2-4x faster than this, so what can this offer?
	
		- I probably can't match it for speed (at least with a single thread), since I'm on python (or is that just an excuse? idk)
		
		- we occasionally beat grep on multiple file searches
		
		- we can search through partially binary files
	
	- ideas (not necessarily practical ones):
		
		- Sorter (a-z, z-a, more?)
		
		- Really drive home that userfriendliness
		
			- Multithreading? Grep is not multithreaded, and while there are ways to use it with multiple threads- they're complicated, and an average end-user won't know how to use them (if they even realize multithreading is a thing)
		
- Protect from zip bombs

	- A fourm post I found suggested checking the size of the tmp folder, and comparing that to the original file- if the ratio of uncompressed:compressed is too high, stop reading.

- some type of analytics?

    - canvas on tkinter
    
    - i might need R for that
    
        - it'll make IST 365 easier for me so eh why not
        
        - though i have no idea how python integration's gonna go for that

config:

- log search history

- options menu

	- (make these settings persistent somehow)
	
	- How to sort the lines?
	
	- How many lines to read at one time?
  
	- options to remove redundant lines of passwords
	
	- make directory searching non-recursive
	
	- make multi-file logs cohesive, instead of split
	
	- stop after XXXXMB parsed
	
- clean up
	
	- nicer exceptions
	
		- eg. say "file name too long truncating to XXXX" instead of crashing with an exception
	
	
- QoL

	- faster reading
	
		- mmem is how I wanna do it, but honestly mmem scares me
	
	- there's probably optimizations everywhere to be made

	- improve the spin loader
		
		- threading, basically
	
Email altmcman@gmail.com if you have suggestions or problems
