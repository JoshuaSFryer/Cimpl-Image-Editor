import sys  # get_image calls exit
import inspect  #currently unused
import time  #used for timer in main loop
from Cimpl import *
import Cimpl  #duplicate import needed to use the inspect module
import filters


#File I/O and Management
open_images = []  #list of all working images
curr_image = None  #you can't work on an image you haven't opened!
					#so this start as a null variable

def open_new_image():
	"""
	None --> None
	Prompts the user to choose an image to add to the list of open images,
	and sets that imate to be the working image
	"""
	try:
		new_image = Image(choose_file())
		open_images.append(new_image)
		global curr_image
		curr_image = new_image
	#gets thrown if the file selection dialog was closed prematurely
	except AttributeError:
		print("Warning: No image was selected")

def close_curr_image(image):
	"""
	Image --> None
	Removes the selected image from memory and selects a new working image
	if needed
	"""
	global curr_image
	global open_images
	if image is curr_image:
		print("You are closing the current image; please select a new one.")
		curr_image = None
		open_images.remove(image)
		if len(open_images) > 0:
			curr_image = select_image()
		else:
			open_new_image()
	else:
		curr_image = None
		open_images.remove(image)

def close_image():
	"""
	None --> None
	Closes an image selected by the user
	"""
	list_open_images()
	index = int(input("Select file by numerical index: "))
	close_curr_image(open_images[index])

def save_image():
	"""
	None --> None
	Saves an image selected by the user, overwriting the source file
	"""
	list_open_images()
	index = int(input("Select file by numerical index: "))
	save(open_images[index])	

def save_image_as():
	"""
	None --> None
	Saves an image selected by the user, allowing them to specify a new
	filename with a file picking dialog
	"""
	if len(open_images) > 0:
		list_open_images()
		index = int(input("Select file by numerical index: "))
		save_as(open_images[index])
	else:
		print("No open images")

def list_open_images():
	"""
	None --> None
	Prints a list of all currently open images
	"""
	id = 0
	if len(open_images) > 0:
		for i in open_images:
			filename = os.path.basename(i.get_filename())
			print(id, filename)
			id += 1
	else:
		print("No open images")

def select_image():
	"""
	None --> None
	Prompts the user to select a new working image from the list
	of currently open images
	"""
	if len(open_images) > 0:
		list_open_images()
		index = int(input("Select file by numerical index: "))
		return open_images[index]
	else:
		print("No open images")

"""
def get_filters():
	#this function is dummied out; it was a potential approach to
	#automatically get all filters in filters.py
	#It is currently unused.
	all_fxns = inspect.getmembers(filters, inspect.isfunction)
	cimpl_fxns = inspect.getmembers(Cimpl, inspect.isfunction)
	filter_fxns = [item for item in all_fxns if item not in cimpl_fxns]

	filter_list = []
	function_list = []
	for item in filter_fxns:
		filter_list.append(item[0])
		function_list.append(item[1])
	return filter_list, function_list
"""

def display_menu(nest_level):
	"""
	String --> None
	Displays a menu of commands to the user; the input string determines
	which menu to call.
	"""
	main_menu_list = [
		"F: File",
		"I: Filter",
		"Q: Quit"
	]

	file_menu_list = [
		"L: Load",
		"S: Save",
		"A: save As", 
		"T: lisT images",
		"P: Pick image",
		"H: sHow image", 
		"C: Close",
		"B: Back"
	]
	filter_menu_list = [
		"C: brightness and Contrast", 
		"A: color Adjustments",
		"S: Sharpen / blur", 
		"T: Transform",
		"B: Back"
	]
	color_menu_list = [
		"C: get Channel",
		"G: Greyscale", 
		"N: Negative", 
		"S: Sepia",
		"W: sWap channels", 
		"B: Back"
	]
	bright_menu_list = [
		"M: Modify brightness",
		"X: eXtreme contrast", 
		"B: Back"
	]
	trans_menu_list = [
		"H: flip Horizontal",
		"V: flip Vertical",
		"B: Back"
	]
	blur_menu_list = [
		"L: bLur",
		"E: detect Edges",
		"B: Back"
	]

	time.sleep(0.35)
	
	if nest_level == "main":
		for element in main_menu_list:
			print(element)
		interpret_command(get_command(), "main")
	elif nest_level == "file":
		for element in file_menu_list:
			print(element)
		interpret_command(get_command(), "file")
	elif nest_level == "filter":
		for element in filter_menu_list:
			print(element)
		interpret_command(get_command(), "filter")
	elif nest_level == "bright":
		for element in bright_menu_list:
			print(element)
		interpret_command(get_command(), "bright")
	elif nest_level == "blur":
		for element in blur_menu_list:
			print(element)
		interpret_command(get_command(), "blur")

def get_command():
	"""
	None --> String
	Returns a string as entered by the user.
	"""
	command = input(">: ").upper()  #sanitize the input
	return command


def interpret_command(command, nest_level):
	"""
	String, String --> None
	Depending on the current menu, executes a command based on user input
	as provided in the "command" parameter
	"""
	global curr_image

	if nest_level == "main":
		#interpret input assuming main menu
		if command == "F":
			display_menu("file")
		elif command == "I":
			if curr_image is not None:
				display_menu("filter")
			else:
				print("Please load an image first")
		elif command == "Q":
			sys.exit()
		else:
			print("Invalid command")


	elif nest_level == "file":
		#interpret input assuming file menu
		if command == "L":
			open_new_image()
		elif command == "S":
			save_image_as()
		elif command == "T":
			list_open_images()
		elif command == "P":
			curr_image = select_image()
		elif command == "C":
			close_image()
		elif command == "H":
			show(select_image())
		elif command == "B":
			return
		else:
			print("Invalid command")


	elif nest_level == "filter":
		#interpret input assuming filter menu
		if command == "C":
			display_menu("bright")
		elif command == "A":
			display_menu("color")
		elif command == "T":
			display_menu("trans")
		elif command == "S":
			display_menu("blur")
		elif command == "B":
			return
		else:
			print("Invalid command")

	elif nest_level == "bright":
		if command == "M":
			print("Brightness scale (%)?")
			while True:  #Sanitize the input
				try:
					filters.modify_brightness(curr_image, int(input(">: ")))
					break
				except ValueError:  #input is a non-integer
					print("Please enter an integer value")
		elif command == "X":
			filters.extreme_contrast(curr_image)
		elif command == "B":
			return
		else:
			print ("Invalid command")

	elif nest_level == "trans":
		if command == "H":
			filters.flip_horizontal(curr_image)
		elif command == "V":
			filters.flip_vertical(curr_image)
		elif command == "B":
			return
		else:
			print ("Invalid command")

	elif nest_level == "blur":
		if command == "L":
			filters.blur(curr_image)
		elif command == "E":
			print("Threshold? Recommended values: ~7-18")
			filters.detect_edges(curr_image, int(input(">: ")))
		elif command == "B":
			return
		else:
			print ("Invalid command")



if __name__ == "__main__":
	"""	
	Primary runtime loop.
	If there are no open images (as is always the case on launch), prompt
	the user to select one and then display the main menu.
	"""
	while(True):
		if len(open_images) < 1:
			open_new_image()

		display_menu("main")

