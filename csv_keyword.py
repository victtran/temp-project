import pandas as pd

def search_keyword_in_dataframe(csv_path, keyword):
    # Read CSV file into a DataFrame
    df = pd.read_csv(csv_path)

    # Iterate over rows and print rows containing the keyword
    for index, row in df.iterrows():
        if keyword.lower() in row.astype(str).str.lower().values:
            print(f"Row {index + 1}:", row)

# Example usage
csv_file_path = "your_file.csv"  # Replace with the path to your CSV file
search_keyword = "your_keyword"  # Replace with the keyword you're searching for

search_keyword_in_dataframe(csv_file_path, search_keyword)
