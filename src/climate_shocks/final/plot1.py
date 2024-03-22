import os
import pandas as pd
import plotly.express as px

def read_and_process_data():
    """
    Reads survey data from a CSV file and processes it.

    1. Specifying the path to the CSV file stored in the bld folder
    2. Reading the file into a pandas DataFrame
    3. Replacing column names

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

    We begin with  defining the list of persons, then initializing an empty DataFrame to store average values for both high and low risk, and finally, iterating through persons and calculate average values for both high and low risk

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

    Returns:
    plotly.graph_objs.Figure: Plotly figure object representing the combined chart.
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


'''
def save_chart_as_image(fig_combined):
    """
    Saves the combined chart as PNG inside the bld folder.

    Args:
    fig_combined (plotly.graph_objs.Figure): Plotly figure object representing the combined chart.
    """
    fig_combined.write_image("bld/Fig1.png")

if __name__ == "__main__":
    df = read_and_process_data()
    average_data_combined = calculate_average_ratings(df)
    categories_order = ['sustainability', 'moral', 'I would', 'Others would', 'People should']
    fig_combined = create_and_show_chart(average_data_combined, categories_order)
    save_chart_as_image(fig_combined)

'''

def save_chart_as_image():
    """
    Saves the combined chart as PNG inside the bld folder.

    Args:
    fig_combined (plotly.graph_objs.Figure): Plotly figure object representing the combined chart.
    """
    df = read_and_process_data()
    average_data_combined = calculate_average_ratings(df)
    categories_order = ['sustainability', 'moral', 'I would', 'Others would', 'People should']
    fig_combined = create_and_show_chart(average_data_combined, categories_order)
    file_path = "bld/Fig1.png"
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    fig_combined.write_image(file_path)

if __name__ == "__main__":
    save_chart_as_image()
