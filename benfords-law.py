#!/usr/bin/python

import unittest
import math
import argparse
import sys

class result:
	def __init__(self, histogram, frequencies, passed):
		self.histogram = histogram
		self.frequencies = frequencies
		self.passed = passed

	def __str__(self):
		output = ""
		bfd = benfords_frequncy_distribution()
		for digit in range(1, 10):
			output += str(digit) + ":\t" + str(self.histogram[digit]) + "\t"
			output += str(self.frequencies[digit]) + "\t" + str(bfd[digit]) + "\t" + str(self.passed[digit]) + "\n"
		return output

def digits():
	return {x: 0 for x in range(1, 10)}

def benfords_frequncy_distribution():
	return {x: math.log(1 + (1/x), 10) for x in range (1, 10)}

def calculate_frequncies_from_histogram(histogram):
	count = 0
	for c in histogram.itervalues():
		count += c
	frequencies  = dict()
	for k,v in histogram.iteritems():
		frequencies[k] = v * 100 / count
	return frequencies

def skip_zeros(word):
	i = 0;
	while i < len(word) and word[i].isdigit() and int(word[i]) == 0: i += 1
	if i < len(word) and word[i].isdigit(): return i
	return None

def calculate_benfords_histogram_from_text(text):
	digits_histogram = digits()
	for word in text.split():
		i = skip_zeros(word)
		if i != None: # TODO is not a date
			digits_histogram[int(word[i])] += 1
	return digits_histogram

def expected_distribution_test_for_digits_frequencies(expected, frequencies, treshold = 0):
	return {x: math.fabs(frequencies[x] - expected[x]) <= treshold for x in range(1, 10)}

class benfords_law:

	def __init__(self, text):
		self.text = text

	def calculate_histogram(self):
		return calculate_benfords_histogram_from_text(self.text)

	def get_result(self):
		histogram = self.calculate_histogram()
		return format_result(result(histogram, calculate_frequncies_from_histogram(histogram), {x: False for x in range (1, 10)}))

class test_calculate_benfords_histogram_from_text(unittest.TestCase):
	def test_one_number(self):
		text = "12345"
		digits_histogram = {1:1, 2:0, 3:0, 4:0, 5:0, 6:0, 7:0, 8:0, 9:0}
		self.assertEqual(calculate_benfords_histogram_from_text(text), digits_histogram)

	def test_two_numbers_separated_by_space(self):
		text = "12345 234"
		digits_histogram = {1:1, 2:1, 3:0, 4:0, 5:0, 6:0, 7:0, 8:0, 9:0}
		self.assertEqual(calculate_benfords_histogram_from_text(text), digits_histogram)

	def test_number_among_words(self):
		text = "abc 987 zdf"
		digits_histogram = {1:0, 2:0, 3:0, 4:0, 5:0, 6:0, 7:0, 8:0, 9:1}
		self.assertEqual(calculate_benfords_histogram_from_text(text), digits_histogram)

	def test_number_with_dot_colon(self):
		text = "2,34 5.34"
		digits_histogram = {1:0, 2:1, 3:0, 4:0, 5:1, 6:0, 7:0, 8:0, 9:0}
		self.assertEqual(calculate_benfords_histogram_from_text(text), digits_histogram)

	def test_number_starting_from_zeros(self):
		text = "00345"
		digits_histogram = {1:0, 2:0, 3:1, 4:0, 5:0, 6:0, 7:0, 8:0, 9:0}
		self.assertEqual(calculate_benfords_histogram_from_text(text), digits_histogram)

class test_result_str(unittest.TestCase):
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
		self.assertEqual(output, str(r))

class test_calculate_frequncies_from_histogram(unittest.TestCase):
	def test_two_positions(self):
		histogram = {1: 2, 2: 18}
		frequencies = {1: 10, 2: 90}
		self.assertEqual(frequencies, calculate_frequncies_from_histogram(histogram))

class test_expected_distribution_test_for_digits_frequencies(unittest.TestCase):
	def test_all_failed(self):
		frequencies = {x: 1 for x in range(1, 10)}
		expected = {x: 2 for x in range(1, 10)}
		marks = {x: False for x in range(1, 10)}
		self.assertEqual(marks, expected_distribution_test_for_digits_frequencies(expected, frequencies))

	def test_all_passed(self):
		frequencies = {x: 1 for x in range(1, 10)}
		marks = {x: True for x in range(1, 10)}
		self.assertEqual(marks, expected_distribution_test_for_digits_frequencies(frequencies, frequencies))

	def test_two_passed(self):
		frequencies = {x: 1 for x in range(1, 10)}
		expected = {x: 2 for x in range(1, 10)}
		marks = {x: False for x in range(1, 10)}
		for i in [2, 7]:
			frequencies[i] = expected[i]
			marks[i] = True
		self.assertEqual(marks, expected_distribution_test_for_digits_frequencies(expected, frequencies))

	def test_two_passed_with_treshold(self):
		frequencies = {x: 1 for x in range(1, 10)}
		expected = {x: 3 for x in range(1, 10)}
		marks = {x: False for x in range(1, 10)}
		frequencies[2] = expected[2] + 1
		marks[2] = True
		frequencies[7] = expected[7] - 1
		marks[7] = True
		self.assertEqual(marks, expected_distribution_test_for_digits_frequencies(expected, frequencies, 1))

test_program_option = "--run-tests"
parser = argparse.ArgumentParser(description="Check a text document against Benford's law.")
parser.add_argument(test_program_option, dest='test', action='store_true',
		help='run unit tests')

args = parser.parse_args()

if args.test:
	sys.argv.remove(test_program_option)
	unittest.main()
