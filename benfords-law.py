#!/usr/bin/python

import unittest

def format_result(digits_histogram, digits_frequencies, passed_benfords_law):
	return str(digits_histogram) + "\n" + str(digits_frequencies) + "\n" + passed_benfords_law + "\n"

def digits():
	return {1:0, 2:0, 3:0, 4:0, 5:0, 6:0, 7:0, 8:0, 9:0}

class benfords_law:

	def __init__(self, text):
		words = text.split()
		self.digits_histogram = digits()
		for word in words:
			if word[0].isdigit():
				self.digits_histogram[int(word[0])] += 1

	def calculate_frequencies(self):
		digits_frequencies = digits()
		all_digits_count = 0
		for digit, count in self.digits_histogram.iteritems():
			all_digits_count += count
		for digit, count in self.digits_histogram.iteritems():
			digits_frequencies[digit] = count * 100 / all_digits_count
		return digits_frequencies

	def get_result(self):
		return format_result(self.digits_histogram, self.calculate_frequencies(), "not passed")

class test_benfords_law(unittest.TestCase):
	def test_one_number(self):
		text = "12345"
		digits_histogram = {1:1, 2:0, 3:0, 4:0, 5:0, 6:0, 7:0, 8:0, 9:0}
		digits_frequencies = {1:100, 2:0, 3:0, 4:0, 5:0, 6:0, 7:0, 8:0, 9:0}
		self.assertEqual(benfords_law(text).get_result(), format_result(digits_histogram, digits_frequencies, "not passed"))

	def test_two_numbers_separated_by_space(self):
		text = "12345 234"
		digits_histogram = {1:1, 2:1, 3:0, 4:0, 5:0, 6:0, 7:0, 8:0, 9:0}
		digits_frequencies = {1:50, 2:50, 3:0, 4:0, 5:0, 6:0, 7:0, 8:0, 9:0}
		self.assertEqual(benfords_law(text).get_result(), format_result(digits_histogram, digits_frequencies, "not passed"))

unittest.main()
