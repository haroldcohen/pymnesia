FILTER_FUNCTIONS_REGISTRY = {}
REL_FILTER_FUNCTIONS_REGISTRY = {}


def register_filter_func(*, filter_name: str, relational: bool = False):
    """Allows to register a filter function

    :param filter_name: The filter name.
    :param relational: Whether the function is used for relational filter or not.
    :return: A decorator that will register the filter function.
    """

    def decorator(func):
        if not relational:
            FILTER_FUNCTIONS_REGISTRY[filter_name] = func
        else:
            REL_FILTER_FUNCTIONS_REGISTRY[filter_name] = func

        return func

    return decorator


def find_filter_function(filter_name: str, relational: bool = False):
    """Retrieves a filter function based on its filter name.

    :param filter_name: The filter name for which to retrieve a filter function.
    :param relational: Whether the function is used for relational filter or not.
    :return: A callable that can be used for filtering.
    """
    if not relational:
        return FILTER_FUNCTIONS_REGISTRY[filter_name]

    return REL_FILTER_FUNCTIONS_REGISTRY[filter_name]
