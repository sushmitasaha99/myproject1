from pathlib import Path
import pandas as pd
import pytask
from climate_shocks.analysis.model import load_data, perform_t_test
from climate_shocks.config import BLD, GROUPS, SRC
from climate_shocks.utilities import read_yaml

# Defining dependencies for the task
fit_model_deps = {
    "data": BLD / "survey_data.csv",
}

# Defining a task for performing independent t-tests
def perform_t_tests(
    depends_on=fit_model_deps,
    produces=BLD / "python" / "results" / "t_test_results.csv",
):
    """
    Perform independent t-tests for low and high risk ratings among different categories and persons.
    """
    # Loading the data
    data = load_data(depends_on["data"])
    # Performing t-tests
    persons = ['A', 'B', 'C']
    categories_order = ['sustainability', 'moral', 'I would', 'Others would', 'People should']
    t_test_results = perform_t_test(data, persons, categories_order)
    # Saving the results to a CSV file
    t_test_results.to_csv(produces, index=False)

