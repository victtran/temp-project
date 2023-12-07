import pandas as pd
import Levenshtein
from heapq import nlargest  


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
# ######################################


# def search_nested_dict(nested_dict, target_value):
#     for key, value in nested_dict.items():
#         if key == target_value or search_nested_dict(value, target_value):
#             return key
#     return None


# def search_nested_dict_similarity_original_case(nested_dict, target_value):
#     best_match = None
#     best_distance = float('inf')

#     for key, value in nested_dict.items():
#         distance = Levenshtein.distance(target_value.lower(), key.lower())
        
#         if distance < best_distance:
#             best_distance = distance
#             best_match = key

#         child_match = search_nested_dict_similarity_original_case(value, target_value)
#         if child_match:
#             return child_match

#     return best_match

# def search_nested_dict_top5_similarity(nested_dict, target_value, top_k=5):
#     closest_matches = []

#     def search_recursive(node):
#         nonlocal closest_matches

#         for key, value in node.items():
#             distance = Levenshtein.distance(target_value.lower(), key.lower())

#             if len(closest_matches) < top_k:
#                 closest_matches.append((key, distance))
#             else:
#                 max_distance = max(closest_matches, key=lambda x: x[1])
#                 if distance < max_distance[1]:
#                     closest_matches.remove(max_distance)
#                     closest_matches.append((key, distance))

#             search_recursive(value)

#     search_recursive(nested_dict)

#     # Return the top 5 closest matches
#     return nlargest(top_k, closest_matches, key=lambda x: x[1])

# ################################################################ New tests
# import Levenshtein  # You may need to install this library: pip install python-Levenshtein

# def search_nested_dict_similarity(nested_dict, target_value, top_k=5):
#     closest_matches = []

#     def search_recursive(node, current_path):
#         nonlocal closest_matches

#         for key, value in node.items():
#             distance = Levenshtein.distance(target_value.lower(), key.lower())

#             if len(closest_matches) < top_k:
#                 closest_matches.append((key, distance, current_path + [key]))
#             else:
#                 max_distance = max(closest_matches, key=lambda x: x[1])
#                 if distance < max_distance[1]:
#                     closest_matches.remove(max_distance)
#                     closest_matches.append((key, distance, current_path + [key]))

#             search_recursive(value, current_path + [key])

#     search_recursive(nested_dict, [])

#     # Return the top 5 closest matches with their parents and children
#     return closest_matches




# def search_nested_dict_top5_similarity1(nested_dict, target_value, top_k=5):
#     closest_matches = []

#     def search_recursive(node, current_path):
#         nonlocal closest_matches

#         for key, value in node.items():
#             distance = Levenshtein.distance(target_value.lower(), key.lower())

#             if len(closest_matches) < top_k:
#                 closest_matches.append((key, distance, current_path + [key]))
#             else:
#                 max_distance = max(closest_matches, key=lambda x: x[1])
#                 if distance < max_distance[1]:
#                     closest_matches.remove(max_distance)
#                     closest_matches.append((key, distance, current_path + [key]))

#             search_recursive(value, current_path + [key])

#     search_recursive(nested_dict, [])

#     # Return the top 5 closest matches with their parents and children
#     return nlargest(top_k, closest_matches, key=lambda x: x[1])


#############Good Code############
# def search_nested_dict_top5_similarity(nested_dict, target_value, top_k=5):
#     closest_matches = []

#     def search_recursive(node, current_path):
#         nonlocal closest_matches

#         for key, value in node.items():
#             distance = Levenshtein.distance(target_value.lower(), key.lower())

#             if len(closest_matches) < top_k:
#                 closest_matches.append((key, distance, current_path + [key]))
#             else:
#                 max_distance = max(closest_matches, key=lambda x: x[1])
#                 if distance < max_distance[1]:
#                     closest_matches.remove(max_distance)
#                     closest_matches.append((key, distance, current_path + [key]))

#             search_recursive(value, current_path + [key])

#     search_recursive(nested_dict, [])

#     # Return the top 5 closest matches with their parents and children
#     top_matches = nlargest(top_k, closest_matches, key=lambda x: x[1])
#     results = []

#     for match in top_matches:
#         path = match[2]
#         match_with_children = find_children_path(nested_dict, path)
#         results.append((match[0], path, match_with_children))

#     return results

# def find_children_path(node, path):
#     for key in path:
#         node = node[key]

#     children_path = list(node.keys())
#     return children_path
#############Good Code############


def search_nested_dict_top5_similarity(nested_dict, target_value, top_k=5):
    closest_matches = []

    def search_recursive(node, current_path):
        nonlocal closest_matches

        for key, value in node.items():
            distance = Levenshtein.distance(target_value.lower(), key.lower())

            if len(closest_matches) < top_k:
                closest_matches.append((key, distance, current_path + [key]))
            else:
                max_distance = max(closest_matches, key=lambda x: x[1])
                if distance < max_distance[1]:
                    closest_matches.remove(max_distance)
                    closest_matches.append((key, distance, current_path + [key]))

            search_recursive(value, current_path + [key])

    search_recursive(nested_dict, [])

    # Return the top 5 closest matches with their complete hierarchy
    top_matches = nlargest(top_k, closest_matches, key=lambda x: x[1])
    results = []

    for match in reversed(top_matches):
        path = match[2]
        complete_hierarchy = find_complete_hierarchy(nested_dict, path)
        results.append((match[0], path, complete_hierarchy))

    return results

def find_complete_hierarchy(node, path):
    for key in path:
        node = node[key]

    complete_hierarchy = recursive_children(node, 0)
    return complete_hierarchy

def recursive_children(node, level):
    children = []
    for key, value in node.items():
        children.append(f"{' ' * (level * 2)}- {key}")  # Adjust the indentation level
        children.extend(recursive_children(value, level + 1))

    return children



################################################################

# Example usage:
csv_file_path = 'mindmaptest2.csv'
nested_dict = parse_csv_to_dict(csv_file_path)
#print(nested_dict)


# Example usage:
target_input = 'training team'
results = search_nested_dict_top5_similarity(nested_dict, target_input)
for result in results:
    print(f"Found value '{target_input}' or similar in the nested dictionary.")
    print(f"Closest match: {result[0]}")
    print(f"Path: {' -> '.join(result[1])}")
    print("Complete Hierarchy:")
    print("\n".join(result[2]))
    print()

#############Good Code############
# target_input = 'name'
# results = search_nested_dict_top5_similarity(nested_dict, target_input)
# for result in results:
#     print(f"Found value '{target_input}' or similar in the nested dictionary.")
#     print(f"Closest match: {result[0]}")
#     print(f"Path: {' -> '.join(result[1])}")
#     print(f"Children: {result[2]}")
#     print()
#############Good Code############



# Example usage:
# target_input = 'name'
# results = search_nested_dict_similarity(nested_dict, target_input)
# for result in results:
#     print(f"Found value '{target_input}' or similar in the nested dictionary.")
#     print(f"Closest match: {result[0]}")
#     print(f"Path: {' -> '.join(result[2])}")
#     print()


# target_value = 'name'
# top_matches = search_nested_dict_top5_similarity(nested_dict, target_value)

# if top_matches:
#     print(f"Found value '{target_value}' or similar in the nested dictionary. Top 5 closest matches:")
#     for match in top_matches:
#         print(f" - {match[0]} (Distance: {match[1]})")
# else:
#     print(f"Value '{target_value}' or similar not found in the nested dictionary.")


# target_input = 'name'
# results = search_nested_dict_top5_similarity1(nested_dict, target_input)
# for result in results:
#     print(f"Found value '{target_input}' or similar in the nested dictionary.")
#     print(f"Closest match: {result[0]}")
#     print(f"Path: {' -> '.join(result[2])}")
#     print()

########################################################S


# target_value = 'E-mail:'
# result = search_nested_dict(nested_dict, target_value) #fix to see level in b/w

# if result:
#     print(f"Found value '{target_value}' in the nested dictionary. Parent key: {result}")
# else:
#     print(f"Value '{target_value}' not found in the nested dictionary.")


# target_value = 'emiial'
# result = search_nested_dict_similarity_original_case(nested_dict, target_value)

# if result:
#     print(f"Found value '{target_value}' or similar in the nested dictionary. Closest match: {result}")
# else:
#     print(f"Value '{target_value}' or similar not found in the nested dictionary.")



# target_value = 'fiRST NAme'
# top_matches = search_nested_dict_top5_similarity(nested_dict, target_value)

# if top_matches:
#     print(f"Found value '{target_value}' or similar in the nested dictionary. Top 5 closest matches:")
#     for match in top_matches:
#         print(f" - {match[0]} (Distance: {match[1]})")
# else:
#     print(f"Value '{target_value}' or similar not found in the nested dictionary.")


