import pandas as pd
import plotly.express as px
import os

def visualize_age_distribution(save_path="bld/age_distribution.png"):
    """
    Loading survey data from a CSV file, map numerical values to labels,
    and create a histogram to visualize the distribution of ages based
    on whether participants live in a place where natural resources are
    extracted.
    
    Args:
        save_path (str): Path to save the figure image.
    
    Returns:
        None
    """
    df = pd.read_csv("bld/survey_data.csv")
    df['CS_Extraction'] = df['CS_Extraction'].map({1: 'Yes', 2: 'No'})

    fig = px.histogram(df, x='Age', color='CS_Extraction', 
                       barmode='group', 
                       title='Distribution of Age by Living in a place where natural resources are extracted',
                       labels={'Age': 'Age', 'count': 'Count'},
                       template='plotly_dark',  
                       opacity=0.7,  
                       histnorm='percent',  
                       category_orders={'CS_Extraction': ['Yes', 'No']},  
                       color_discrete_map={'Yes': '#1f77b4', 'No': '#ff7f0e'}  
                      )
    fig.update_xaxes(title_text='Age')
    fig.update_yaxes(title_text='Percentage of Participants')
    
    
    os.makedirs(os.path.dirname(save_path), exist_ok=True)
    
   
    fig.write_image(save_path)


visualize_age_distribution()
