from tkinter import *
from tkinter import filedialog
from analyzer import Analyzer  # work on your naming scheme bruh


class ControlApp:

	def __init__(self, master):

		self.opt_dict = {
			"log_path": StringVar(),
			"save_path": StringVar(),
			"keyword_list": StringVar(),
			"ignored_keyword_list": StringVar(),
			"ignored_file_list": StringVar(),
			"force_os_detection": StringVar(),
			"verbosity_value": IntVar(),
			"fun_box": BooleanVar(),
			"force_box": BooleanVar(),
			"return_value": BooleanVar(),
			"line_sorting": IntVar(),
			"line_limit": IntVar(),
			"remove_redundant": BooleanVar(),
			"recursion": IntVar()
		}
		# group creation
		self.operation_group = LabelFrame(
			master,
			text="Operations"
		)
		self.text_group = LabelFrame(
			master,
			text="Search options"
		)
		self.option_group = LabelFrame(
			master,
			text="Misc options"
		)

		# operation group
		self.quit_button = Button(
			self.operation_group,
			text="QUIT",
			command=master.quit
		)
		self.parse_button = Button(
			self.operation_group,
			text="parse",
			command=lambda: self.parse(self.opt_dict)
		)
		self.option_button = Button(
			self.operation_group,
			text="Options...",
			command=lambda: self.option_menu()
		)

		# text group
		self.log_label = Label(
			self.text_group,
			text="Log path:"
		)
		self.log_path = Entry(
			self.text_group,
			text="enter a log path here...",
			textvariable=self.opt_dict["log_path"]
		)
		self.log_browse = Button(
			self.text_group,
			text="Browse for file(s)...",
			command=lambda: self.browse("log_path")
		)
		self.save_label = Label(
			self.text_group,
			text="Save path:"
		)
		self.save_path = Entry(
			self.text_group,
			text="enter a save path here..",
			textvariable=self.opt_dict["save_path"]
		)
		self.save_browse = Button(
			self.text_group,
			text="Browse for save...",
			command=lambda: self.browse("save_path")
		)
		self.keywords_label = Label(
			self.text_group,
			text="Keywords:"
		)
		self.keywords = Entry(
			self.text_group,
			text="enter your keywords here...",
			textvariable=self.opt_dict["keyword_list"]
		)
		self.ignored_keywords_label = Label(
			self.text_group,
			text="Ignored keywords:"
			)
		self.ignored_keywords = Entry(
			self.text_group,
			text="enter your ignored keywords here...",
			textvariable=self.opt_dict["ignored_keyword_list"]
		)
		self.ignored_files_label = Label(
			self.text_group,
			text="Ignored files:"
		)
		self.ignored_files = Entry(
			self.text_group,
			text="enter your ignored files here...",
			textvariable=self.opt_dict["ignored_file_list"]
		)

		# option group

		# group grid section
		self.text_group.grid(row=0, column=0)
		self.operation_group.grid(row=1, column=0)

		# text grid section
		self.log_label.grid(row=0, column=0)
		self.log_path.grid(row=0, column=1)
		self.log_browse.grid(row=0, column=2)
		self.save_label.grid(row=1, column=0)
		self.save_path.grid(row=1, column=1)
		self.save_browse.grid(row=1, column=2)
		self.keywords_label.grid(row=2, column=0)
		self.keywords.grid(row=2, column=1)
		self.ignored_keywords_label.grid(row=3, column=0)
		self.ignored_keywords.grid(row=3, column=1)
		self.ignored_files_label.grid(row=4, column=0)
		self.ignored_files.grid(row=4, column=1)

		# operation pack section
		self.parse_button.pack(side=LEFT)
		self.option_button.pack()
		self.quit_button.pack(side=RIGHT)

	"""
	"""
	@staticmethod
	def parse(vars_dict):
		win = Toplevel()
		log_parser = Analyzer(**vars_dict)
		text_frame = LabelFrame(win, text="Output")
		text_frame.pack(fill=BOTH, expand=1)
		scrollbar_text_box = Scrollbar(text_frame)
		scrollbar_text_box.pack(side=RIGHT, fill=Y)
		text_box = Text(text_frame, wrap=WORD, borderwidth=3, yscrollcommand=scrollbar_text_box.set)
		close_button = Button(win, text='OK', command=win.destroy)
		scrollbar_text_box.pack()
		scrollbar_text_box.config(command=text_box.yview)
		text_box.pack(fill=BOTH, expand=1)
		close_button.pack()
		try:
			log_parser.easy_read_lines()
			file_lines = log_parser.get_file_lines()
			for line in file_lines:
				text_box.insert(END, line)
		except TypeError as e:
			print(e)
			text_box.insert(END, "TYPEERROR: Can't read file, it might not exist")

	"""
	"""
	def browse(self, dict_target=None):
		if dict_target is "log_path":
			self.opt_dict[dict_target].set(filedialog.askopenfilename())
		elif dict_target is "save_path":
			self.opt_dict[dict_target].set(filedialog.asksaveasfilename())
		elif dict_target is None:
			return filedialog.askopenfilename()
		else:
			print("Error: dict_target invalid")

	def option_menu(self):
		win = Toplevel()
		Button(
			win,
			text='OK',
			command=win.destroy
		).pack()
		sort_list = Listbox(
			win,
			listvariable=self.opt_dict["line_sorting"]
		)
		recursive_label = Label(
			win,
			text="Recursion depth (0=∞)"
		)
		recursive_value = Entry(
			win,
			text="Recursion",
			textvariable=self.opt_dict["recursion"]
		)
		limit_label = Label(
			win,
			text="Line Limit"
		)
		limit_value = Entry(
			win,
			textvariable=self.opt_dict["line_limit"]
		)

		force_unix_detection = Radiobutton(
			win,
			text="Unix",
			variable=self.opt_dict["force_os_detection"],
			value="u",
			indicatoron=0
		)
		force_windows_detection = Radiobutton(
			win,
			text="Windows",
			indicatoron=0,
			value="w",
			variable=self.opt_dict["force_os_detection"]
		)
		fun_box = Checkbutton(win, text="Fun", variable=self.opt_dict["fun_box"])
		force_box = Checkbutton(win, text="Force", variable=self.opt_dict["force_box"])
		return_box = Checkbutton(win, text="Return", variable=self.opt_dict["return_value"])
		verbosity_slider = Scale(win, from_=3, to=-3, variable=self.opt_dict["verbosity_value"], label="Verbosity")
		redundant_box = Checkbutton(win, text="Remove Redundant", variable=self.opt_dict["remove_redundant"])

		verbosity_slider.pack()
		force_unix_detection.pack()
		force_windows_detection.pack()
		sort_list.pack()
		limit_label.pack()
		limit_value.pack()
		recursive_label.pack()
		recursive_value.pack()
		fun_box.pack()
		force_box.pack()
		return_box.pack()
		redundant_box.pack()
		for item in ["A-Z (Default)", "Z-A"]:
			sort_list.insert(END, item)


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
