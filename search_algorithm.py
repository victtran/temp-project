import Levenshtein
from heapq import nlargest

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
