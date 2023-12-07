import pandas as pd

def parse_csv_to_dict(csv_file_path):
    # Read the CSV file into a DataFrame
    df = pd.read_csv(csv_file_path)

    # Convert the DataFrame to a nested dictionary
    nested_dict = {}
    for index, row in df.iterrows():
        current_dict = nested_dict
        for level in row.dropna():
            if level not in current_dict:
                current_dict[level] = {}
            current_dict = current_dict[level]

    return nested_dict