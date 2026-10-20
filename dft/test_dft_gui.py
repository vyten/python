#!/usr/bin/env python3
# **************************************************************
# File      : test_dft_gui.py
# Version   : 1.0
# Purpose   : tests for the window in dft_gui.py, clicks the buttons and reads the answers
# Linked to : dft_gui.py, dft_language.py
#
# Created by: Urban Björkén
# Date      : 2026-10-20
# email     : vyten@starnet.nu
# **************************************************************

# ** Imports ***************************************************
import unittest
import logging
import tempfile
import tkinter as tk
from os import path
import dft_gui
import dft_language

# ** Variables *************************************************


# ** Functions *************************************************
# find_widgets() - all controls of one kind in the window, also those inside frames, in the order they are shown
def find_widgets(parent, widget_class):
	found = []
	for widget in parent.winfo_children():
		if widget.winfo_class() == widget_class:
			found.append(widget)
		found += find_widgets(widget, widget_class)
	return found


# setUpModule() - runs once before all tests
# logging is turned off, the tests make errors on purpose and they should not end up in dft.log
def setUpModule():
	logging.disable(logging.CRITICAL)


# tearDownModule() - runs once after all tests
def tearDownModule():
	logging.disable(logging.NOTSET)


# ** Classes ***************************************************
# TestDftGui - each method that starts with test_ is one test, unittest runs them in alphabetical order
# setUp() runs before each test and tearDown() after, so every test starts with a new window
class TestDftGui(unittest.TestCase):

	def setUp(self):
		# the saved language goes to a temporary directory, so the real dft_lang.txt is not touched
		self.temp_dir = tempfile.TemporaryDirectory()
		self.real_lang_file = dft_language.LANG_FILE
		dft_language.LANG_FILE = path.join(self.temp_dir.name, dft_language.LANG_FILE_NAME)
		self.window = None

	def tearDown(self):
		if self.window is not None:
			try:
				self.window.destroy()
			except tk.TclError:
				pass    # already closed, for example by the quit button
		dft_language.LANG_FILE = self.real_lang_file
		self.temp_dir.cleanup()

	# -- helpers --------------------------------------------------

	# save_language() - as if the language was chosen last time
	def save_language(self, number):
		with open(dft_language.LANG_FILE, 'w') as lang_file:
			lang_file.write(number)

	# saved_language() - what is in the language file now
	def saved_language(self):
		with open(dft_language.LANG_FILE) as lang_file:
			return lang_file.read()

	# open_window() - creates the window without mainloop(), update() draws it
	def open_window(self):
		try:
			self.window = dft_gui.create_window()
		except tk.TclError as error:
			self.skipTest(f"no screen to show the window on: {error}")
		self.window.update()

	# click() - clicks the button with the text
	def click(self, text):
		for button in find_widgets(self.window, 'Button'):
			if button.cget('text') == text:
				button.invoke()
				self.window.update()
				return
		self.fail(f"no button '{text}'")

	# click_flag() - clicks flag number 0, 1 or 2 (Swedish, English, Czech)
	def click_flag(self, index):
		flags = [button for button in find_widgets(self.window, 'Button') if button.cget('image')]
		flags[index].invoke()
		self.window.update()

	# fill() - writes the values in the fields, from the top
	def fill(self, *values):
		for entry, value in zip(self.entries(), values):
			entry.delete(0, 'end')
			entry.insert(0, value)

	def entries(self):
		return find_widgets(self.window, 'Entry')

	# texts() - all texts on the page that are not empty
	def texts(self):
		return [label.cget('text') for label in find_widgets(self.window, 'Label') if label.cget('text').strip()]

	# answer() - the answer or error line, the second label on the calculation page
	def answer(self):
		return find_widgets(self.window, 'Label')[1]

	# red_fields() - the numbers of the fields that are red
	def red_fields(self):
		return [index for index, entry in enumerate(self.entries()) if entry.cget('bg') == dft_gui.COL_ERROR]

	# -- the language ---------------------------------------------

	def test_first_time_shows_flags(self):
		self.open_window()
		self.assertEqual(self.window.title(), dft_gui.WINDOW_TITLE)
		flags = [button for button in find_widgets(self.window, 'Button') if button.cget('image')]
		self.assertEqual(len(flags), 3)

	def test_flag_saves_language_and_shows_start_page(self):
		self.open_window()
		self.click_flag(1)
		self.assertEqual(self.saved_language(), '2')
		self.assertEqual(self.window.title(), 'D S T - Distance Speed Time')
		self.assertIn('Calculate your', self.texts())

	def test_saved_language_shows_start_page_directly(self):
		self.save_language('3')
		self.open_window()
		self.assertIn('Vypočtěte si svůj(e)', self.texts())

	def test_broken_language_file_shows_flags(self):
		self.save_language('xyz')
		self.open_window()
		flags = [button for button in find_widgets(self.window, 'Button') if button.cget('image')]
		self.assertEqual(len(flags), 3)

	def test_small_flag_changes_language_and_keeps_values(self):
		self.save_language('2')
		self.open_window()
		self.click('Distance')
		self.fill('6', '1', '30')
		self.click_flag(0)    # the small Swedish flag
		self.assertEqual(self.saved_language(), '1')
		self.assertIn('Distans', self.texts())
		self.assertEqual([entry.get() for entry in self.entries()], ['6', '1', '30'])

	# -- the calculations -----------------------------------------

	def test_distance(self):
		self.save_language('1')
		self.open_window()
		self.click('Distans')
		self.fill('6', '1', '30')
		self.click('Beräkna')
		self.assertEqual(self.answer().cget('text'), 'Distansen är: 9.0 nm')

	def test_speed(self):
		self.save_language('1')
		self.open_window()
		self.click('Fart')
		self.fill('9', '1', '30')
		self.click('Beräkna')
		self.assertEqual(self.answer().cget('text'), 'Farten är: 6.0 knop')

	def test_time(self):
		self.save_language('1')
		self.open_window()
		self.click('Tid')
		self.fill('10', '3')
		self.click('Beräkna')
		self.assertEqual(self.answer().cget('text'), 'Tiden är: 3 h 20 min')

	def test_decimal_comma(self):
		self.save_language('1')
		self.open_window()
		self.click('Distans')
		self.fill('5,5', '2', '0')
		self.click('Beräkna')
		self.assertEqual(self.answer().cget('text'), 'Distansen är: 11.0 nm')

	def test_enter_calculates(self):
		self.save_language('1')
		self.open_window()
		self.click('Tid')
		self.fill('10', '3')
		self.entries()[0].event_generate('<Return>')
		self.window.update()
		self.assertEqual(self.answer().cget('text'), 'Tiden är: 3 h 20 min')

	# -- the errors -----------------------------------------------

	def test_letters_give_error_and_red_field(self):
		self.save_language('1')
		self.open_window()
		self.click('Distans')
		self.fill('6', 'abc', '30')
		self.click('Beräkna')
		self.assertEqual(self.answer().cget('text').strip(), 'Det måste vara en siffra, försök igen')
		self.assertEqual(self.answer().cget('bg'), dft_gui.COL_ERROR)
		self.assertEqual(self.red_fields(), [1])

	def test_negative_gives_error(self):
		self.save_language('1')
		self.open_window()
		self.click('Tid')
		self.fill('-1', '3')
		self.click('Beräkna')
		self.assertEqual(self.answer().cget('text').strip(), 'Talet får inte vara negativt, försök igen')
		self.assertEqual(self.red_fields(), [0])

	def test_time_zero_gives_error(self):
		self.save_language('1')
		self.open_window()
		self.click('Fart')
		self.fill('9', '0', '0')
		self.click('Beräkna')
		self.assertEqual(self.answer().cget('text').strip(), 'Tiden får inte vara 0')

	def test_speed_zero_gives_error(self):
		self.save_language('1')
		self.open_window()
		self.click('Tid')
		self.fill('10', '0')
		self.click('Beräkna')
		self.assertEqual(self.answer().cget('text').strip(), 'Farten får inte vara 0')

	def test_corrected_error_removes_red(self):
		self.save_language('1')
		self.open_window()
		self.click('Tid')
		self.fill('x', '3')
		self.click('Beräkna')
		self.fill('10', '3')
		self.click('Beräkna')
		self.assertEqual(self.answer().cget('text'), 'Tiden är: 3 h 20 min')
		self.assertEqual(self.answer().cget('bg'), dft_gui.COL_BACKGROUND)
		self.assertEqual(self.red_fields(), [])

	# -- the buttons ----------------------------------------------

	def test_back_shows_start_page_and_removes_enter(self):
		self.save_language('1')
		self.open_window()
		self.click('Distans')
		self.click('« Tillbaka')
		self.assertIn('Beräkna din', self.texts())
		self.assertEqual(self.entries(), [])
		self.assertEqual(self.window.bind('<Return>'), '')

	def test_quit_closes_window(self):
		self.save_language('1')
		self.open_window()
		self.click('Avsluta')
		with self.assertRaises(tk.TclError):
			self.window.winfo_exists()


# ** Main ******************************************************
# run all tests, runs only when this file is started directly
if __name__ == "__main__":
	unittest.main(verbosity=2)

# ** History ***************************************************
# 1.0 2026-10-20 Initial version

# ** END SCRIPT ************************************************
