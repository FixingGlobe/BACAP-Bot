def cut_namespace(string_with_namespace: str) -> str:
    return string_with_namespace.split(":", 1)[1]


def common_elements(*lists):
    """
    :param lists: Any number of lists
    :return: Elements that can be found in all lists
    """
    sets = [set(lst) for lst in lists if lst is not None]
    return list(set.intersection(*sets))
