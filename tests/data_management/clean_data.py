import pandas as pd

def read_data(file_path):
    """
    Read data from a CSV file.

    Args:
        file_path (str): The path to the CSV file.

    Returns:
        pd.DataFrame: A DataFrame containing the data read from the CSV file.
    """
    data = pd.read_csv(file_path)
    return data

def clean_column_names(data):
    """
    Clean column names by removing leading and trailing whitespaces.

    Args:
        data (pd.DataFrame): The DataFrame containing the data.

    Returns:
        pd.DataFrame: The DataFrame with cleaned column names.
    """
    data.columns = data.columns.str.strip()
    return data

def rename_countries(data):
    """
    Rename values in the "Country_of_Residence" column.

    Args:
        data (pd.DataFrame): The DataFrame containing the data.

    Returns:
        pd.DataFrame: The DataFrame with renamed country values.
    """
    data['Country_of_Residence'] = data['Country_of_Residence'].replace({
        1: 'Germany',
        2: 'India',
        3: 'Indonesia'
    })
    return data

def filter_data(data):
    """
    Filter data columns and rows to prepare for analysis.

    Args:
        data (pd.DataFrame): The DataFrame containing the data.

    Returns:
        pd.DataFrame: The filtered DataFrame.
    """
    
    filtered_columns = data.filter(regex='^(EAI_(1[0-9]|[1-9]|2[0-4])|Country_of_Residence)$', axis=1)

    
    filtered_data = filtered_columns[filtered_columns['Country_of_Residence'].isin(['Germany', 'India', 'Indonesia'])]

    return filtered_data

def save_filtered_data(data, file_path):
    """
    Save filtered data to a CSV file.

    Args:
        data (pd.DataFrame): The DataFrame containing the filtered data.
        file_path (str): The path to save the CSV file.

    Returns:
        None
    """
    
    column_order = ['Country_of_Residence'] + [col for col in data if col != 'Country_of_Residence']

    
    data[column_order].to_csv(file_path, index=False)

def clean_data(data):
    """
    Clean data by applying all necessary cleaning operations.

    Args:
        data (pd.DataFrame): The DataFrame containing the data.

    Returns:
        pd.DataFrame: The DataFrame with cleaned data.
    """
    data = clean_column_names(data)
    data = rename_countries(data)
    return data

def main():
    """
    Main function to execute the data filtering process.
    """
    
    data = read_data('bld/survey_data.csv')

    
    data = clean_data(data)

    
    filtered_data = filter_data(data)

    
    save_filtered_data(filtered_data, 'bld/clean_filtered_data.csv')

if __name__ == "__main__":
    main()
