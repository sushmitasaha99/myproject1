import numpy as np
import pandas as pd
import pytest
from climate_shocks.config import TEST_DIR
from climate_shocks.data_management.clean_data import read_data, clean_column_names, rename_countries, filter_data, save_filtered_data, clean_data
from climate_shocks.utilities import read_yaml


@pytest.fixture
def sample_data():
    """
    Fixture to provide sample data for testing.
    """

    data = pd.DataFrame({
        'EAI_1': [1, 2, 3],
        'EAI_2': [4, 5, 6],
        'Country_of_Residence': [1, 2, 3]
    })
    return data

def test_read_data(sample_data):
    """
    Test read_data function.
    """
    
    file_path = 'test_data.csv'
    sample_data.to_csv(file_path, index=False)
    loaded_data = read_data(file_path)
    
    assert loaded_data.equals(sample_data)
    
    import os
    os.remove(file_path)

def test_clean_column_names(sample_data):
    """
    Test clean_column_names function.
    """

    sample_data.columns = [' EAI_1 ', ' EAI_2 ', ' Country_of_Residence ']
    
    cleaned_data = clean_column_names(sample_data)
    
    assert cleaned_data.columns.tolist() == ['EAI_1', 'EAI_2', 'Country_of_Residence']

def test_rename_countries(sample_data):
    """
    Test rename_countries function.
    """
    renamed_data = rename_countries(sample_data)
    
    assert renamed_data['Country_of_Residence'].tolist() == ['Germany', 'India', 'Indonesia']


def test_save_filtered_data(sample_data):
    """
    Test save_filtered_data function.
    """
   
    file_path = 'tests/data_management/data_fixture.csv'
    
    
    save_filtered_data(sample_data, file_path)
    
    saved_data = pd.read_csv(file_path)
    


