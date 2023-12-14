def nested_dict_to_list(nested_dict, current_path=None):
    if current_path is None:
        current_path = []

    result = []
    for key, value in nested_dict.items():
        current_path.append(key)
        if isinstance(value, dict):
            result.extend(nested_dict_to_list(value, current_path.copy()))
        else:
            result.append(current_path.copy())
        current_path.pop()

    return result
