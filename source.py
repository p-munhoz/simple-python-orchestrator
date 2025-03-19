import pandas as pd


def read_csv_file(filepath: str):
    """
    Reads a CSV file given its filepath and returns the loaded DataFrame.

    Args:
        filepath (str): The path to the CSV file to be loaded.

    Returns:
        pandas.DataFrame: The loaded DataFrame.
    """
    df = pd.read_csv(filepath)
    print("CSV loaded successfully")
    return df

def filter_departments(df):
    """
    Filters the DataFrame to include only specified departments.

    Args:
        df (pandas.DataFrame): The DataFrame containing employee data with a 'department' column.

    Returns:
        pandas.DataFrame: A DataFrame filtered to include only rows where the 'department' is in the specified list.
    """

    departments_to_include = ['IT', 'Finance']
    filtered_df = df[df['department'].isin(departments_to_include)]
    print(f"Filtered departments: {departments_to_include}")
    return filtered_df

def compute_average_salary(df):
    """
    Computes the average salary for each department in the given DataFrame and saves the result to a CSV file.

    Args:
        df (pandas.DataFrame): The DataFrame containing employee data with a 'salary' and 'department' column.

    Returns:
        pandas.DataFrame: A DataFrame with two columns: 'department' and 'salary', where 'salary' is the mean salary for each department.
    """
    average_salary = df.groupby('department')['salary'].mean().reset_index()
    average_salary.to_csv("average_salary.csv", index=False)
    print("Calculated average salary per department:")
    print(average_salary)
    return average_salary

