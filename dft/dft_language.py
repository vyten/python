#!/usr/bin/env python3
# **************************************************************
# File      : dft_language.py
# Version   : 1.0
# Purpose   : the languages and the saved language, used by both dft.py and dft_gui.py
# Linked to : dft.py, dft_gui.py, lang_se.py, lang_en.py, lang_cz.py
#
# Created by: Urban Björkén
# Date      : 2026-10-20
# email     : vyten@starnet.nu
# **************************************************************

# ** Imports ***************************************************
import logging
from os import path
import lang_se
import lang_en
import lang_cz

# ** Variables *************************************************
# the chosen language is saved here until next time, like the cookie in the PHP version
LANG_FILE_NAME = 'dft_lang.txt'
LANG_FILE = path.join(path.dirname(path.abspath(__file__)), LANG_FILE_NAME)

# the languages to choose from, the number is the choice in the menu and what is saved in the file
LANGUAGES = {
	'1': lang_se.TEXTS,
	'2': lang_en.TEXTS,
	'3': lang_cz.TEXTS,
}

# ** Functions *************************************************
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


# ** Main ******************************************************
# show the languages and the saved language, runs only when this file is started directly
if __name__ == "__main__":
	for number, texts in LANGUAGES.items():
		print(f"{number} = {texts['language']}")
	print(f"saved in {LANG_FILE_NAME}: {load_language()}")

# ** History ***************************************************
# 1.0 2026-10-20 Initial version, moved from dft.py

# ** END SCRIPT ************************************************
