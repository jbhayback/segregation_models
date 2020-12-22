import pytest
import pandas as pd
import numpy as np

import os,sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Fixtures
@pytest.fixture
def dissimilarity_seg_model():
	from Dissimilarity import Dissimilarity as DissimilaritySegregationModel

	raw_test_input_data = pd.read_csv('./tests/Input_test_data.csv').fillna('')

	return DissimilaritySegregationModel(raw_test_input_data)

@pytest.fixture
def application_main():
	import App as app

	return app

# App tests
def test_main_app_count_char(application_main):
	# Expected values
	expected_X_char_count = 15
	expected_O_char_count = 14
	expected_blank_char_count = 7

	# Actual values
	raw_test_input_data = pd.read_csv('./tests/Input_test_data.csv').fillna('')
	X_char_count = application_main.count_char(raw_test_input_data.values, 'X')
	O_char_count = application_main.count_char(raw_test_input_data.values, 'O')
	empty_char_count = application_main.count_char(raw_test_input_data.values, '')

	# Assertions
	assert X_char_count == expected_X_char_count
	assert O_char_count == expected_O_char_count
	assert empty_char_count == expected_blank_char_count

def test_main_app_count_char2(application_main):
	# Expected values
	expected_X_char_count = 12
	expected_O_char_count = 15
	expected_blank_char_count = 9

	# Actual values
	raw_test_input_data = pd.read_csv('./tests/Input_test_data_2.csv').fillna('')
	X_char_count = application_main.count_char(raw_test_input_data.values, 'X')
	O_char_count = application_main.count_char(raw_test_input_data.values, 'O')
	empty_char_count = application_main.count_char(raw_test_input_data.values, '')

	# Assertions
	assert X_char_count == expected_X_char_count
	assert O_char_count == expected_O_char_count
	assert empty_char_count == expected_blank_char_count

def test_validate_data_for_invalid_chars(application_main):
	# Valid input test data (no characters other than X, O and blank/empty)
	raw_test_input_valid_data = pd.read_csv('./tests/Input_test_data.csv').fillna('')
	assert application_main.validate_data_for_invalid_chars(raw_test_input_valid_data) == True

	# Invalid input test data (with characters other than X, O and blank/empty)
	raw_test_input_invalid_data = pd.read_csv('./tests/Input_test_invalid_data.csv').fillna('')
	assert application_main.validate_data_for_invalid_chars(raw_test_input_invalid_data) == False

def test_validate_row_column_inputs(application_main):
	# Test data is 6x6 matrix
	raw_test_input_data = pd.read_csv('./tests/Input_test_data.csv').fillna('')

	# Valid input data 2x2 which are both multiples of 36(total population)
	assert application_main.validate_row_column_inputs(raw_test_input_data, 2, 2)[0] == True
	assert application_main.validate_row_column_inputs(raw_test_input_data, 2, 2)[1] == 'SUCCESS'

	# Invalid data 2x5 since 10 is not a multiple of 36(total population)
	assert application_main.validate_row_column_inputs(raw_test_input_data, 2, 5)[0] == False
	assert application_main.validate_row_column_inputs(raw_test_input_data, 2, 5)[1] == 'NOT_MULTIPLE'

	# Invalid data 9x4 though its product is multiple of 36(total population), its row(m) is not a multiple of M which is 6
	assert application_main.validate_row_column_inputs(raw_test_input_data, 9, 4)[0] == False
	assert application_main.validate_row_column_inputs(raw_test_input_data, 9, 4)[1] == 'CANT_SPLIT'


def test_convert_char_seq_to_numeric_grid(application_main):
	# Test input data is 6x6 character matrix
	character_seq_test_input_data = pd.read_csv('./tests/Input_test_data.csv').fillna('')

	# Converted test data to 6x6 numeric matrix (1 - X, -1 is O and 0 is blank/empty)
	numeric_test_input_data = pd.read_csv('./tests/Converted_to_numeric_input_test_data.csv').fillna('')
	assert application_main.convert_char_seq_to_numeric_grid(character_seq_test_input_data).equals(numeric_test_input_data)

def test_convert_numeric_grid_to_char_seq_grid(application_main):
	# Test input data of 6x6 numeric matrix
	numeric_test_data = pd.read_csv('./tests/Converted_to_numeric_input_test_data.csv').fillna('')

	# Converted test datato 6x6 character matrix (1 - X, -1 is O and 0 is blank/empty)
	character_seq_test_input_data = pd.read_csv('./tests/Input_test_data.csv').fillna('')
	assert application_main.convert_numeric_grid_to_char_seq_grid(numeric_test_data).equals(character_seq_test_input_data)

# Dissimilarity Tests
def test_get_splitted_data(dissimilarity_seg_model):
	# Expected 3x3x4 3D Array - these are the expected Tracts to be created when 6x6 Matrix will be splitted to 3x3 matrices per Tract
	expected_tracts_array =[[['X','X','O'],['X','O','O'],['O','X','X']],
		[['O','X',''],['X','O',''],['','X','O']],
		[['O','X','X'],['X','O','O'],['O','O','']],
		[['X','O','X'],['X','O','X'],['','','']]],
	[[['X','X','O'],['X','O','O'],['O','X','X']],
		[['O','X',''],['X','O',''],['','X','O']],
		[['O','X','X'],['X','O','O'],['O','O','']],
		[['X','O','X'],['X','O','X'],['','','']]]
	assert (dissimilarity_seg_model.get_splitted_data(3, 3) == np.array(expected_tracts_array)).all()

def test_calculate_partial_index(dissimilarity_seg_model):
	expected_partial_index = 0.07
	# For 2x2 Tract from the original 6x6 data grid
	actual_partial_index = round(dissimilarity_seg_model.calculate_partial_index(
		dissimilarity_seg_model.input_data.iloc[0:1, 0:1].values), 2)
	assert actual_partial_index == expected_partial_index 

	expected_partial_index = 0.13
	# For 3x3 Tract from the original 6x6 data grid
	actual_partial_index = round(dissimilarity_seg_model.calculate_partial_index(
		dissimilarity_seg_model.input_data.iloc[0:2, 0:2].values), 2)
	assert actual_partial_index == expected_partial_index 

def test_count_char(dissimilarity_seg_model):
	# Expected Values
	expected_X_char_count = 15
	expected_O_char_count = 14
	expected_blank_char_count = 7

	# Actual Values
	X_char_count = dissimilarity_seg_model.count_char(dissimilarity_seg_model.input_data.values, 'X')
	O_char_count = dissimilarity_seg_model.count_char(dissimilarity_seg_model.input_data.values, 'O')
	blank_char_count = dissimilarity_seg_model.count_char(dissimilarity_seg_model.input_data.values, '')

	# Assertions
	assert X_char_count == expected_X_char_count
	assert O_char_count == expected_O_char_count
	assert blank_char_count == expected_blank_char_count