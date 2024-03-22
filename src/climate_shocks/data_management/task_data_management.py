"""Tasks for managing the data."""

from pathlib import Path

import pandas as pd

from climate_shocks.config import BLD, SRC
from climate_shocks.data_management.clean_data import read_data
from climate_shocks.data_management.clean_data import clean_column_names
from climate_shocks.data_management.clean_data import rename_countries
from climate_shocks.data_management.clean_data import filter_data
from climate_shocks.data_management.clean_data import save_filtered_data
from climate_shocks.data_management.clean_data import clean_data
from climate_shocks.data_management.clean_data import main
from climate_shocks.utilities import read_yaml

clean_data_deps = {
    "scripts": Path("clean_data.py"),
    "data_info": SRC / "data_management" / "data_info.yaml",
    "data": BLD / "survey_data.csv",
}


def task_clean_data_python(
    depends_on=clean_data_deps,
    produces=BLD / "clean_filtered_data.csv",
):
    """Clean the data (Python version)."""
    data_info = read_yaml(depends_on["data_info"])
    data = pd.read_csv(depends_on["data"])
    data = clean_data(data)
    data.to_csv(produces, index=False)
