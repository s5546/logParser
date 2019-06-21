from tkinter import *
from tkinter import filedialog
from parser import Parser # work on your naming scheme bruh

#button implementation
class ControlApp:
	
	def __init__(self, master):
		
		self.opt_dict = {
			"log_path" : StringVar(),
			"save_path" : StringVar(),
			"keyword_list" : StringVar(),
			"ignored_keyword_list" : StringVar(),
			"ignored_file_list" : StringVar(),
			"force_os_detection" : StringVar(),
			"verbosity_value" : IntVar(),
			"fun_box" : BooleanVar(),
			"force_box" : BooleanVar(),
			"return_value" : BooleanVar()
		}
		# group creation
		self.operation_group = LabelFrame(master, text="Operations")
		self.text_group = LabelFrame(master, text="Search options")
		self.option_group = LabelFrame(master, text="Misc options")
		# todo: self.output_group

		# operation group
		self.quit_button = Button(self.operation_group, text="QUIT", fg="pink", command=master.quit)
		self.parse_button = Button(self.operation_group, text="parse", command=lambda: self.parse(self.opt_dict))

		# text group
		self.log_label = Label(self.text_group, text="Log path:")
		self.log_path = Entry(self.text_group, text="enter a log path here...", textvariable=self.opt_dict["log_path"])
		self.log_browse = Button(self.text_group, text="Browse for file(s)...", command = lambda: self.browse("log_path"))
		self.save_label = Label(self.text_group, text="Save path:")
		self.save_path = Entry(self.text_group, text="enter a save path here..", textvariable=self.opt_dict["save_path"])
		self.keywords_label = Label(self.text_group, text="Keywords:")
		self.keywords = Entry(self.text_group, text="enter your keywords here...", textvariable=self.opt_dict["keyword_list"])
		self.ignored_keywords_label = Label(self.text_group, text="Ignored keywords:")
		self.ignored_keywords = Entry(self.text_group, text="enter your ignored keywords here...", textvariable=self.opt_dict["ignored_keyword_list"])
		self.ignored_files_label = Label(self.text_group, text="Ignored files:")
		self.ignored_files = Entry(self.text_group, text="enter your ignored files here...", textvariable=self.opt_dict["ignored_file_list"])

		# option group
		self.force_unix_detection = Radiobutton(self.option_group, text="Unix", variable=self.opt_dict["force_os_detection"], value="u", indicatoron=0)
		self.force_windows_detection = Radiobutton(self.option_group, text="Windows", variable=self.opt_dict["force_os_detection"], value="w", indicatoron=0)
		self.fun_box = Checkbutton(self.option_group, text="Fun", variable=self.opt_dict["fun_box"])
		self.force_box = Checkbutton(self.option_group, text="Force", variable=self.opt_dict["force_box"])
		self.return_box = Checkbutton(self.option_group, text="Return", variable=self.opt_dict["return_value"])
		self.verbosity_slider = Scale(self.option_group, from_=3, to=-3, variable=self.opt_dict["verbosity_value"], label="Verbosity")

		# text grid section
		self.text_group.grid(row=0, column=0)
		self.option_group.grid(row=0, column=1)
		self.operation_group.grid(row=0, column=2)
		self.log_label.grid(row=0, column=0)
		self.log_path.grid(row=0, column=1)
		self.log_browse.grid(row=0, column=2)
		self.save_label.grid(row=1, column=0)
		self.save_path.grid(row=1, column=1)
		self.keywords_label.grid(row=2, column=0)
		self.keywords.grid(row=2, column=1)
		self.ignored_keywords_label.grid(row=3, column=0)
		self.ignored_keywords.grid(row=3, column=1)
		self.ignored_files_label.grid(row=4, column=0)
		self.ignored_files.grid(row=4, column=1)

		# option pack section
		self.force_unix_detection.pack(side=LEFT)
		self.force_windows_detection.pack(side=LEFT)
		self.verbosity_slider.pack(side=LEFT)
		self.fun_box.pack(side=LEFT)
		self.force_box.pack(side=LEFT)
		self.return_box.pack(side=LEFT)

		# operation pack section
		self.quit_button.pack(side=RIGHT)
		self.parse_button.pack(side=LEFT)
	"""
	"""
	@staticmethod
	def parse(vars_dict):
		log_parser = Parser(**vars_dict)
		log_parser.easy_read_lines()
		for line in log_parser.get_file_lines():
			print(line)

	"""
	"""
	def browse(self, dict_target=None):
		if dict_target is "log_path":
			self.opt_dict[dict_target].set(filedialog.askdirectory())
		elif dict_target is "save_path":
			self.opt_dict[dict_target].set(filedialog.asksaveasfilename())
		elif dict_target is None:
			return filedialog.askopenfilename()
		else:
			print("Error: dict_target invalid")


# root widget
root = Tk()

# control panel
app = ControlApp(root)

# show window
root.mainloop()

# explicitly destroys main window
try:
	# if you close without using the quit button this fails
	root.destroy()
except TclError:
	# no need to do anything, program already closing
	pass
