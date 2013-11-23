#!/usr/bin/python

import unittest

def format_result(digits_histogram, passed_benfords_law):
	return str(digits_histogram) + "\n" + passed_benfords_law + "\n"

class benfords_law:
	def __init__(self, text):
		words = text.split()
		self.digits_histogram = {1:0, 2:0, 3:0, 4:0, 5:0, 6:0, 7:0, 8:0, 9:0}
		for word in words:
			if word[0].isdigit():
				self.digits_histogram[int(word[0])] += 1

	def get_result(self):
		return format_result(self.digits_histogram, "not passed")

class test_benfords_law(unittest.TestCase):
	def test_one_number(self):
		text = "12345"
		digits_histogram = {1:1, 2:0, 3:0, 4:0, 5:0, 6:0, 7:0, 8:0, 9:0}
		self.assertEqual(benfords_law(text).get_result(), format_result(digits_histogram, "not passed"))

	def test_two_numbers_separated_by_space(self):
		text = "12345 234"
		digits_histogram = {1:1, 2:1, 3:0, 4:0, 5:0, 6:0, 7:0, 8:0, 9:0}
		self.assertEqual(benfords_law(text).get_result(), format_result(digits_histogram, "not passed"))

unittest.main()
