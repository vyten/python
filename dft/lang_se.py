#!/usr/bin/env python3
# **************************************************************
# File      : lang_se.py
# Version   : 1.3
# Purpose   : Swedish texts for dft.py and dft_gui.py
# Linked to : dft.py, dft_gui.py
#
# Created by: Urban Björkén
# Date      : 2026-10-14
# email     : vyten@starnet.nu
# **************************************************************

# ** Imports ***************************************************


# ** Variables *************************************************
# {name} is replaced with a value when the text is printed, :.1f means one decimal
TEXTS = {
	# title, menu and general
	'language': 'Svenska',
	'title': 'D F T - Distans Fart Tid',
	'menu_question': 'Vad vill du räkna ut?',
	'distance': 'Distans',
	'speed': 'Fart',
	'time': 'Tid',
	'quit': 'Avsluta',
	'change_language': 'Byt språk',
	'choice': 'Val: ',
	'goodbye': 'Hej då!',

	# questions
	'ask_distance': 'Distans, nm: ',
	'ask_speed': 'Fart, knop: ',
	'ask_hours': 'Tid, timmar: ',
	'ask_minutes': 'Tid, minuter: ',

	# answers
	'result_distance': 'Distansen är: {distance:.1f} nm',
	'result_speed': 'Farten är: {speed:.1f} knop',
	'result_time': 'Tiden är: {hours} h {minutes} min',

	# errors
	'error_not_number': 'Det måste vara en siffra, försök igen',
	'error_negative': 'Talet får inte vara negativt, försök igen',
	'error_time_zero': 'Tiden får inte vara 0',
	'error_speed_zero': 'Farten får inte vara 0',
	'error_menu': 'Välj 1, 2, 3, 4 eller 0',

	# window, used by dft_gui.py
	'calculate_your': 'Beräkna din',
	'calculate': 'Beräkna',
	'back': 'Tillbaka',
	'unit_distance': 'nm',
	'unit_speed': 'knop',
	'unit_hours': 'h',
	'unit_minutes': 'min',
}

# ** Functions *************************************************


# ** Main ******************************************************
# show all texts, runs only when this file is started directly
if __name__ == "__main__":
	for key, text in TEXTS.items():
		print(f"{key:<18} {text}")

# ** History ***************************************************
# 1.0 2026-10-14 Initial version
# 1.1 2026-10-14 change_language, 4 in error_menu
# 1.2 2026-10-14 nm instead of M, same as English and Czech
# 1.3 2026-10-20 texts for the window: calculate, back and units

# ** END SCRIPT ************************************************
