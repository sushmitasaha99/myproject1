import os
import pandas as pd
from scipy.stats import ttest_ind
import seaborn as sns
import matplotlib.pyplot as plt


def load_data(file_path):
    """
    Loads survey data from a CSV file into a pandas DataFrame.

    Args:
    file_path (str): The path to the CSV file.

    Returns:
    pandas.DataFrame: DataFrame containing survey data.
    """
    return pd.read_csv(file_path).apply(pd.to_numeric, errors='coerce')

def replace_column_names(dataframe):
    """
    Replaces column names in the DataFrame to enhance readability.

    Args:
    dataframe (pandas.DataFrame): Input DataFrame.

    Returns:
    pandas.DataFrame: DataFrame with replaced column names.
    """
    return dataframe.rename(columns=lambda x: x.replace('I_would', 'I would')
                                                .replace('others_would', 'Others would')
                                                .replace('people_should', 'People should'))

def visualize_p_values_heatmap(dataframe, save_path=None):
    """
    Visualizes a heatmap of p-values for t-tests comparing low vs. high risk ratings among different categories and persons.

    Args:
    dataframe (pandas.DataFrame): DataFrame containing t-test results.
    save_path (str, optional): Path to save the plot image. 
    """
    heatmap_data = dataframe.pivot(index='Person', columns='Category', values='P-Value')

    plt.figure(figsize=(12, 8))
    sns.heatmap(heatmap_data, annot=True, cmap='Greens', linewidths=.5, fmt=".3f")
    plt.title('P-Values Heatmap for T-Tests (Low vs. High Risk)')

    
    if save_path:
        plt.savefig(save_path)

    plt.show()

def perform_t_test(dataframe, persons, categories_order):
    """
    Performs independent t-tests for low and high risk ratings among different categories and persons.

    Args:
    dataframe (pandas.DataFrame): DataFrame containing survey data.
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


persons = ['A', 'B', 'C']
categories_order = ['sustainability', 'moral', 'I would', 'Others would', 'People should']
t_test_results = perform_t_test(df, persons, categories_order)


save_path = 'bld/Fig2.png'  
visualize_p_values_heatmap(t_test_results, save_path)


print("Dataframe shape after loading:", df.shape)
print("T-test results:")
print(t_test_results)
print("Calling visualization function...")
