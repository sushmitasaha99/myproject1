import pandas as pd
import plotly.express as px

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
