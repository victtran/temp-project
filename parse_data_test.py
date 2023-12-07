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

def search_nested_dict(nested_dict, target_value):
    for key, value in nested_dict.items():
        if key == target_value or search_nested_dict(value, target_value):
            return key
    return None



import Levenshtein

def search_nested_dict_similarity_original_case(nested_dict, target_value):
    best_match = None
    best_distance = float('inf')

    for key, value in nested_dict.items():
        distance = Levenshtein.distance(target_value.lower(), key.lower())
        
        if distance < best_distance:
            best_distance = distance
            best_match = key

        child_match = search_nested_dict_similarity_original_case(value, target_value)
        if child_match:
            return child_match

    return best_match



from heapq import nlargest

def search_nested_dict_top5_similarity(nested_dict, target_value, top_k=5):
    closest_matches = []

    def search_recursive(node):
        nonlocal closest_matches

        for key, value in node.items():
            distance = Levenshtein.distance(target_value.lower(), key.lower())

            if len(closest_matches) < top_k:
                closest_matches.append((key, distance))
            else:
                max_distance = max(closest_matches, key=lambda x: x[1])
                if distance < max_distance[1]:
                    closest_matches.remove(max_distance)
                    closest_matches.append((key, distance))

            search_recursive(value)

    search_recursive(nested_dict)

    # Return the top 5 closest matches
    return nlargest(top_k, closest_matches, key=lambda x: x[1])



# Example usage:
csv_file_path = 'mindmaptest.csv'

df = pd.read_csv(csv_file_path, header =None, skiprows=1)

for i,col in enumerate(df.columns[1:], start=1):
    df[col] = df[col].shift(-1*col)
df = df.dropna(axis=0, how='all')
df = df.reset_index(drop=True)
df.to_csv('new_mindmap.csv')  
#print(df)

mindmap_data = create_nested_dict_from_csv(df)

# Convert lists to dictionaries
convert_to_dict_structure(mindmap_data)

# Print the resulting nested dictionary
import pprint
pprint.pprint(mindmap_data)

# target_value = 'E-mail:'
# result = search_nested_dict(mindmap_data, target_value) #fix to see level in b/w

# if result:
#     print(f"Found value '{target_value}' in the nested dictionary. Parent key: {result}")
# else:
#     print(f"Value '{target_value}' not found in the nested dictionary.")


# target_value = 'emiial'
# result = search_nested_dict_similarity_original_case(mindmap_data, target_value)

# if result:
#     print(f"Found value '{target_value}' or similar in the nested dictionary. Closest match: {result}")
# else:
#     print(f"Value '{target_value}' or similar not found in the nested dictionary.")



# target_value = 'fiRST NAme'
# top_matches = search_nested_dict_top5_similarity(mindmap_data, target_value)

# if top_matches:
#     print(f"Found value '{target_value}' or similar in the nested dictionary. Top 5 closest matches:")
#     for match in top_matches:
#         print(f" - {match[0]} (Distance: {match[1]})")
# else:
#     print(f"Value '{target_value}' or similar not found in the nested dictionary.")