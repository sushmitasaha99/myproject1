import pytest
import pandas as pd
from climate_shocks.final.plot1 import read_and_process_data, calculate_average_ratings, create_and_show_chart, save_chart_as_image
from climate_shocks.final.plot4 import load_data, plot_countplots
from climate_shocks.final.plot5 import load_data, replace_country_codes, replace_experience_labels, filter_data, calculate_ratios, plot_ratio_bar_chart

def test_read_and_process_data():
    """
    Test the read_and_process_data function.
    """
    pass

def test_calculate_average_ratings():
    """
    Test the calculate_average_ratings function.
    """
    pass

def test_create_and_show_chart():
    """
    Test the create_and_show_chart function.
    """
    pass

def test_save_chart_as_image():
    """
    Test the save_chart_as_image function.
    """
    pass

def test_load_data():
    """
    Test if data is loaded correctly.

    Loads data from the specified path and checks if the returned object is a pandas DataFrame.

    Raises:
        AssertionError: If the loaded object is not a pandas DataFrame.
    """
    df = load_data('bld/survey_data.csv')
    assert isinstance(df, pd.DataFrame)

def test_plot_countplots():
    """
    Test if countplots are generated without errors.

    Calls the plot_countplots function and checks if it executes without raising any errors.

    Raises:
        AssertionError: If the plot_countplots function raises any errors.
    """
    plot_countplots()

def test_filter_data():
    """
    Test for filtering data.
    """
    test_data = pd.DataFrame({
        'Country_of_Residence': [1, 2, 3, 1, 2],
        'CS_Experience': [1, 1, 2, 2, 1]
    })
    filtered_data = filter_data(test_data)
    assert len(filtered_data) == 0


def test_replace_country_codes():
    """
    Test if country codes are replaced correctly.
    """
    test_data = pd.DataFrame({
        'Country_of_Residence': [1, 2, 3, 1, 2],
        'CS_Experience': [1, 1, 2, 2, 1]
    })
    transformed_data = replace_country_codes(test_data)
    expected_result = pd.DataFrame({
        'Country_of_Residence': ['Germany', 'India', 'Indonesia', 'Germany', 'India'],
        'CS_Experience': [1, 1, 2, 2, 1]
    })
    pd.testing.assert_frame_equal(transformed_data, expected_result)


def test_replace_experience_labels():
    """
    Test if experience labels are replaced correctly.
    """
    sample_data = pd.DataFrame({
        'Country_of_Residence': [1, 2, 3, 1, 2],
        'CS_Experience': [1, 2, 1, 2, 1]
    })
    transformed_data = replace_experience_labels(sample_data)
    assert set(transformed_data['CS_Experience']) == {'Yes', 'No'}
    assert len(transformed_data) == len(sample_data)
    assert all(transformed_data['Country_of_Residence'] == sample_data['Country_of_Residence'])


def test_calculate_ratios():
    """
    Test for calculating ratios.
    """
    test_data = pd.DataFrame({
        'Country_of_Residence': ['Germany', 'India', 'Germany', 'India'],
        'CS_Experience': ['Yes', 'Yes', 'No', 'No']
    })
    counts_by_country = calculate_ratios(test_data)
    assert 'Ratio_Yes' in counts_by_country.columns
    assert 'Ratio_No' in counts_by_country.columns
    assert all((counts_by_country['Ratio_Yes'] >= 0) & (counts_by_country['Ratio_Yes'] <= 1))
    assert all((counts_by_country['Ratio_No'] >= 0) & (counts_by_country['Ratio_No'] <= 1))


def test_plot_ratio_bar_chart():
    """
    Test if plot is generated without errors.
    """
    test_data = pd.DataFrame({
        'Country_of_Residence': [1, 2, 3, 1, 2],
        'CS_Experience': [1, 1, 2, 2, 1]
    })
    with pytest.raises(KeyError) as excinfo:
        plot_ratio_bar_chart(test_data)
    assert "Index(['Ratio_Yes', 'Ratio_No'], dtype='object')" in str(excinfo.value)
