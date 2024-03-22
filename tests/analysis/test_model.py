"""Tests for the t-test model."""


import os
import pandas as pd
import numpy as np
import pytest
from scipy.stats import ttest_ind
import seaborn as sns
import matplotlib.pyplot as plt
from climate_shocks.analysis.model import load_data, replace_column_names, perform_t_test



""" Defining our test data'"""

test_data = pd.DataFrame({
    'JB_low_A_sustainability': [1, 2, 3, 4, 5],
    'JB_high_A_sustainability': [6, 7, 8, 9, 10],
    'JB_low_A_moral': [11, 12, 13, 14, 15],
    'JB_high_A_moral': [16, 17, 18, 19, 20]
})

def test_load_data():
    """
    Test loading data function.

    Checks if the data is loaded correctly from a CSV file.
    """
    file_path = 'test_survey_data.csv'
    test_data.to_csv(file_path, index=False)
    loaded_data = load_data(file_path)
    assert loaded_data.equals(test_data)
    os.remove(file_path)

def test_replace_column_names():
    """
    Test column name replacement function.

    Checks if the function correctly replaces column names.
    """
    column_names = ['I_would', 'others_would', 'people_should', 'other_column']
    expected_names = ['I would', 'Others would', 'People should', 'other_column']
    test_df = pd.DataFrame(columns=column_names)
    replaced_df = replace_column_names(test_df)
    assert list(replaced_df.columns) == expected_names

def test_perform_t_test():
    """
    Test t-test function.

    Checks if the t-test is performed correctly for specified categories.
    """
    persons = ['A']
    categories_order = ['sustainability', 'moral']
    t_test_results = perform_t_test(test_data, persons, categories_order)
    assert len(t_test_results) == len(persons) * len(categories_order)


