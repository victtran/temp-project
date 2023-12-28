def find_path_for_exact_string(nested_dict, target_string):
    path = []

    def search_recursive(node, current_path):
        for key, value in node.items():
            if key == target_string:
                # If the target string is found, update the path and return
                current_path.append(key)
                path.extend(current_path)
                return

            # Recursively search in child dictionaries
            search_recursive(value, current_path + [key])

    # Start the recursive search from the top-level
    search_recursive(nested_dict, [])

    return path
