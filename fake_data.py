import random

import pandas as pd
from faker import Faker


def generate_data(num_records=100):
    """
    Generate fake employee data.

    Parameters
    ----------
    num_records : int, optional
        The number of records to generate. Defaults to 100.

    Returns
    -------
    pandas.DataFrame
        A DataFrame with the generated data.
    """
    fake = Faker()
    
    names = [fake.unique.first_name() for _ in range(num_records)]
    
    min_salary = 30000
    max_salary = 150000
    min_age = 20
    max_age = 65
    departments = [
        "Sales", "Marketing", "Finance", "HR", "IT",
        "Operations", "Customer Service", "Legal", "R&D", "Administration"
    ]
    
    data = []
    for i in range(num_records):
        record = {
            "id": i + 1,
            "name": names[i],
            "salary": random.randint(min_salary, max_salary),
            "age": random.randint(min_age, max_age),
            "department": random.choice(departments)
        }
        data.append(record)
    
    return pd.DataFrame(data)

def main():
    """
    Generates sample data with 100 records and saves it to a CSV file.

    The data includes the following columns: id, name, salary, age, department.
    """
    df = generate_data(100)

    df.to_csv("data.csv", index=False)
    print("Data generated and saved to sample_data_generated.csv")

if __name__ == "__main__":
    main()
