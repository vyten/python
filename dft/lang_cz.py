#!/usr/bin/env python3
# **************************************************************
# File      : lang_cz.py
# Version   : 1.4
# Purpose   : Czech texts for dft.py and dft_gui.py
# Linked to : dft.py, dft_gui.py
#
# Created by: Urban Björkén
#             translation Richard Fleetwood
# Date      : 2026-10-14
# email     : vyten@starnet.nu
# **************************************************************

# ** Imports ***************************************************


# ** Variables *************************************************
# {name} is replaced with a value when the text is printed, :.1f means one decimal
TEXTS = {
	# title, menu and general
	'language': 'český',
	'title': 'V R C - vzdálenost rychlost čas',
	'menu_question': 'Co chcete vypočítat?',
	'distance': 'vzdálenost',
	'speed': 'rychlost',
	'time': 'čas',
	'quit': 'Ukončit',
	'change_language': 'Změnit jazyk',
	'choice': 'Volba: ',
    'goodbye': 'Na shledanou!',

	# questions
	'ask_distance': 'vzdálenost, nm: ',
	'ask_speed': 'rychlost, uzly: ',
	'ask_hours': 'čas, hodiny: ',
	'ask_minutes': 'čas, minuty: ',

	# answers
	'result_distance': 'Odhadovaná vzdálenost: {distance:.1f} nm',
	'result_speed': 'Odhadovaná rychlost: {speed:.1f} uzly',
	'result_time': 'Odhadovaný čas: {hours} h {minutes} m',

    # errors
    'error_not_number': 'Zadejte prosím číslo a zkuste to znovu.',
    'error_negative': 'Číslo nesmí být záporné. Zkuste to znovu.',
    'error_time_zero': 'Čas nesmí být nulový.',
    'error_speed_zero': 'Rychlost nesmí být nulová.',
    'error_menu': 'Vyberte 1, 2, 3, 4 nebo 0.',

	# window, used by dft_gui.py
	'calculate_your': 'Vypočtěte si svůj(e)',
	'calculate': 'Vypočtěte',
	'back': 'zpět',
	'unit_distance': 'nm',
	'unit_speed': 'kn',
	'unit_hours': 'h',
	'unit_minutes': 'm',
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
# 1.2 2026-10-14 change_language in Czech
# 1.3 2026-10-20 texts for the window: calculate, back and units
# 1.4 2026-10-21 final translation into Czech

# ** END SCRIPT ************************************************
