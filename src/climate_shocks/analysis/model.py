import os
import pandas as pd
from scipy.stats import ttest_ind

# Define our functions here...
def load_data(file_path):
    """
    Load data from a CSV file into a pandas DataFrame.

    Parameters:
    file_path (str): The path to the CSV file.

    Returns:
    pandas.DataFrame: The loaded DataFrame.
    """
    return pd.read_csv(file_path).apply(pd.to_numeric, errors='coerce')

def replace_column_names(dataframe):
    """
    Replace column names to enhance readability.

    Parameters:
    dataframe (pandas.DataFrame): The DataFrame with original column names.

    Returns:
    pandas.DataFrame: The DataFrame with replaced column names.
    """
    return dataframe.rename(columns=lambda x: x.replace('I_would', 'I would')
                                                .replace('others_would', 'Others would')
                                                .replace('people_should', 'People should'))

def perform_t_test(dataframe, persons, categories_order):
    """
    Perform independent t-tests for low and high risk ratings among different categories and persons.

    Parameters:
    dataframe (pandas.DataFrame): The DataFrame containing ratings.
    persons (list): List of persons.
    categories_order (list): Order of categories.

    Returns:
    pandas.DataFrame: DataFrame containing t-test results.
    """
    t_test_results = []

    for person in persons:
        for category in categories_order:
            low_risk_data = dataframe[f'JB_low_{person}_{category}'].dropna()
            high_risk_data = dataframe[f'JB_high_{person}_{category}'].dropna()

            t_statistic, p_value = ttest_ind(low_risk_data, high_risk_data)

            t_test_results.append({'Person': person, 'Category': category, 'T-Statistic': t_statistic, 'P-Value': p_value})

    return pd.DataFrame(t_test_results)


file_path = 'bld/survey_data.csv'
df = load_data(file_path)
df = replace_column_names(df)

''' Performing t-tests'''

persons = ['A', 'B', 'C']
categories_order = ['sustainability', 'moral', 'I would', 'Others would', 'People should']
t_test_results = perform_t_test(df, persons, categories_order)

'''Printing statements for debugging'''

print("Dataframe shape after loading:", df.shape)
print("T-test results:")
print(t_test_results)
print("If our null hypothesis is that there is no significant difference in the average ratings between low and high climate risk for each category, then here we already see there is a statistically significant difference in sustainability ratings between low and high risk for Person A. As, since the p-value is less than the common significance level of 0.05, thus we reject the null hypothesis; but not for Person B and C).")

