import pandas as pd

def create_nested_dict_from_csv(df):

    def fill_structure(node, row_index, col_index):
        if col_index >= len(df.columns):
            return

        current_value = str(df.iloc[row_index, col_index])  # Convert to string
        if pd.isna(df.iloc[row_index, col_index]):

        
            ####FIX multiple same level####

            return  # Skip NaN values

        if current_value not in node:
            node[current_value] = {}
        fill_structure(node[current_value], row_index, col_index + 1)

    root_node = {}
    for row_index in range(len(df)):
        fill_structure(root_node, row_index, 0)

    return root_node

def convert_to_dict_structure(d):
    for key, value in d.items():
        if isinstance(value, dict):
            convert_to_dict_structure(value)
        elif isinstance(value, list):
            if len(value) == 1 and isinstance(value[0], dict):
                d[key] = value[0]
            elif not value:
                d[key] = None
            else:
                d[key] = merge_dicts(value)

def merge_dicts(dicts):
    result = {}
    for d in dicts:
        for key, value in d.items():
            if key not in result:
                result[key] = value
            else:
                result[key].append(value)
    return result