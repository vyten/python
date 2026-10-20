#!/usr/bin/env python3
# **************************************************************
# File      : dft_functions.py
# Version   : 1.6
# Purpose   : functions for calculating distance, speed and time
# Linked to : dft.py
#
# Created by: Urban Björkén
# Date      : 2026-10-13
# email     : vyten@starnet.nu
# **************************************************************

# ** Imports ***************************************************
import math

# ** Variables *************************************************


# ** Functions *************************************************
# to_number() - checks the text the user wrote, returns two values: the number and None,
# or None and the key of the error message in the language files
# accepts both 2.5 and 2,5, not letters, nan, inf or negative numbers
def to_number(user_input_value):
	try:
		number = float(user_input_value.replace(',', '.'))
	except ValueError:
		return None, 'error_not_number'

	# float() also accepts nan and inf, they are not numbers that can be calculated with
	if not math.isfinite(number):
		return None, 'error_not_number'

	if number < 0:
		return None, 'error_negative'

	return number, None


# to_minutes() - converts hours and minutes to minutes
def to_minutes(hours, minutes):
	return hours * 60 + minutes


# calculate_distance() - returns the distance in nautical miles (nm)
# speed in knots, time in hours and minutes
def calculate_distance(speed, hours, minutes):
	return speed * to_minutes(hours, minutes) / 60


# calculate_speed() - returns the speed in knots
# distance in nautical miles (nm), time in hours and minutes
def calculate_speed(distance, hours, minutes):
	return distance / to_minutes(hours, minutes) * 60


# to_hours_and_minutes() - converts minutes to whole hours and minutes, returns two values
def to_hours_and_minutes(total_minutes):
	hours, minutes = divmod(round(total_minutes), 60)
	return hours, minutes


# calculate_time() - returns the time in hours and minutes
# distance in nautical miles (nm), speed in knots
def calculate_time(distance, speed):
	return to_hours_and_minutes(distance / speed * 60)


# ** Main ******************************************************
# test the functions, runs only when this file is started directly
# assert stops with AssertionError if an answer is wrong
# math.isclose() is used for decimals, since 0.1 + 0.2 is not exactly 0.3 in a computer
if __name__ == "__main__":
	# text -> number or error
	for user_input_value, expected in [('5', (5, None)), ('2,5', (2.5, None)), (' 3 ', (3, None)), ('0', (0, None)),
			('abc', (None, 'error_not_number')), ('', (None, 'error_not_number')), ('nan', (None, 'error_not_number')),
			('-inf', (None, 'error_not_number')), ('-1', (None, 'error_negative'))]:
		result = to_number(user_input_value)
		assert result == expected, f"to_number({user_input_value!r}) gave {result}, expected {expected}"

	# speed, hours, minutes -> distance
	for speed, hours, minutes, expected in [(6, 1, 30, 9), (10, 0, 45, 7.5), (5.5, 2, 0, 11)]:
		distance = calculate_distance(speed, hours, minutes)
		assert math.isclose(distance, expected), f"calculate_distance({speed}, {hours}, {minutes}) gave {distance}, expected {expected}"

	# distance, hours, minutes -> speed
	for distance, hours, minutes, expected in [(9, 1, 30, 6), (7.5, 0, 45, 10), (11, 2, 0, 5.5)]:
		speed = calculate_speed(distance, hours, minutes)
		assert math.isclose(speed, expected), f"calculate_speed({distance}, {hours}, {minutes}) gave {speed}, expected {expected}"

	# distance, speed -> hours and minutes, the last two are the 60 minute bug from the C# version
	for distance, speed, expected in [(9, 6, (1, 30)), (7.5, 10, (0, 45)), (10, 3, (3, 20)), (6, 6, (1, 0)), (5.97, 6, (1, 0))]:
		result = calculate_time(distance, speed)
		assert result == expected, f"calculate_time({distance}, {speed}) gave {result}, expected {expected}"

	print("All tests OK")

# ** History ***************************************************
# 1.0 2026-10-13 Initial version
# 1.1 2026-10-13 calculate_distance()
# 1.2 2026-10-13 calculate_speed(), to_minutes()
# 1.3 2026-10-13 calculate_time(), to_hours_and_minutes()
# 1.4 2026-10-14 tests with assert instead of printing
# 1.5 2026-10-14 nm instead of M in the comments
# 1.6 2026-10-20 to_number(), the check of numbers used by both dft.py and dft_gui.py

# ** END SCRIPT ************************************************
