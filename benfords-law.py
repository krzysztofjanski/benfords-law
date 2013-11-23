#!/usr/bin/python

import unittest

def format_result(digits, passed_benfords_law):
	return str(digits) + "\n" + passed_benfords_law + "\n"

class benfords_law:
	def __init__(self, text):
		words = text.split()
		self.digits = {1:0, 2:0, 3:0, 4:0, 5:0, 6:0, 7:0, 8:0, 9:0}
		for word in words:
			if word[0].isdigit():
				self.digits[int(word[0])] += 1

	def get_result(self):
		return format_result(self.digits, "not passed")

class test_benfords_law(unittest.TestCase):
	def test_one_number(self):
		text = "12345"
		digits = {1:1, 2:0, 3:0, 4:0, 5:0, 6:0, 7:0, 8:0, 9:0}
		self.assertEqual(benfords_law(text).get_result(), format_result(digits, "not passed"))

	def test_two_numbers_separated_by_space(self):
		text = "12345 234"
		digits = {1:1, 2:1, 3:0, 4:0, 5:0, 6:0, 7:0, 8:0, 9:0}
		self.assertEqual(benfords_law(text).get_result(), format_result(digits, "not passed"))

unittest.main()
