import Levenshtein
from heapq import nlargest

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

    # Return the top 5 closest matches, sorted by distance in ascending order
    return sorted(closest_matches, key=lambda x: x[1])[:top_k]
