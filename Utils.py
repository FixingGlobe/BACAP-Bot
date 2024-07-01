from typing import List, Any, TextIO, Set


def cut_namespace(string_with_namespace: str) -> str:
    if ":" in string_with_namespace:
        return string_with_namespace.split(":", 1)[1]
    return string_with_namespace


def open_text_file(path: str) -> TextIO:
    return open(path, encoding="utf-8")


def read_text_file(path: str) -> str:
    with open(path, encoding="utf-8") as file:
        return file.read()


def set_intersection(*sets: Set[Any]) -> List[Any]:
    """
    :param lists: Any number of lists
    :return: Elements that can be found in all lists
    """
    return list(set.intersection(*sets))


def hex_to_int(hex: str) -> int:
    return int(hex.lstrip('#'), 16)
