import pandas as pd
from fuzzywuzzy import process

def fuzzy_search_keyword_in_dataframe(csv_path, keyword):
    # Read CSV file into a DataFrame
    df = pd.read_csv(csv_path)

    # Perform fuzzy matching to find the best match
    best_match, score = process.extractOne(keyword, df.values.flatten(), scorer=fuzzywuzzy.fuzz.token_sort_ratio)

    # Print the best match and its score
    print(f"Best Match: {best_match}")
    print(f"Score: {score}")

    # Search for rows containing the best match
    matching_rows = df[df.apply(lambda row: best_match in row.astype(str), axis=1)]

    # Print the matching rows
    print("\nMatching Rows:")
    print(matching_rows)

# Example usage
csv_file_path = "your_file.csv"  # Replace with the path to your CSV file
search_keyword = "your_keyword"  # Replace with the keyword you're searching for

fuzzy_search_keyword_in_dataframe(csv_file_path, search_keyword)
