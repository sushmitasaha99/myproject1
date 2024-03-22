import pandas as pd
import matplotlib.pyplot as plt
import os

def load_data(file_path):
    """
    Load data from a CSV file into a pandas DataFrame.

    Args:
        file_path (str): Path to the CSV file.

    Returns:
        pandas.DataFrame: Loaded data from the CSV file.
    """
    return pd.read_csv(file_path)

def replace_country_codes(dataframe):
    """
    Replacing numerical country codes with corresponding country names.

    Args:
        dataframe (pandas.DataFrame): DataFrame containing country codes.

    Returns:
        pandas.DataFrame: DataFrame with country codes replaced by country names.
    """
    country_mapping = {1: 'Germany', 2: 'India', 3: 'Indonesia'}
    dataframe['Country_of_Residence'] = dataframe['Country_of_Residence'].map(country_mapping)
    return dataframe

def replace_experience_labels(dataframe):
    """
    Replacing numerical values with corresponding labels in the 'CS_Experience' column.

    Args:
        dataframe (pandas.DataFrame): DataFrame containing 'CS_Experience' column.

    Returns:
        pandas.DataFrame: DataFrame with numerical values replaced by labels in the 'CS_Experience' column.
    """
    dataframe['CS_Experience'] = dataframe['CS_Experience'].replace({1: 'Yes', 2: 'No'})
    return dataframe

def filter_data(dataframe):
    """
    Filtering the DataFrame based on the 'CS_Experience' column.

    Args:
        dataframe (pandas.DataFrame): DataFrame to be filtered.

    Returns:
        pandas.DataFrame: Filtered DataFrame.
    """
    return dataframe[dataframe['CS_Experience'].isin(['Yes', 'No'])]

def calculate_ratios(dataframe):
    """
    Calculating ratios of 'Yes' and 'No' occurrences by country.

    Args:
    dataframe (pandas.DataFrame): The DataFrame containing 'Yes' and 'No' occurrences.

    Returns:
    pandas.DataFrame: The DataFrame with calculated ratios.
    """
    counts_by_country = dataframe.groupby(['Country_of_Residence', 'CS_Experience']).size().unstack().reset_index()
    counts_by_country[counts_by_country.columns[1:]] = counts_by_country[counts_by_country.columns[1:]].apply(pd.to_numeric, errors='coerce')
    counts_by_country['Ratio_Yes'] = counts_by_country['Yes'] / counts_by_country[['Yes', 'No']].sum(axis=1)
    counts_by_country['Ratio_No'] = counts_by_country['No'] / counts_by_country[['Yes', 'No']].sum(axis=1)
    return counts_by_country

def plot_ratio_bar_chart(dataframe, save_path=None):
    """
    Plotting a horizontal bar chart showing the ratio of participants who experienced climate-related shocks or extreme weather events.

    Args:
        dataframe (pandas.DataFrame): DataFrame containing ratios.
        save_path (str, optional): Path to save the plot as an image file. Defaults to None.
    """
    fig, ax = plt.subplots(figsize=(10, 6))
    fig.set_facecolor('white')
    dataframe.set_index('Country_of_Residence')[['Ratio_Yes', 'Ratio_No']].plot(kind='barh', stacked=True, ax=ax, color=['green', 'lightcoral'])
    ax.set_title('Ratio of Participants who Experienced Climate-Related Shocks or Extreme Weather Events')
    ax.set_xlabel('Ratio')
    ax.set_ylabel('Country')

    for idx, (ratio_yes, ratio_no) in enumerate(zip(dataframe['Ratio_Yes'], dataframe['Ratio_No'])):
        if not pd.isna(ratio_yes):
            ax.text(ratio_yes / 2, idx, f'{ratio_yes:.2%}', ha='center', va='center', color='white', fontweight='bold')
        if not pd.isna(ratio_no):
            ax.text(ratio_yes + ratio_no / 2, idx, f'{ratio_no:.2%}', ha='center', va='center', color='white', fontweight='bold')

    ax.grid(False)
    plt.legend(['Yes', 'No'])

    if save_path:
        plt.savefig(save_path, bbox_inches='tight', dpi=300)
        
        """
        Save the plot as a PNG file.

        """

    plt.show()

if __name__ == "__main__":

    combined_data = load_data('bld/survey_data.csv')

    combined_data = replace_country_codes(combined_data)

    combined_data = replace_experience_labels(combined_data)

    combined_data_cleaned = filter_data(combined_data)

    counts_by_country = calculate_ratios(combined_data_cleaned)

    plot_ratio_bar_chart(counts_by_country, save_path=os.path.join('bld', 'Fig5.png'))
