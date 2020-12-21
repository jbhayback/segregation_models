import pandas as pd
import numpy as np

# Class the handles calculation of Index of Dissimilarity for Segration Model
class Dissimilarity:

	def __init__(self, input_data):
		self.input_data = input_data
		self.total_X_count = self.count_char(input_data.values, 'X')
		self.total_O_count = self.count_char(input_data.values, 'O')

	def get_splitted_data(self, nrows, ncols):
		# Splits a matrix/data grid into sub-matrices based on the given number of rows and columns per split/sub-grid
		r, h = self.input_data.shape

		return (self.input_data.values.reshape(h//nrows, nrows, -1, ncols)
			.swapaxes(1, 2)
			.reshape(-1, nrows, ncols))

	def calculate_partial_index(self, tract_data):
		# Calculates the partial per tract
		x_count_in_tract = self.count_char(tract_data, 'X')
		o_count_in_tract = self.count_char(tract_data, 'O')

		return abs((x_count_in_tract/self.total_X_count) - (o_count_in_tract/self.total_O_count))

	def count_char(self, tract_data, char_to_count):
		# Counts the specific char from each tract of char sequence obtained via get_specific_data function.
		char_count = 0
		for sub_array in tract_data:
		    char_count += np.count_nonzero(sub_array == char_to_count)

		return char_count