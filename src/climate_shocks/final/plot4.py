import os
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.ticker import FixedLocator

def load_data(file_path):
    """
    Loading data from a CSV file into a pandas DataFrame.

    Args:
        file_path (str): Path to the CSV file.

    Returns:
        pandas.DataFrame: Loaded data from the CSV file.
    """
    return pd.read_csv(file_path)

def plot_countplots():
    """
    Ploting countplots for selected columns.

    This function generates countplots for each selected column based on the provided DataFrame.
    """
   
    file_path = 'bld/survey_data.csv'

    
    df = load_data(file_path)

    selected_columns = ['ClimateConcern', 'ClimateDamage', 'ClimateCause', 'ClimateCauseProbability', 'Country_of_Residence']

    
    country_mapping = {1: 'Germany', 2: 'India', 3: 'Indonesia'}
    df_selected = df[selected_columns].copy()
    df_selected['Country_of_Residence'] = df_selected['Country_of_Residence'].map(country_mapping)

    response_order = {
        'ClimateConcern': ['not at all worried', 'not very worried', 'somewhat worried', 'very worried'],
        'ClimateDamage': ['not at all', 'only a little', 'quite a bit', 'a great deal'],
        'ClimateCause': ['a result of natural causes', 'a result of human activities'],
        'ClimateCauseProbability': ['a result of natural causes', 'a result of human activities']
    }

    
    fig, axes = plt.subplots(nrows=2, ncols=2, figsize=(15, 8))

    colors = {'Germany': 'red', 'India': 'green', 'Indonesia': 'blue'}

    for i, col in enumerate(selected_columns[:-1]):
        sns.countplot(x=col, hue='Country_of_Residence', data=df_selected, ax=axes[i // 2, i % 2], palette=colors)

        if col == 'ClimateCauseProbability':
            axes[i // 2, i % 2].set_xticks([0, 1])
            axes[i // 2, i % 2].set_xticklabels(['a result of human activities', 'a result of natural causes'])
            axes[i // 2, i % 2].set_xlabel('')
            axes[i // 2, i % 2].set_title('In your opinion, is the increased probability of climate shocks mainly...')

        if col == 'ClimateCause':
            axes[i // 2, i % 2].set_xticks([0, 1])
            axes[i // 2, i % 2].set_xticklabels(['a result of human activities', 'a result of natural causes'])
            axes[i // 2, i % 2].set_xlabel('')
            axes[i // 2, i % 2].set_title('Do you think that climate shocks are mainly...')

        if col == 'ClimateDamage':
            axes[i // 2, i % 2].set_xticks([0, 1, 2, 3])
            axes[i // 2, i % 2].set_xticklabels(['not at all', 'only a little', 'quite a bit', 'a great deal'])
            axes[i // 2, i % 2].set_xlabel('')
            axes[i // 2, i % 2].set_title('How much do you think climate shocks will harm people in your place?')

        if col == 'ClimateConcern':
            axes[i // 2, i % 2].set_xticks([0, 1, 2, 3])
            axes[i // 2, i % 2].set_xticklabels(['not at all worried', 'not very worried', 'somewhat worried', 'very worried'])
            axes[i // 2, i % 2].set_xlabel('')
            axes[i // 2, i % 2].set_title('How worried are you about climate shocks?')

    
    output_folder = 'bld'
    output_file_path = os.path.join(output_folder, 'Fig4.png')
    plt.tight_layout(rect=[0, 0, 1, 1])
    plt.savefig(output_file_path, format='png')

    plt.show()

if __name__ == '__main__':
    plot_countplots()
