#!/usr/bin/env python3
# **************************************************************
# File      : dft.py
# Version   : 1.14
# Purpose   : calculate distance, speed or time at sea (Distans Fart Tid)
# Linked to : dft_functions.py
#
# Created by: Urban Björkén
# Date      : 2026-10-13
# email     : vyten@starnet.nu
# **************************************************************

# ** Imports ***************************************************
import subprocess
import logging
import sys
from os import path
# the root directory of the repo, so that common/ can be found
sys.path.insert(0, path.join(path.dirname(path.abspath(__file__)), '..'))
import dft_functions
import lang_se
import lang_en
import lang_cz
from common.terminal_colors import COL_YELLOW_BLUE, COL_YELLOW_RED, COL_GREEN, COL_STANDARD

# ** Variables *************************************************
LOG_FILE_NAME = 'dft.log'
LOG_FILE = path.join(path.dirname(path.abspath(__file__)), LOG_FILE_NAME)

# the chosen language is saved here until next time, like the cookie in the PHP version
LANG_FILE_NAME = 'dft_lang.txt'
LANG_FILE = path.join(path.dirname(path.abspath(__file__)), LANG_FILE_NAME)

# the languages to choose from, the number is the choice in the menu
LANGUAGES = {
	'1': lang_se.TEXTS,
	'2': lang_en.TEXTS,
	'3': lang_cz.TEXTS,
}

# ** Functions *************************************************
# ask_number() - asks until the user writes a number that is 0 or more, the check is in dft_functions.to_number()
def ask_number(question, texts):
	while True:
		user_input_value = input(question)
		number, error = dft_functions.to_number(user_input_value)
		if error:
			logging.error(f"ask_number: '{user_input_value}' {error}")
			print(f"{COL_YELLOW_RED} {texts[error]} {COL_STANDARD}")
			continue

		return number


# ask_time() - asks for hours and minutes, returns two values
def ask_time(texts):
	hours = ask_number(texts['ask_hours'], texts)
	minutes = ask_number(texts['ask_minutes'], texts)
	return hours, minutes


# load_language() - returns the saved language number, or None if no language is saved
def load_language():
	try:
		with open(LANG_FILE) as lang_file:
			choice = lang_file.read().strip()
	except FileNotFoundError:
		return None
	except OSError as error:
		logging.error(f"load_language: {error}")
		return None

	if choice in LANGUAGES:
		return choice

	logging.error(f"load_language: '{choice}' in {LANG_FILE_NAME} is not a language")
	return None


# save_language() - saves the language number until next time
def save_language(choice):
	try:
		with open(LANG_FILE, 'w') as lang_file:
			lang_file.write(choice)
	except OSError as error:
		logging.error(f"save_language: {error}")


# choose_language() - asks until the user chooses a language, saves it and returns the texts for it
# current_choice is shown as [2], Enter alone keeps it, None when no language is chosen yet
def choose_language(current_choice):
	# clear linux screen
	subprocess.run(['clear'])

	print()
	print(f"{COL_YELLOW_BLUE}   D F T   {COL_STANDARD}")
	print()
	for number, texts in LANGUAGES.items():
		print(f"  {number} = {texts['language']}")

	prompt = f"[{current_choice}] > " if current_choice else "> "
	while True:
		choice = input(prompt)
		if choice == "" and current_choice:
			choice = current_choice
		if choice in LANGUAGES:
			save_language(choice)
			return choice

		logging.error(f"choose_language: '{choice}' is not a language")
		print(f"{COL_YELLOW_RED} {' / '.join(LANGUAGES)} {COL_STANDARD}")


# show_title() - clears the screen and shows the title in the chosen language
def show_title(texts):
	# clear linux screen
	subprocess.run(['clear'])

	print()
	print(f"{COL_YELLOW_BLUE}   {texts['title']}   {COL_STANDARD}")


# main() - the flow of the script
# the language from last time is used directly, the language menu is shown only the first time
# Ctrl+C or Ctrl+D ends the script quietly instead of showing a Python error
def main():
	# Swedish until a language is chosen, used if Ctrl+C comes before that
	texts = lang_se.TEXTS
	try:
		language_choice = load_language()
		if language_choice is None:
			language_choice = choose_language(None)
		texts = LANGUAGES[language_choice]
		show_title(texts)

		while True:
			print()
			print(texts['menu_question'])
			print(f"  1 = {texts['distance']}")
			print(f"  2 = {texts['speed']}")
			print(f"  3 = {texts['time']}")
			print(f"  4 = {texts['change_language']}")
			print(f"  0 = {texts['quit']}")
			choice = input(texts['choice'])

			if choice == "1":
				speed = ask_number(texts['ask_speed'], texts)
				hours, minutes = ask_time(texts)
				distance = dft_functions.calculate_distance(speed, hours, minutes)
				print(f"{COL_GREEN}{texts['result_distance'].format(distance=distance)}{COL_STANDARD}")

			elif choice == "2":
				distance = ask_number(texts['ask_distance'], texts)
				hours, minutes = ask_time(texts)
				if dft_functions.to_minutes(hours, minutes) == 0:
					logging.error("main: speed asked with time 0")
					print(f"{COL_YELLOW_RED} {texts['error_time_zero']} {COL_STANDARD}")
					continue
				speed = dft_functions.calculate_speed(distance, hours, minutes)
				print(f"{COL_GREEN}{texts['result_speed'].format(speed=speed)}{COL_STANDARD}")

			elif choice == "3":
				distance = ask_number(texts['ask_distance'], texts)
				speed = ask_number(texts['ask_speed'], texts)
				if speed == 0:
					logging.error("main: time asked with speed 0")
					print(f"{COL_YELLOW_RED} {texts['error_speed_zero']} {COL_STANDARD}")
					continue
				hours, minutes = dft_functions.calculate_time(distance, speed)
				print(f"{COL_GREEN}{texts['result_time'].format(hours=hours, minutes=minutes)}{COL_STANDARD}")

			elif choice == "4":
				language_choice = choose_language(language_choice)
				texts = LANGUAGES[language_choice]
				show_title(texts)

			elif choice == "0":
				print(texts['goodbye'])
				break

			else:
				print(f"{COL_YELLOW_RED} {texts['error_menu']} {COL_STANDARD}")

	except (KeyboardInterrupt, EOFError):
		print()
		print(texts['goodbye'])


# ** Main ******************************************************
# run main() only when the script is started, not when it is imported
if __name__ == "__main__":
	# logging
	logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', filename=LOG_FILE, level=logging.ERROR)

	main()

# ** History ***************************************************
# 1.0 2026-10-13 Initial version
# 1.1 2026-10-13 menu, input and output
# 1.2 2026-10-13 clear screen at start
# 1.3 2026-10-13 subprocess.run() instead of os.system()
# 1.4 2026-10-13 logging to dft.log, Ctrl+C and Ctrl+D end the script quietly
# 1.5 2026-10-14 constants in upper case
# 1.6 2026-10-14 colors (terminal_colors.py)
# 1.7 2026-10-14 answers in green
# 1.8 2026-10-14 texts from lang_se.py
# 1.9 2026-10-14 choose language at start: Swedish, English or Czech
# 1.10 2026-10-14 remember the language until next time in dft_lang.txt
# 1.11 2026-10-14 saved language is used directly, 4 in the menu changes language
# 1.12 2026-10-14 nan and inf are not accepted as numbers
# 1.13 2026-10-14 terminal_colors from common/
# 1.14 2026-10-20 the check of numbers moved to dft_functions.to_number()

# ** END SCRIPT ************************************************
