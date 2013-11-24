#!/usr/bin/python

import unittest
import math

class result:
	def __init__(self, histogram, frequancies, passed):
		self.histogram = histogram
		self.frequencies = frequancies
		self.passed = passed

def format_result(result):
	output = ""
	bfd = benfords_frequncy_distribution()
	for digit in range(1, 10):
		output += str(digit) + ":\t" + str(result.histogram[digit]) + "\t"
		output += str(result.frequencies[digit]) + "\t" + str(bfd[digit]) + "\t" + str(result.passed[digit]) + "\n"
	return output

def digits():
	return {1:0, 2:0, 3:0, 4:0, 5:0, 6:0, 7:0, 8:0, 9:0}

def benfords_frequncy_distribution():
	return {x: math.log(1 + (1/x), 10) for x in range (1, 10)}

class benfords_law:

	def __init__(self, text):
		self.text = text
		self.calculate_histogram()
		self.numbers_count = self.count_numbers()

	def calculate_histogram(self):
		self.digits_histogram = digits()
		for word in self.text.split():
			if word[0].isdigit(): # TODO is not a date
				self.digits_histogram[int(word[0])] += 1

	def count_numbers(self):
		numbers_count = 0
		for count in self.digits_histogram.itervalues():
			numbers_count += count
		return numbers_count

	def calculate_frequencies(self):
		digits_frequencies = digits()
		for digit, count in self.digits_histogram.iteritems():
			digits_frequencies[digit] = count * 100 / self.numbers_count
		return digits_frequencies

	def get_result(self):
		return format_result(result(self.digits_histogram, self.calculate_frequencies(), {x: False for x in range (1, 10)}))

class test_benfords_law(unittest.TestCase):
	def test_one_number(self):
		text = "12345"
		digits_histogram = {1:1, 2:0, 3:0, 4:0, 5:0, 6:0, 7:0, 8:0, 9:0}
		digits_frequencies = {1:100, 2:0, 3:0, 4:0, 5:0, 6:0, 7:0, 8:0, 9:0}
		digits_passed = {x: False for x in range (1, 10)}
		r = result(digits_histogram, digits_frequencies, digits_passed)
		self.assertEqual(benfords_law(text).get_result(), format_result(r))

	def test_two_numbers_separated_by_space(self):
		text = "12345 234"
		digits_histogram = {1:1, 2:1, 3:0, 4:0, 5:0, 6:0, 7:0, 8:0, 9:0}
		digits_frequencies = {1:50, 2:50, 3:0, 4:0, 5:0, 6:0, 7:0, 8:0, 9:0}
		digits_passed = {x: False for x in range (1, 10)}
		r = result(digits_histogram, digits_frequencies, digits_passed)
		self.assertEqual(benfords_law(text).get_result(), format_result(r))

class test_format_result(unittest.TestCase):
	def test_print(self):
		digits_histogram = {x: x for x in range(1, 10)}
		digits_frequencies = {x: 10 - x for x in range(1, 10)}
		digits_passed = {x: (x % 2) == 0 for x in range(1, 10)}
		r = result(digits_histogram, digits_frequencies, digits_passed)
		bfd = benfords_frequncy_distribution()
		output = ""
		for digit in range(1, 10):
			output += str(digit) + ":\t" + str(digits_histogram[digit]) + "\t"
			output += str(digits_frequencies[digit]) + "\t" + str(bfd[digit]) + "\t" + str(digits_passed[digit]) + "\n"
		self.assertEqual(output, format_result(r))

unittest.main()
