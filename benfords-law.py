#!/usr/bin/python

import unittest

def benfords_law(text):
	words = text.split()
	digits = {1:0, 2:0, 3:0, 4:0, 5:0, 6:0, 7:0, 8:0, 9:0}
	for word in words:
		if word[0].isdigit():
			digits[int(word[0])] += 1
	return str(digits) + "\nnot passed\n"

class test_benfords_law(unittest.TestCase):
	def test_one_number(self):
		text = "12345"
		digits = {1:1, 2:0, 3:0, 4:0, 5:0, 6:0, 7:0, 8:0, 9:0}
		output = str(digits) + "\nnot passed\n"
		self.assertEqual(benfords_law(text), output)

	def test_two_numbers_separated_by_space(self):
		text = "12345 234"
		digits = {1:1, 2:1, 3:0, 4:0, 5:0, 6:0, 7:0, 8:0, 9:0}
		output = str(digits) + "\nnot passed\n"
		self.assertEqual(benfords_law(text), output)

unittest.main()
