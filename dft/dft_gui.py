#!/usr/bin/env python3
# **************************************************************
# File      : dft_gui.py
# Version   : 1.7
# Purpose   : calculate distance, speed or time at sea (Distans Fart Tid) in a window
# Linked to : dft_functions.py, dft.py, lang_se.py, lang_en.py, lang_cz.py
#
# Created by: Urban Björkén
# Date      : 2026-10-14
# email     : vyten@starnet.nu
# **************************************************************

# ** Imports ***************************************************
import tkinter as tk
import logging
from os import path
import dft_functions
import dft    # LANGUAGES, load_language() and save_language(), the same saved language as in the terminal

# ** Variables *************************************************
WINDOW_TITLE = 'D F T'    # until a language is chosen, then the title from the language file
WINDOW_SIZE = '400x450'    # width x height in pixels
IMAGE_DIR = path.join(path.dirname(path.abspath(__file__)), 'img')

# the same log file as dft.py
LOG_FILE_NAME = 'dft.log'
LOG_FILE = path.join(path.dirname(path.abspath(__file__)), LOG_FILE_NAME)

# colors from the PHP version (w3.css)
COL_BACKGROUND = '#616161'    # dark gray, the page
COL_BUTTON = '#607d8b'        # blue gray, choice buttons
COL_HOVER = '#2196F3'         # blue, button under the mouse pointer
COL_CALCULATE = '#4CAF50'     # green, the calculate button
COL_BACK = '#ff5722'          # deep orange, back and quit
COL_TEXT = '#ffffff'          # white
COL_ANSWER = '#ffeb3b'        # yellow, the answer
COL_INPUT = '#bbbbbb'         # gray, input fields
COL_ERROR = '#f44336'         # red, error message and the field that is wrong

FONT_HEADER = ('Helvetica', 18, 'bold')
FONT_TEXT = ('Helvetica', 12)

# the flags, the number is the same as in dft.LANGUAGES and dft_lang.txt
FLAGS = {
	'1': 'flag_nation_se.png',
	'2': 'flag_nation_en.png',
	'3': 'flag_nation_cz.png',
}

# the fields on each calculation page: (text, unit), in the same order as calculate() reads them
# the values are keys in the language files, None means no text
CALCULATIONS = {
	'distance': [('speed', 'unit_speed'), ('time', 'unit_hours'), (None, 'unit_minutes')],
	'speed': [('distance', 'unit_distance'), ('time', 'unit_hours'), (None, 'unit_minutes')],
	'time': [('distance', 'unit_distance'), ('speed', 'unit_speed')],
}

# the images must be kept in a variable, otherwise Python throws them away and the buttons become empty
flag_images = {}
small_flag_images = {}

# ** Functions *************************************************
# load_images() - loads the flags, can only be done after tk.Tk() has been created
def load_images():
	for number, file_name in FLAGS.items():
		flag_images[number] = tk.PhotoImage(file=path.join(IMAGE_DIR, file_name))
		small_flag_images[number] = flag_images[number].subsample(2)    # every second pixel, 32 x 32


# set_language() - saves the language until next time, sets the window title and returns the texts
def set_language(window, number):
	dft.save_language(number)
	texts = dft.LANGUAGES[number]
	window.title(texts['title'])
	return texts


# clear_page() - removes everything in the window before a new page is shown
def clear_page(window):
	for widget in window.winfo_children():
		widget.destroy()


# make_button() - a button with the colors from the PHP version
def make_button(parent, text, color, command):
	return tk.Button(parent, text=text, command=command, font=FONT_TEXT, width=15,
		bg=color, fg=COL_TEXT, activebackground=COL_HOVER, activeforeground=COL_TEXT,
		relief='flat', cursor='hand2')


# show_answer() - the answer in yellow on the page background
def show_answer(result_label, text):
	result_label.config(text=text, fg=COL_ANSWER, bg=COL_BACKGROUND)


# show_error() - the error in yellow on red, the wrong field turns red and gets the cursor
def show_error(result_label, text, entry):
	result_label.config(text=f" {text} ", fg=COL_ANSWER, bg=COL_ERROR)
	entry.config(bg=COL_ERROR)
	entry.focus_set()


# read_number() - returns the number in the field, or None and shows the error
# the check is in dft_functions.to_number(), the same as in dft.py
def read_number(entry, result_label, texts):
	user_input_value = entry.get()
	number, error = dft_functions.to_number(user_input_value)
	if error:
		logging.error(f"read_number: '{user_input_value}' {error}")
		show_error(result_label, texts[error], entry)
		return None

	return number


# calculate() - reads the fields, calculates and shows the answer or an error
def calculate(calculation, entries, result_label, texts):
	# all fields back to gray, a field that was wrong last time may be right now
	for entry in entries:
		entry.config(bg=COL_INPUT)

	# stop at the first field that is wrong
	values = []
	for entry in entries:
		number = read_number(entry, result_label, texts)
		if number is None:
			return
		values.append(number)

	if calculation == 'distance':
		speed, hours, minutes = values
		distance = dft_functions.calculate_distance(speed, hours, minutes)
		show_answer(result_label, texts['result_distance'].format(distance=distance))

	elif calculation == 'speed':
		distance, hours, minutes = values
		if dft_functions.to_minutes(hours, minutes) == 0:
			logging.error("calculate: speed asked with time 0")
			show_error(result_label, texts['error_time_zero'], entries[1])
			return
		speed = dft_functions.calculate_speed(distance, hours, minutes)
		show_answer(result_label, texts['result_speed'].format(speed=speed))

	else:
		distance, speed = values
		if speed == 0:
			logging.error("calculate: time asked with speed 0")
			show_error(result_label, texts['error_speed_zero'], entries[1])
			return
		hours, minutes = dft_functions.calculate_time(distance, speed)
		show_answer(result_label, texts['result_time'].format(hours=hours, minutes=minutes))


# show_header() - the header at the top of each page
def show_header(window, text):
	tk.Label(window, text=text, font=FONT_HEADER, bg=COL_BACKGROUND, fg=COL_TEXT).pack(pady=15)


# show_flag_page() - page 1, choose language with the flags, shown only the first time
# number=number is needed, otherwise all three buttons get the last number in the loop
def show_flag_page(window):
	clear_page(window)
	show_header(window, ' ')
	for number in FLAGS:
		tk.Button(window, image=flag_images[number], bg=COL_BUTTON, activebackground=COL_HOVER,
			relief='flat', cursor='hand2',
			command=lambda number=number: show_start_page(window, set_language(window, number))).pack(pady=10)


# show_start_page() - page 2, choose what to calculate
def show_start_page(window, texts):
	clear_page(window)
	show_header(window, texts['calculate_your'])
	for calculation in CALCULATIONS:
		make_button(window, texts[calculation], COL_BUTTON,
			lambda calculation=calculation: show_calculate_page(window, calculation, texts)).pack(pady=10)
	make_button(window, texts['quit'], COL_BACK, window.destroy).pack(pady=30)


# show_calculate_page() - page 3, the fields for the chosen calculation
# values is what was written in the fields before a change of language, None for empty fields
def show_calculate_page(window, calculation, texts, values=None):
	clear_page(window)
	fields = CALCULATIONS[calculation]
	show_header(window, texts[calculation])

	# the answer is shown here, empty until something is calculated
	result_label = tk.Label(window, text='', font=FONT_TEXT, bg=COL_BACKGROUND, fg=COL_ANSWER)
	result_label.pack()

	# the fields in a grid: text, field and unit on each row
	form = tk.Frame(window, bg=COL_BACKGROUND)
	form.pack(pady=10)
	entries = []    # the fields are saved here so that calculate() can read them
	for row, (text_key, unit_key) in enumerate(fields):
		text = texts[text_key] if text_key else ''
		unit = texts[unit_key]
		tk.Label(form, text=text, font=FONT_TEXT, bg=COL_BACKGROUND, fg=COL_TEXT).grid(row=row, column=0, sticky='e', padx=5, pady=5)
		entry = tk.Entry(form, width=6, font=FONT_TEXT, bg=COL_INPUT)
		entry.grid(row=row, column=1, padx=5, pady=5)
		if values:
			entry.insert(0, values[row])
		entries.append(entry)
		tk.Label(form, text=unit, font=FONT_TEXT, bg=COL_BACKGROUND, fg=COL_TEXT).grid(row=row, column=2, sticky='w', padx=5, pady=5)

	# the cursor starts in the first field, like setFocus() in the PHP version
	entries[0].focus_set()

	make_button(window, texts['calculate'], COL_CALCULATE,
		lambda: calculate(calculation, entries, result_label, texts)).pack(pady=10)
	make_button(window, f"« {texts['back']}", COL_BACK, lambda: show_start_page(window, texts)).pack(pady=10)

	# small flags to change language, the same page is shown again in the new language with the same values
	flag_row = tk.Frame(window, bg=COL_BACKGROUND)
	flag_row.pack(pady=10)
	for number in FLAGS:
		tk.Button(flag_row, image=small_flag_images[number], bg=COL_BACKGROUND, activebackground=COL_HOVER,
			relief='flat', cursor='hand2', bd=0,
			command=lambda number=number: show_calculate_page(window, calculation, set_language(window, number),
				[entry.get() for entry in entries])).pack(side='left', padx=5)


# main() - creates the window, shows the first page and waits for the user
# the flags are shown the first time, after that the start page in the saved language
def main():
	window = tk.Tk()
	window.title(WINDOW_TITLE)
	window.geometry(WINDOW_SIZE)
	window.configure(bg=COL_BACKGROUND)

	load_images()
	number = dft.load_language()
	if number is None:
		show_flag_page(window)
	else:
		show_start_page(window, set_language(window, number))

	# mainloop() shows the window and runs until it is closed
	window.mainloop()


# ** Main ******************************************************
# run main() only when the script is started, not when it is imported
if __name__ == "__main__":
	# logging
	logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', filename=LOG_FILE, level=logging.ERROR)

	main()

# ** History ***************************************************
# 1.0 2026-10-14 Initial version, empty window
# 1.1 2026-10-14 controls: radio buttons, input fields, button and result, no function yet
# 1.2 2026-10-14 three pages like the PHP version: flags, start page and calculation page
# 1.3 2026-10-14 the calculate button calculates with dft_functions.py
# 1.4 2026-10-14 wrong input and 0 give an error in yellow on red, logging to dft.log
# 1.5 2026-10-20 texts from the language files, the language is saved in dft_lang.txt like dft.py
# 1.6 2026-10-20 the values in the fields are kept when the language is changed
# 1.7 2026-10-20 the check of numbers from dft_functions.to_number()

# ** END SCRIPT ************************************************
