### Test Cases from test_model.py:

| Test Case                      | Reasoning                                                                                  | Scenario                                                           | Input                                                               | Expected Output                                                       | Assertion                                                                |
|--------------------------------|--------------------------------------------------------------------------------------------|--------------------------------------------------------------------|----------------------------------------------------------------------|-----------------------------------------------------------------------|--------------------------------------------------------------------------|
| `test_load_data`               | Tests data loading mechanism for CSV files                                                 | Valid CSV file is provided                                        | Valid test data in CSV format                                       | The loaded data matches the test data                                 | The loaded data is equal to the test data                                |
| `test_replace_column_names`    | Tests column names replacement mechanism                                                   | Test DataFrame with column names containing underscores           | Test DataFrame with column names containing underscores              | Column names with underscores replaced with spaces                      | Replaced column names match the expected column names                     |
| `test_perform_t_test`          | Tests t-test computation functionality                                                      | Test t-test computation for all persons and categories            | Test data, persons ['A'], and categories ['sustainability', 'moral'] | Results for t-test for all combinations of persons and categories     | The length of the t-test results matches the expected length            |

### Test Cases from test_clean_data.py:

| Test Case                      | Reasoning                                                                                  | Scenario                                                           | Input                                                               | Expected Output                                                       | Assertion                                                                |
|--------------------------------|--------------------------------------------------------------------------------------------|--------------------------------------------------------------------|----------------------------------------------------------------------|-----------------------------------------------------------------------|--------------------------------------------------------------------------|
| `test_read_data`               | Tests reading data from a valid CSV file                                                    | Valid CSV file provided                                           | Valid sample data saved in CSV format                                | Loaded data matches the sample data                                   | The loaded data is equal to the sample data                              |
| `test_clean_column_names`      | Tests cleaning column names with leading and trailing spaces                                 | Column names with leading and trailing spaces                     | Sample data with column names containing leading and trailing spaces | Column names without leading and trailing spaces                       | Cleaned column names match the expected column names                     |
| `test_rename_countries`        | Tests renaming original country values                                                      | Original country values                                           | Sample data with original country values                              | Country values replaced with renamed values                            | Renamed country values match the expected values                         |
| `test_save_filtered_data`      | Tests saving sample data to a CSV file                                                      | Sample data to be saved                                           | Sample data to be saved to a CSV file                                 | CSV file containing the sample data                                    | The saved data matches the sample data                                   |

### Test Cases from test_plots.py:


| Test Function                 | Description                                                                                           |
|-------------------------------|-------------------------------------------------------------------------------------------------------|
| `test_load_data`                 | Tests if data is loaded correctly and returned object is a pandas DataFrame.                          |
| `test_plot_countplots`        | Tests if countplots are generated without errors.                                                      |
| `test_filter_data`             | Tests for filtering data.                                                                             |
| `test_replace_country_codes`   | Tests if country codes are replaced correctly.                                                         |
| `test_replace_experience_labels` | Tests if experience labels are replaced correctly.                                                    |
| `test_calculate_ratios`        | Tests for calculating ratios.                                                                         |
| `test_plot_ratio_bar_chart`    | Tests if plot is generated without errors.                                                             |
| `test_read_and_process_data`   | Placeholder test for read_and_process_data function.                                                   |
| `test_calculate_average_ratings` | Placeholder test for calculate_average_ratings function.                                               |
| `test_create_and_show_chart`   | Placeholder test for create_and_show_chart function.                                                   |
| `test_save_chart_as_image`     | Placeholder test for save_chart_as_image function.                                                     |
