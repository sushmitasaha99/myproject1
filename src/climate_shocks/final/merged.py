import pandas as pd
import matplotlib.pyplot as plt
import os
import plotly.express as px
from scipy.stats import ttest_ind
import seaborn as sns
from matplotlib.ticker import FixedLocator

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
        
    plt.show()

def read_and_process_data():
    """
    Reads survey data from a CSV file and processes it.

    Returns:
    pandas.DataFrame: Processed DataFrame containing survey data.
    """
    
    file_path = 'bld/survey_data.csv'

   
    df = pd.read_csv(file_path)
    df = df.apply(pd.to_numeric, errors='coerce')

    
    df.columns = df.columns.str.replace('I_would', 'I would').str.replace('others_would', 'Others would').str.replace('people_should', 'People should')

    return df

def calculate_average_ratings(df):
    """
    Calculates average ratings for different categories among persons A, B, and C.

    Args:
    df (pandas.DataFrame): Processed DataFrame containing survey data.

    Returns:
    pandas.DataFrame: DataFrame containing average ratings for each category, person, and risk level.
    """
    
    persons = ['A', 'B', 'C']

    average_data_combined = pd.DataFrame()

    categories_order = ['sustainability', 'moral', 'I would', 'Others would', 'People should']

    for person in persons:
        for risk in ['Low', 'High']:
            for category in categories_order:
                col_name = f'JB_{risk.lower()}_{person}_{category}'
                average_value = df[col_name].mean()
                person_data = pd.DataFrame({'Person': [person], 'Category': [category], 'Risk': [risk], 'Average Rating': [average_value]})
                average_data_combined = pd.concat([average_data_combined, person_data])

    return average_data_combined

def create_and_show_chart(average_data_combined, categories_order):
    """
    Creates a grouped bar chart for average ratings and displays it.

    Args:
    average_data_combined (pandas.DataFrame): DataFrame containing average ratings for each category, person, and risk level.
    categories_order (list): Order of categories for the chart.
    """

    fig_combined = px.bar(average_data_combined, x='Category', y='Average Rating', color='Person', facet_col='Risk',
                          title='Comparison of Ratings Among Persons A, B, and C for Low and High Climate Risk',
                          category_orders={'Category': categories_order},
                          labels={'Person': 'Person'},
                          height=500, barmode='group')  

    fig_combined.update_traces(texttemplate='%{y:.2f}', textposition='outside')

    fig_combined.update_xaxes(ticktext=['Sustainability', 'Moral', 'I would', 'Others would', 'People should'])


    fig_combined.show()
    
    return fig_combined

def save_chart_as_image(fig_combined, save_path):
    """
    Saves the combined chart as PNG inside the bld folder.

    Args:
    fig_combined (plotly.graph_objs.Figure): Plotly figure object representing the combined chart.
    """
    fig_combined.write_image(save_path)

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

if __name__ == "__main__":
    
    df = read_and_process_data()

    average_data_combined = calculate_average_ratings(df)

    categories_order = ['sustainability', 'moral', 'I would', 'Others would', 'People should']

    fig_combined = create_and_show_chart(average_data_combined, categories_order)

    save_chart_as_image(fig_combined, "bld/Fig1.png")

    t_test_results = perform_t_test(df, ['A', 'B', 'C'], categories_order)

    visualize_p_values_heatmap(t_test_results, save_path="bld/Fig2.png")

    combined_data = load_data('bld/survey_data.csv')
    combined_data = replace_country_codes(combined_data)
    combined_data = replace_experience_labels(combined_data)
    combined_data = filter_data(combined_data)
    counts_by_country = calculate_ratios(combined_data)

    plot_ratio_bar_chart(counts_by_country, save_path="bld/Fig5.png")

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



def analyze_gea_scores(csv_file):
    """
    Analyzing General Environmental Attitude (GEA) scores and visualizing the results.

    Args:
        csv_file (str): Path to the CSV file containing GEA score data.

    Returns:
        None

    This function performs the following steps:
    1. Importing the GEA score data from the input CSV file.
    2. Reversing the utilization items across different scales.
    3. Calculating the overall GEA score.
    4. Visualizing the GEA score distribution by country using a histogram.
    5. Categorizing individuals as pro-environmentalists or not based on a cutoff score of 4.
    6. Visualizing the distribution of pro-environmentalists by country using a grouped bar chart.
    """

    data = pd.read_csv(csv_file, header=0)


    data['EAI_7r'] = 8 - data['EAI_7']
    data['EAI_8r'] = 8 - data['EAI_8']
    data['EAI_9r'] = 8 - data['EAI_9']
    data['EAI_10r'] = 8 - data['EAI_10']
    data['EAI_13r'] = 8 - data['EAI_13']
    data['EAI_14r'] = 8 - data['EAI_14']
    data['EAI_17r'] = 8 - data['EAI_17']
    data['EAI_18r'] = 8 - data['EAI_18']
    data['EAI_19r'] = 8 - data['EAI_19']
    data['EAI_20r'] = 8 - data['EAI_20']


    data['score'] = (data['EAI_1'] + data['EAI_2'] + data['EAI_3'] + data['EAI_4'] + data['EAI_5'] +
                     data['EAI_6'] + data['EAI_7r'] + data['EAI_8r'] + data['EAI_9r'] + data['EAI_10r'] +
                     data['EAI_11'] * data['EAI_12'] + data['EAI_13r'] + data['EAI_14r'] + data['EAI_15'] +
                     data['EAI_16'] + data['EAI_17r'] + data['EAI_18r'] + data['EAI_19r'] + data['EAI_20r'] +
                     data['EAI_21'] + data['EAI_22'] + data['EAI_23'] + data['EAI_24']) / 24

    fig = px.histogram(data, x='score', color='Country_of_Residence',
                       marginal='rug', histnorm='percent', barmode='overlay',
                       opacity=0.7, nbins=20, title='GEA score by Country')
    fig.update_layout(xaxis_title='GEA Score', yaxis_title='Frequency (%)')
 
    fig.show()

    fig.write_image("bld/Fig03.png")

    data['pro_environmentalist'] = data['score'].apply(lambda x: 'Pro' if x > 4 else 'Not Pro')

    pro_env_data = data.groupby(['Country_of_Residence', 'pro_environmentalist']).size().unstack()
    pro_env_data.reset_index(inplace=True)
    fig = px.bar(pro_env_data, x='Country_of_Residence', y=['Not Pro', 'Pro'],
                 barmode='group', title='Pro-environmentalist by Country',
                 labels={'value': 'Count', 'variable': 'Pro-environmentalist'})
    fig.update_layout(xaxis_title='Country', yaxis_title='Count')
 
    fig.show()

    fig.write_image("bld/Fig3.png")


analyze_gea_scores("bld/clean_filtered_data.csv")

