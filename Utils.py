def cut_namespace(string_with_namespace: str) -> str:
    return string_with_namespace.split(":", 1)[1]
