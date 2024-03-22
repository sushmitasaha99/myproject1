"""Tasks running the results formatting (tables, figures)."""

import pandas as pd
import pytask
from climate_shocks.config import BLD, GROUPS, SRC
from climate_shocks.final.plot1 import read_and_process_data, calculate_average_ratings, create_and_show_chart, save_chart_as_image
from climate_shocks.final.plot2 import load_data, replace_column_names, visualize_p_values_heatmap, perform_t_test
from climate_shocks.final.Plot3 import analyze_gea_scores
from climate_shocks.final.plot4 import load_data, plot_countplots
from climate_shocks.final.plot5 import load_data, replace_country_codes, replace_experience_labels, filter_data, plot_ratio_bar_chart, calculate_ratios
from climate_shocks.utilities import read_yaml

deps = {
    "data": BLD / "survey_data.csv",
}


@pytask.task
def task_plot_results(
    depends_on=deps,
    produces=BLD / "Fig1.png",
):
    """Plotting results (Python version).

    Args:
        depends_on (dict): Dependency dictionary containing the path to the data file.
        produces (str): Path to the produced figure.

    Returns:
        Plot showing participants' response to different levels of climate shocks.
    """
    df = read_and_process_data()  
    average_data = calculate_average_ratings(df)  
    categories_order = ['sustainability', 'moral', 'I would', 'Others would', 'People should']

    fig = create_and_show_chart(average_data, categories_order)  


if __name__ == "__main__":
    
    for group in GROUPS:
        task_plot_results(depends_on={**deps, "group": group})


@pytask.task
def task_plot_countplots(
    depends_on=deps,
    produces=BLD / "Fig4.png",
):
    """Plotting countplots (Python version).

    Args:
        depends_on (dict): Dependency dictionary containing the path to the data file.
        produces (str): Path to the produced figure.

    Returns:
        Plot showing cross-country analysis.
    """
    plot_countplots()

if __name__ == "__main__":
    for group in GROUPS:
        task_plot_countplots(depends_on={**deps, "group": group})

@pytask.task
def task_plot_ratio_bar_chart(
    depends_on=deps,
    produces=BLD / "Fig5.png",
):
    """Plotting ratio bar chart (Python version).

    Args:
        depends_on (dict): Dependency dictionary containing the path to the data file.
        produces (str): Path to the produced figure.

    Returns:
        The plot where it shows the ratio of participants who has experienced climate shocks in their countries"
    """
    combined_data = load_data(BLD / "survey_data.csv")
    combined_data = replace_country_codes(combined_data)
    combined_data = replace_experience_labels(combined_data)
    combined_data_cleaned = filter_data(combined_data)
    counts_by_country = calculate_ratios(combined_data_cleaned)
    plot_ratio_bar_chart(counts_by_country, save_path=produces)

if __name__ == "__main__":
    for group in GROUPS:
        task_plot_ratio_bar_chart(depends_on={**deps, "group": group})


