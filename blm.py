import unittest
import math

class result:
	def __init__(self, histogram, frequencies, passed):
		self.histogram = histogram
		self.frequencies = frequencies
		self.passed = passed

	def __str__(self):
		output = self.get_header()
		bfd = benfords_frequncy_distribution()
		for digit in range(1, 10):
			output += self.get_format().format(digit, self.histogram[digit], self.frequencies[digit],
					bfd[digit], self.passed[digit])
		return output

	def get_format(self):
		return "{0:d}:\t{1:d}\t\t{2:f}\t{3:f}\t{4}\n"

	def get_header(self):
		return "digit\thistogram\tfrequency\tbenfords\tpassed\n"

def digits():
	return {x: 0 for x in range(1, 10)}

def benfords_frequncy_distribution():
	return {x: math.log(float(1) + (float(1)/float(x)), float(10)) for x in range (1, 10)}

def calculate_frequncies_from_histogram(histogram):
	count = 0
	for c in histogram.itervalues():
		count += c
	frequencies  = dict()
	for k,v in histogram.iteritems():
		frequencies[k] = float(v) / float(count)
	return frequencies

def skip_minus(word):
	if word[0] == '-': return 1
	return 0

def skip_zeros(word):
	i = 0;
	while i < len(word) and word[i].isdigit() and int(word[i]) == 0: i += 1
	return i

def calculate_benfords_histogram_from_text(text):
	digits_histogram = digits()
	for word in text.split():
		i = 0
		i += skip_minus(word)
		i += skip_zeros(word)
		if i < len(word) and word[i].isdigit(): # TODO is not a date
			digits_histogram[int(word[i])] += 1
	return digits_histogram

def expected_distribution_test_for_digits_frequencies(expected, frequencies, treshold = 0):
	return {x: math.fabs(frequencies[x] - expected[x]) <= treshold for x in range(1, 10)}

class benfords_law:

	def __init__(self, text, treshold = 0):
		self.text = text
		self.treshold = treshold

	def get_result(self):
		bfd = benfords_frequncy_distribution()
		histogram = calculate_benfords_histogram_from_text(self.text)
		frequencies = calculate_frequncies_from_histogram(histogram)
		marks = expected_distribution_test_for_digits_frequencies(bfd, frequencies,	self.treshold)
		return str(result(histogram, frequencies, marks))

class test_calculate_benfords_histogram_from_text(unittest.TestCase):
	def test_one_number(self):
		text = "12345"
		digits_histogram = {1:1, 2:0, 3:0, 4:0, 5:0, 6:0, 7:0, 8:0, 9:0}
		self.assertEqual(calculate_benfords_histogram_from_text(text), digits_histogram)

	def test_negative_number(self):
		text = "-12345"
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
		digits_frequencies = {x: float(10) - float(x) for x in range(1, 10)}
		digits_passed = {x: (x % 2) == 0 for x in range(1, 10)}
		r = result(digits_histogram, digits_frequencies, digits_passed)
		bfd = benfords_frequncy_distribution()
		output = r.get_header()
		for digit in range(1, 10):
			output += r.get_format().format(digit, digits_histogram[digit], digits_frequencies[digit],
					bfd[digit], digits_passed[digit])
		self.assertEqual(output, str(r))

class test_calculate_frequncies_from_histogram(unittest.TestCase):
	def test_two_positions(self):
		histogram = {1: 2, 2: 18}
		frequencies = {1: 0.1, 2: 0.9}
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

if __name__ == '__main__':
    unittest.main()
