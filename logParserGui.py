from tkinter import *
import parser

#button implementation
class ControlApp:
	
	def __init__(self, master):
		frame = Frame(master)
		frame.pack()
		
		#creates two buttons, quit and hello
		self.button = Button(
			frame, text="QUIT", fg="pink", command=frame.quit
			)
		self.button.pack(side=LEFT)
		
		self.parse_button = Button(frame, text="parse", command= lambda: self.parse(self.opt_dict))
		self.parse_button.pack(side=LEFT)
		
		self.opt_dict = {
			"log_path" : StringVar(),
			"save_path" : StringVar(),
			"keyword_list" : StringVar(),
			"ignored_keyword_list" : StringVar(),
			"ignored_file_list" : StringVar(),
			"force_os_detection" : StringVar(),
			"verbosity_value" : IntVar(),
			"fun_box" : BooleanVar(),
			"force_box" : BooleanVar()
		}
		# adding all fields
		# there's gotta be a smarter way to do this, right?
		# cause this feels REALLY gross
		self.log_path = Entry(master, text="enter a log path here...", textvariable=self.opt_dict["log_path"])
		self.save_path = Entry(master, text="enter a save path here..", textvariable=self.opt_dict["save_path"])
		self.keywords = Entry(master, text="enter your keywords here...", textvariable=self.opt_dict["keyword_list"])
		self.ignored_keywords = Entry(master, text="enter your ignored keywords here...", textvariable=self.opt_dict["ignored_keyword_list"])
		self.ignored_files = Entry(master, text="enter your ignored files here...", textvariable=self.opt_dict["ignored_file_list"])
		self.force_unix_detection = Radiobutton(master, text="Unix", variable=self.opt_dict["force_os_detection"], value="u", indicatoron=0)
		self.force_windows_detection = Radiobutton(master, text="Windows", variable=self.opt_dict["force_os_detection"], value="w", indicatoron=0)
		self.fun_box = Checkbutton(master, text="Fun", variable=self.opt_dict["fun_box"])
		self.force_box = Checkbutton(master, text="Force", variable=self.opt_dict["force_box"])
		self.verbosity_slider = Scale(master, from_=3, to=-3, variable=self.opt_dict["verbosity_value"], label="Verbosity")
		self.log_path.pack(side=LEFT)
		self.save_path.pack(side=LEFT)
		self.keywords.pack(side=LEFT)
		self.ignored_keywords.pack(side=LEFT)
		self.ignored_files.pack(side=LEFT)
		self.force_unix_detection.pack(side=LEFT)
		self.force_windows_detection.pack(side=LEFT)
		self.verbosity_slider.pack(side=LEFT)
		self.fun_box.pack(side=LEFT)
		self.force_box.pack(side=LEFT)
				
	def parse(self, vars_dict):
		for line in parser.easyReadLines(vars_dict):
			print(line)
		
	

#root widget
root = Tk()

#label
w = Label(root, text="Hello, world!")
#size window to fix text
w.pack()

#button
app = ControlApp(root)

#show window
root.mainloop()

#explicitly destroys main window
root.destroy()
