#!/usr/bin/python

import unittest
import math

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

def format_result(r):
	return str(r)

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

def calculate_benfords_histogram_from_text(text):
	digits_histogram = digits()
	for word in text.split():
		if word[0].isdigit(): # TODO is not a date
			digits_histogram[int(word[0])] += 1
	return digits_histogram

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

class test_calculate_frequncies_from_histogram(unittest.TestCase):
	def test_two_positions(self):
		histogram = {1: 2, 2: 18}
		frequencies = {1: 10, 2: 90}
		self.assertEqual(frequencies, calculate_frequncies_from_histogram(histogram))

unittest.main()
