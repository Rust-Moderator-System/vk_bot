from app.filtres.abc import ABCFilter


def execute_filters(data, filters: list[ABCFilter]) -> bool:
    for filter in filters:
        if not filter(data):
            return False
    return True
